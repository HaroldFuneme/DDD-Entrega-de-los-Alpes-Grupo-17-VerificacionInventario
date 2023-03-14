import logging
import traceback
from dataclasses import dataclass

from verifica_inventario.modulos.aplicacion.comandos.base import VerificaInventarioBaseHandler
from verifica_inventario.modulos.aplicacion.dto import ItemDTO, OrdenCreadaDTO
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorOrdenCreada
from verifica_inventario.modulos.dominio.entidades import Orden, InventarioBodega, Producto, Bodega, CentroDistribucion
from verifica_inventario.modulos.dominio.fabricas import FabricaVerificacionInventario
from verifica_inventario.modulos.dominio.objetos_valor import Descripcion, TipoProducto, Direccion, \
    NombreCentroDistribucion
from verifica_inventario.modulos.dominio.repositorios import RepositorioOrdenesCreadas
from verifica_inventario.modulos.infraestructura.fabricas import FabricaRepositorio
from verifica_inventario.seedwork.aplicacion.comandos import Comando
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando as comando


@dataclass
class AgregarOrdenCreada(Comando):
    event_id: str
    id_orden: str
    usuario: str
    direccion_usuario: str
    items: list[ItemDTO]

    def inicializa_estado_comando(self, orden_creada_dto: OrdenCreadaDTO):
        self.event_id = orden_creada_dto.event_id
        self.id_orden = orden_creada_dto.id_orden
        self.usuario = orden_creada_dto.usuario
        self.direccion_usuario = orden_creada_dto.direccion_usuario

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return

        orden_creada_dto = OrdenCreadaDTO(
            event_id=self.event_id
            , id_orden=self.id_orden
            , usuario=self.usuario
            , direccion_usuario=self.direccion_usuario
            , items=self.items)

        # Crea objeto de dominio a partir de objeto de capa de aplicación
        fabrica_verificacion_inventario = FabricaVerificacionInventario()
        orden: Orden = fabrica_verificacion_inventario.crear_objeto(orden_creada_dto,
                                                                    MapeadorOrdenCreada())

        # Se agrega evento de registro/aceptación de la orden
        orden.registrar_orden(orden)
        orden.verificar_inventario(obtener_inventario())

        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenesCreadas)

        repositorio.agregar(orden)

        db.session.commit()


def obtener_productos():
    productos = list()
    for i in range(4):
        producto = Producto(descripcion=Descripcion(descripcion=f'item{i}'), tipo_producto=TipoProducto.BIENES_CONSUMO)
        productos.append(producto)
    return productos


def obtener_inventario():
    inventario_eda = list()
    for i in range(3):
        bodega = Bodega(nombre_bodega=f'Bodega {i}',
                        direccion=Direccion(direccion=f'Calle {i} # {i} - {i}'))
        inventario_bodega = InventarioBodega(bodega=bodega, productos=obtener_productos())
        inventario_eda.append(inventario_bodega)

    for i in range(2):
        nombre_centro_dist = NombreCentroDistribucion(nombre=f'Centro de Distribucion {i}')
        centro_distribucion = CentroDistribucion(nombre_centro_distribucion=nombre_centro_dist,
                                                 direccion=Direccion(direccion=f'Carrera {i} # {i} - {i}'))
        inventario_centro_dist = InventarioBodega(bodega=centro_distribucion, productos=obtener_productos())
        inventario_eda.append(inventario_centro_dist)

    return inventario_eda


class AgregarOrdenCreadaHandler(VerificaInventarioBaseHandler):

    def handle(self, comando: AgregarOrdenCreada):
        from verifica_inventario.config.db import db

        comando.ejecutar(db=db)


@comando.register(AgregarOrdenCreada)
def ejecutar_comando_crear_reserva(comando: AgregarOrdenCreada, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = AgregarOrdenCreadaHandler()
            handler.handle(comando)
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
