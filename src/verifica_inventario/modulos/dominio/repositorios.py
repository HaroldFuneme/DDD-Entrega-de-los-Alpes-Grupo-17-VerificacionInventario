from abc import ABC
from verifica_inventario.seedwork.dominio.repositorios import Repositorio


class RepositorioOrdenesCreadas(Repositorio, ABC):
    ...


class RepositorioEventosOrdenesVerificadas(Repositorio, ABC):
    ...
