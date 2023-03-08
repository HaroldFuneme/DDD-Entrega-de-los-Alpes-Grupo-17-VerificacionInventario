from verifica_inventario.modulos.infraestructura.despachadores import Despachador
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import InventarioVerificado, \
    InventarioVerificadoPayload
from verifica_inventario.seedwork.aplicacion.handlers import Handler


class HandlerVerificaInventarioIntegracion(Handler):

    @staticmethod
    def handle_inventario_verificado(evento):
        orden_verificada = InventarioVerificadoPayload(ordenId=evento.id_orden, user=evento.usuario,
                                                       user_address=evento.direccion_usuario,
                                                       items_bodegas=evento.items_bodegas,
                                                       items_centros=evento.items_centros)

        inventario_verificado = InventarioVerificado(eventId=evento.id, payload=orden_verificada)

        despachador = Despachador()
        despachador.publicar_mensaje(inventario_verificado, 'eventos-inventario-verificado')
