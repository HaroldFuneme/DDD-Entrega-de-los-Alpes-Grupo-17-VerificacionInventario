""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de vuelos

"""

from dataclasses import dataclass

from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioOrdenesCreadasSQLAlchemy, RepositorioEventosOrdenesVerificadasSQLAlchemy
from ..dominio.repositorios import RepositorioOrdenesCreadas, RepositorioEventosOrdenesVerificadas
from ...seedwork.dominio.fabricas import Fabrica
from ...seedwork.dominio.repositorios import Repositorio


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenesCreadas:
            return RepositorioOrdenesCreadasSQLAlchemy()
        if obj == RepositorioEventosOrdenesVerificadas:
            return RepositorioEventosOrdenesVerificadasSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
