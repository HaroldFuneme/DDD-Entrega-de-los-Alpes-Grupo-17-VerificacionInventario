import json
import logging
import traceback

import _pulsar
import aiopulsar
import pulsar
from pulsar.schema import AvroSchema, Record

from verifica_inventario.modulos.aplicacion.comandos.agregar_orden_creada import AgregarOrdenCreada
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorEventoOrdenCreadaDTOJson
from verifica_inventario.modulos.infraestructura.schema.v1.comandos import ComandoVerificarInventarioOrden
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando
from verifica_inventario.seedwork.infraestructura import utils


async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record,
                               tipo_consumidor: _pulsar.ConsumerType = _pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                    topico,
                    consumer_type=tipo_consumidor,
                    subscription_name=suscripcion,
                    schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    print(mensaje)
                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    await consumidor.acknowledge(mensaje)

    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()


# def suscribirse_a_eventos(app=None):
#     cliente = None
#     try:
#         cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
#         consumidor = cliente.subscribe('eventos-ordenes-creadas', consumer_type=_pulsar.ConsumerType.Shared,
#                                        subscription_name='sub-eventos-ordenes-creadas',
#                                        schema=AvroSchema(EventoOrdenCreada))
#
#         while True:
#             mensaje = consumidor.receive()
#             datos = mensaje.value()
#             print(f'Evento recibido: {datos}')
#             # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
#             ## Mapear json a DTO de aplicación.
#             dto = MapeadorEventoOrdenCreadaDTOJson().externo_a_dto(mensaje.value())
#             ## Crear instancia de comando para procesar evento, AgregarOrdenCreada. Recibe DTO cómo parámetro
#             comando = AgregarOrdenCreada(event_id=dto.event_id, id_orden=dto.id_orden, usuario=dto.usuario,
#                                          direccion_usuario=dto.direccion_usuario, items=dto.items)
#             ## Invocar ejecutar_commando(comando)
#             ejecutar_commando(comando)
#             consumidor.acknowledge(mensaje)
#
#         cliente.close()
#     except:
#         logging.error('ERROR: Suscribiendose al tópico de eventos!')
#         traceback.print_exc()
#         if cliente:
#             cliente.close()
#
#
# def suscribirse_a_comandos(app=None):
#     cliente = None
#     try:
#         cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
#         consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared,
#                                        subscription_name='aeroalpes-sub-comandos',
#                                        schema=AvroSchema(ComandoVerificarInventarioOrden))
#
#         while True:
#             mensaje = consumidor.receive()
#             print(f'Comando recibido: {mensaje.value().data}')
#
#             consumidor.acknowledge(mensaje)
#
#         cliente.close()
#     except:
#         logging.error('ERROR: Suscribiendose al tópico de comandos!')
#         traceback.print_exc()
#         if cliente:
#             cliente.close()
