import uuid

from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.seedwork.dominio.repositorios import Mapeador
from .dto import Item as ItemDTO
from .dto import OrdenCreada as OrdenCreadaDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from ..dominio.eventos import EventoVerificaInventario, OrdenRegistrada
from ..dominio.objetos_valor import Item
from ...seedwork.dominio.entidades import Entidad


class MapeadorOrdenCreada(Mapeador):

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenCreadaDTO:
        orden_creada_dto = OrdenCreadaDTO()
        orden_creada_dto.id_orden = entidad.id_orden
        orden_creada_dto.usuario = entidad.usuario
        orden_creada_dto.direccion_usuario = entidad.direccion_usuario

        items_dto = list()
        for item in entidad.items:
            items_dto.append(self._mapear_item_a_dto(item))

        orden_creada_dto.items = items_dto

        return orden_creada_dto

    def dto_a_entidad(self, dto: OrdenCreadaDTO) -> Orden:
        orden_creada = Orden(id_orden=dto.id_orden, usuario=dto.usuario, direccion_usuario=dto.direccion_usuario)
        orden_creada.items = list()

        items_dto: list[ItemDTO] = dto.items

        for item in items_dto:
            item_entidad: Item(descripcion=item)
            orden_creada.items.append(item_entidad)

        return orden_creada

    def _mapear_item_a_dto(self, item) -> ItemDTO:
        item_dto = ItemDTO()
        item_dto.id = str(uuid.uuid4())
        item_dto.descripcion = item.descripcion
        return item_dto


class MapeadorEventosOrdenCreada(Mapeador):
    # Versiones aceptadas
    versions = ('v1',)

    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            OrdenRegistrada: self._entidad_a_orden_creada
        }

    def obtener_tipo(self) -> type:
        return EventoVerificaInventario.__class__

    def es_version_valida(self, version):
        for v in self.versions:
            if v == version:
                return True
        return False

    def _entidad_a_orden_creada(self, entidad: OrdenRegistrada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import OrdenCreada, EventoOrdenCreada

            payload = OrdenCreada(
                ordenId=str(evento.id_orden),
                user=str(evento.usuario),
                estado=str(evento.estado)
            )
            evento_integracion = EventoOrdenCreada(id=str(evento.event_id))
            evento_integracion.id = str(evento.id)
            evento_integracion.eventId = str(evento.id)
            evento_integracion.spec_version = str(version)
            evento_integracion.type = 'EventoOrdenCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'verifica_inventario'
            evento_integracion.data = payload

            return evento_integracion

        if not self.es_version_valida(version):
            raise Exception(f'No se sabe procesar la version {version}')

        if version == 'v1':
            return v1(entidad)

    def entidad_a_dto(self, entidad: EventoVerificaInventario, version=LATEST_VERSION) -> OrdenCreadaDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, version=version)

    def dto_a_entidad(self, dto: any) -> Entidad:
        raise NotImplementedError
