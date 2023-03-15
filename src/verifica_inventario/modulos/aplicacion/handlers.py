from verifica_inventario.modulos.infraestructura.despachadores import Despachador
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import InventarioVerificado, \
    InventarioVerificadoPayload, Ubicacion
from verifica_inventario.seedwork.aplicacion.handlers import Handler


class HandlerVerificaInventarioIntegracion(Handler):

    @staticmethod
    def handle_inventario_verificado(evento):
        items_bodegas = HandlerVerificaInventarioIntegracion.mapear_items_a_record(evento.items_bodegas)
        items_centros = HandlerVerificaInventarioIntegracion.mapear_items_a_record(evento.items_centros)
        items_pendientes = HandlerVerificaInventarioIntegracion.mapear_items_a_record(evento.items_pendientes)

        orden_verificada = InventarioVerificadoPayload(ordenId=evento.id_orden,
                                                       user=evento.usuario,
                                                       user_address=evento.direccion_usuario,
                                                       items_bodegas=items_bodegas,
                                                       items_centros=items_centros,
                                                       items_pendientes=items_pendientes)

        inventario_verificado = InventarioVerificado(eventId=str(evento.id), payload=orden_verificada)

        despachador = Despachador()
        despachador.publicar_mensaje(inventario_verificado, 'eventos-inventario-verificado')

    @staticmethod
    def mapear_items_a_record(items):
        items_record = list()
        for item_bodega in items:
            if item_bodega.bodega:
                ubicacion = Ubicacion(item=item_bodega.item.descripcion, address_bodega=item_bodega.bodega.direccion)
                items_record.append(ubicacion)
            else:
                ubicacion = Ubicacion(item=item_bodega.item.descripcion, address_bodega=None)
                items_record.append(ubicacion)
        return items_record
