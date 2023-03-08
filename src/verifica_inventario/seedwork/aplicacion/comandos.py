from functools import singledispatch
from abc import ABC, abstractmethod

from verifica_inventario.seedwork.aplicacion.dto import DTO


class Comando:
    @abstractmethod
    def inicializa_estado_comando(self, dto: DTO):
        raise NotImplementedError()


class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Comando):
        raise NotImplementedError()


@singledispatch
def ejecutar_commando(comando):
    raise NotImplementedError(f'No existe implementación para el comando de tipo {type(comando).__name__}')
