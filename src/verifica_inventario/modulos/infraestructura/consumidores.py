import logging
import os
import traceback

import _pulsar
import pulsar
from pulsar.schema import AvroSchema

from verifica_inventario.modulos.aplicacion.comandos.agregar_orden_creada import AgregarOrdenCreada
from verifica_inventario.modulos.aplicacion.comandos.compensar_orden_verificada import CompensarOrdenVerificada
from verifica_inventario.modulos.aplicacion.dto import OrdenCreadaDTO
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorEventoOrdenCreadaDTOJson
from verifica_inventario.modulos.infraestructura.proyecciones import ProyeccionVerificaInventarioOrden
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada, \
    InventarioVerificadoCompensacion
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando
from verifica_inventario.seedwork.infraestructura import utils
from verifica_inventario.seedwork.infraestructura.proyecciones import ejecutar_proyeccion


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        topico_eventos_orden = os.getenv('TOPICO_EVENTOS_ORDEN', default="evento-orden-a")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico_eventos_orden, consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sub-eventos-orden-creada',
                                       schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value()
            print(f'Evento recibido: {datos}')
            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ## Mapear json a DTO de aplicación.
            dto = MapeadorEventoOrdenCreadaDTOJson().externo_a_dto(mensaje.value())

            try:
                with app.app_context():
                    ## Crear instancia de comando para procesar evento, AgregarOrdenCreada. Recibe DTO cómo parámetro
                    comando = AgregarOrdenCreada(event_id=dto.event_id, id_orden=dto.id_orden, usuario=dto.usuario,
                                                 direccion_usuario=dto.direccion_usuario, items=dto.items)
                    ## Invocar ejecutar_commando(comando)
                    ejecutar_commando(comando, app=app)
                    ejecutar_proyeccion(ProyeccionVerificaInventarioOrden(dto), app=app)
                    consumidor.acknowledge(mensaje)
            except:
                logging.error('ERROR: Procesando evento de orden creada!')
                traceback.print_exc()

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        topico_comandos = os.getenv('TOPICO_COMANDOS', default="verifica-inventario-compensacion")
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(topico_comandos, consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='sub-verifica-inventario-compensacion',
                                       schema=AvroSchema(InventarioVerificadoCompensacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value()}')

            orden_creada_dto = OrdenCreadaDTO(mensaje.value().eventId,
                                              mensaje.value().payload.ordenId,
                                              mensaje.value().payload.user,
                                              mensaje.value().payload.user_address)
            try:
                with app.app_context():
                    ## Crear instancia de comando para procesar compensación. Recibe DTO cómo parámetro
                    comando = CompensarOrdenVerificada(orden_creada_dto)
                    ## Invocar ejecutar_commando(comando)
                    ejecutar_commando(comando, app=app)
                    consumidor.acknowledge(mensaje)
            except:
                logging.error('ERROR: Procesando comando de compensación!')
                traceback.print_exc()

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
