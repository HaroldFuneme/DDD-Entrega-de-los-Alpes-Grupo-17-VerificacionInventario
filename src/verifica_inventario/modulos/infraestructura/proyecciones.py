import logging
import traceback
from abc import ABC, abstractmethod

from pydispatch import dispatcher

from verifica_inventario.modulos.aplicacion.dto import OrdenCreadaDTO
from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.modulos.dominio.repositorios import RepositorioOrdenesCreadas
from verifica_inventario.modulos.infraestructura.dto import InventarioBodega, Bodega, UbicacionItem, OrdenCreada
from verifica_inventario.modulos.infraestructura.fabricas import FabricaRepositorio
from verifica_inventario.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from verifica_inventario.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion


class ProyeccionVerificaInventario(Proyeccion, ABC):

    @abstractmethod
    def ejecutar(self):
        ...


class ProyeccionVerificaInventarioOrden(ProyeccionVerificaInventario):

    def __init__(self, orden_creada_dto: OrdenCreadaDTO):
        self.event_id = orden_creada_dto.event_id
        self.id_orden = orden_creada_dto.id_orden
        self.usuario = orden_creada_dto.usuario
        self.direccion_usuario = orden_creada_dto.direccion_usuario
        self.items = orden_creada_dto.items

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return

        ubicacion_items = self.verificar_items_orden(db)

        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenesCreadas)
        orden = db.session.query(OrdenCreada).filter(OrdenCreada.id_orden == self.id_orden).one()

        if orden:
            orden.ubicacion_items = ubicacion_items
            db.session.commit()
            # orden = db.session.query(OrdenCreada).filter(OrdenCreada.id_orden == self.id_orden).one()
            orden_dominio = repositorio.obtener_por_id(self.id_orden)
            orden_dominio.verificar_orden(self.event_id)
            self.publicar_eventos_post_commit(orden_dominio)

    def publicar_eventos_post_commit(self, orden: Orden):
        try:
            for evento in orden.eventos:
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()

    def verificar_items_orden(self, db):
        ubicacion_items = list()
        for item in self.items:
            ubicacion_item = UbicacionItem()
            ubicacion_item.item_id = item
            ubicacion_item.orden_id = self.id_orden
            try:
                inventario, bodega = db.session.query(InventarioBodega, Bodega).filter(InventarioBodega.item_id == item,
                                                                                       InventarioBodega.cantidad_disponible > 0,
                                                                                       InventarioBodega.bodega_id == Bodega.id) \
                    .first()
                ubicacion_item.bodega_id = bodega.id
            except:
                ubicacion_item.bodega_id = None
                logging.error(f'WARNING: No se encontró disponibilidad para el item {item}')

            ubicacion_items.append(ubicacion_item)

        return ubicacion_items


class ProyeccionVerificaInventarioHandler(ProyeccionHandler):

    def handle(self, proyeccion: ProyeccionVerificaInventario):
        from verifica_inventario.config.db import db

        proyeccion.ejecutar(db=db)


@proyeccion.register(ProyeccionVerificaInventarioOrden)
def ejecutar_proyeccion_verifica_inventario(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionVerificaInventarioHandler()
            handler.handle(proyeccion)
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
