from pulsar.schema import *

from verifica_inventario.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)


class ComandoVerificarInventarioOrdenPayload(ComandoIntegracion):
    usuario = String()


class ComandoVerificarInventarioOrden(ComandoIntegracion):
    data = ComandoVerificarInventarioOrdenPayload()
