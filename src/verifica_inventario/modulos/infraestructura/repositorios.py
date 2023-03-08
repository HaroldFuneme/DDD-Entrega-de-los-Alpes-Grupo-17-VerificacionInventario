from uuid import UUID

from pulsar.schema import JsonSchema

from verifica_inventario.config.db import db
from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.modulos.dominio.fabricas import FabricaVerificacionInventario
from verifica_inventario.modulos.dominio.repositorios import RepositorioOrdenesCreadas, RepositorioEventosOrdenesVerificadas
from verifica_inventario.modulos.infraestructura.dto import EventosOrden
from verifica_inventario.modulos.infraestructura.mapeadores import MapeadorOrdenCreada, MapeadorEventosOrdenCreada
from .dto import OrdenCreada as OrdenCreadaDTO


class RepositorioOrdenesCreadasSQLAlchemy(RepositorioOrdenesCreadas):

    def __init__(self):
        self._fabrica_verificacion_inventario: FabricaVerificacionInventario = FabricaVerificacionInventario()

    @property
    def fabrica_verificacion_inventario(self):
        return self._fabrica_verificacion_inventario

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenCreadaDTO).filter_by(id=str(id)).one()
        return self._fabrica_verificacion_inventario.crear_objeto(orden_dto, MapeadorOrdenCreada())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden_creada: Orden):
        orden_creada_dto = self.fabrica_verificacion_inventario.crear_objeto(orden_creada,
                                                                             MapeadorOrdenCreada())
        db.session.add(orden_creada_dto)

    def actualizar(self, orden_creada: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError


class RepositorioEventosOrdenesVerificadasSQLAlchemy(RepositorioEventosOrdenesVerificadas):

    def __init__(self):
        self._fabrica_verificacion_inventario: FabricaVerificacionInventario = FabricaVerificacionInventario()

    @property
    def fabrica_verificacion_inventario(self):
        return self._fabrica_verificacion_inventario

    def obtener_por_id(self, id: UUID) -> Orden:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, evento):
        orden_evento = self._fabrica_verificacion_inventario.crear_objeto(evento, MapeadorEventosOrdenCreada())

        parser_payload = JsonSchema(orden_evento.data.__class__)
        json_str = parser_payload.encode(orden_evento.data)

        # OrdenRegistrada(id=orden.id, id_orden=orden.id_orden, usuario=orden.usuario, estado=orden.estado)
        evento_dto = EventosOrden()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_orden)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.version = str(orden_evento.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(orden_evento.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, orden_creada: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError
