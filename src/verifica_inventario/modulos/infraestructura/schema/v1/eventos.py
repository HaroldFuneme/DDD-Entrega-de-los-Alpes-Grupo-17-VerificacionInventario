import uuid

from pulsar.schema import *

from verifica_inventario.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


# NOTE En este caso usamos composición de eventos, donde un evento de Ordenes es constituido
# por los eventos hijo. Recuerde que al ser mensajes inmutables, no consideramos conceptos como
# la herencia en los registros de esquemas. Por lo que el patrón de composición de mensajes se vuelve una buena opción
# esto nos permite seguir teniendo esquemas estrictos sin la necesidad de múltiples tópicos

class OrdenCreada(Record):
    ordenId = String()
    user = String()
    user_address = String()
    items = Array()


class OrdenValidada(Record):
    id = String()
    fecha_validacion = Long()


class EventoOrdenCreada(EventoIntegracion):
    eventId = String(default=str(uuid.uuid4()))
    spec_version = String(default="v1")
    eventName = String(default="OrdenCreada")
    eventDataFormat = String(default="JSON")
    payload = OrdenCreada

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InventarioVerificadoPayload(Record):
    ordenId = String()
    user = String()
    user_address = String()
    items_bodegas = Array()
    items_centros = Array()


class InventarioVerificado(EventoIntegracion):
    eventId = String(default=str(uuid.uuid4()))
    spec_version = String(default="v1")
    eventName = String(default="InventarioVerificado")
    eventDataFormat = String(default="JSON")
    payload = InventarioVerificadoPayload

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
