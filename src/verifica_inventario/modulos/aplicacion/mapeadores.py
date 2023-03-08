from verifica_inventario.modulos.aplicacion.dto import OrdenCreadaDTO, ItemDTO
from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.modulos.dominio.objetos_valor import Item
from verifica_inventario.seedwork.aplicacion.dto import Mapeador as AppMap
from verifica_inventario.seedwork.dominio.repositorios import Mapeador

PAYLOAD = 'payload'


class MapeadorOrdenCreadaDTOJson(AppMap):

    def externo_a_dto(self, externo: any) -> OrdenCreadaDTO:
        orden_creada_dto = OrdenCreadaDTO(externo.get('eventId'),
                                          externo.get(PAYLOAD).get('ordenId'),
                                          externo.get(PAYLOAD).get('user'),
                                          externo.get(PAYLOAD).get('user_address'))
        for item in externo.get(PAYLOAD).get('items', list()):
            orden_creada_dto.items.append(item)
        return orden_creada_dto

    def dto_a_externo(self, dto: OrdenCreadaDTO) -> any:
        return dto.__dict__

class MapeadorEventoOrdenCreadaDTOJson(AppMap):

    def externo_a_dto(self, evento: any) -> OrdenCreadaDTO:
        orden_creada_dto = OrdenCreadaDTO(evento.eventId,
                                          evento.payload.ordenId,
                                          evento.payload.user,
                                          evento.payload.user_address)
        for item in evento.payload.items:
            orden_creada_dto.items.append(item)
        return orden_creada_dto

    def dto_a_externo(self, dto: OrdenCreadaDTO) -> any:
        return dto.__dict__


class MapeadorOrdenCreada(Mapeador):

    def obtener_tipo(self) -> type:
        return Orden.__class__

    def entidad_a_dto(self, entidad: Orden) -> OrdenCreadaDTO:
        _id_orden = str(entidad.id_orden)
        usuario = entidad.usuario
        direccion_usuario = entidad.direccion_usuario
        items = entidad.items

        return OrdenCreadaDTO(id_orden=_id_orden, usuario=usuario, direccion_usuario=direccion_usuario, items=items)

    def dto_a_entidad(self, dto: OrdenCreadaDTO) -> Orden:
        orden_creada = Orden(id=dto.event_id,id_orden=dto.id_orden, usuario=dto.usuario, direccion_usuario=dto.direccion_usuario)
        orden_creada.items = list()

        items_dto: list[ItemDTO] = dto.items

        for item in items_dto:
            item_entidad = Item(descripcion=item)
            orden_creada.items.append(item_entidad)

        return orden_creada
