import logging
import traceback
from dataclasses import dataclass

from pydispatch import dispatcher

from verifica_inventario.modulos.aplicacion.comandos.base import VerificaInventarioBaseHandler
from verifica_inventario.modulos.aplicacion.dto import OrdenCreadaDTO
from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.modulos.dominio.repositorios import RepositorioOrdenesCreadas
from verifica_inventario.modulos.infraestructura.dto import OrdenCreada
from verifica_inventario.modulos.infraestructura.fabricas import FabricaRepositorio
from verifica_inventario.seedwork.aplicacion.comandos import Comando
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando as comando


@dataclass
class CompensarOrdenVerificada(Comando):

    def __init__(self, orden_creada_dto: OrdenCreadaDTO):
        self.event_id = orden_creada_dto.event_id
        self.id_orden = orden_creada_dto.id_orden
        self.usuario = orden_creada_dto.usuario
        self.direccion_usuario = orden_creada_dto.direccion_usuario

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return

        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenesCreadas)
        orden = db.session.query(OrdenCreada).filter(OrdenCreada.id_orden == self.id_orden).one()
        orden_dominio = repositorio.obtener_por_id(self.id_orden)
        if orden:
            db.session.delete(orden)
            db.session.commit()
            orden_dominio.verificar_orden(self.event_id)
            self.publicar_eventos_post_commit(orden_dominio)

    def publicar_eventos_post_commit(self, orden: Orden):
        try:
            for evento in orden.eventos:
                dispatcher.send(signal=f'{type(evento).__name__}Compensacion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()


class CompensarOrdenVerificadaHandler(VerificaInventarioBaseHandler):

    def handle(self, comando: CompensarOrdenVerificada):
        from verifica_inventario.config.db import db

        comando.ejecutar(db=db)


@comando.register(CompensarOrdenVerificada)
def ejecutar_comando_compensar_orden_verificada(comando: CompensarOrdenVerificada, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = CompensarOrdenVerificadaHandler()
            handler.handle(comando)
    except:
        traceback.print_exc()
        logging.error('ERROR: Al revertir cambios en operación de compensación!')
