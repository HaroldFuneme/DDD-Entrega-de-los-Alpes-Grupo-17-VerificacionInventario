import json
import logging
import traceback

import _pulsar
import pulsar
from pulsar.schema import AvroSchema

from verifica_inventario.modulos.aplicacion.comandos.agregar_orden_creada import AgregarOrdenCreada
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorOrdenCreadaDTOJson
from verifica_inventario.modulos.infraestructura.schema.v1.comandos import ComandoVerificarInventarioOrden
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando
from verifica_inventario.seedwork.infraestructura import utils


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-ordenes-creadas', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sub-eventos-ordenes-creadas',
                                       schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')
            json_dict = json.dumps(mensaje.value())
            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ## Mapear json a DTO de aplicación.
            dto = MapeadorOrdenCreadaDTOJson().externo_a_dto(json_dict)
            ## Crear instancia de comando para procesar evento, AgregarOrdenCreada. Recibe DTO cómo parámetro
            comando = AgregarOrdenCreada()
            comando.inicializa_estado_comando(dto)
            ## Invocar ejecutar_commando(comando)
            ejecutar_commando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='aeroalpes-sub-comandos',
                                       schema=AvroSchema(ComandoVerificarInventarioOrden))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
