"""Objetos valor del dominio de verificación de inventario

En este archivo usted encontrará los objetos valor del dominio de verificación de inventario

"""
from dataclasses import dataclass
from enum import Enum

from verifica_inventario.seedwork.dominio.objetos_valor import ObjetoValor, Ciudad


@dataclass(frozen=True)
class Email(ObjetoValor):
    address: str
    dominio: str
    es_empresarial: bool


@dataclass(frozen=True)
class Rut(ObjetoValor):
    numero: int
    ciudad: Ciudad


@dataclass(frozen=True)
class Descripcion(ObjetoValor):
    descripcion: str


class TipoProducto(Enum):
    BIENES_CONSUMO = "BienesConsumo"
    SERVICIOS = "Servicios"
    BIENES_USO_COMUN = "BienesUsoComun"
    BIENES_EMERGENCIA = "BienesEmergencia"
    BIENES_DURABLES = "BienesDurables"
    BIENES_ESPECIALIDAD = "BienesEspecialidad"


@dataclass(frozen=True)
class NombreBodega():
    nombre: str


@dataclass(frozen=True)
class Direccion(ObjetoValor):
    direccion: str


@dataclass(frozen=True)
class Coordenada(ObjetoValor):
    grados: int
    minutos: int
    segundos: int
    hemisferio: str


@dataclass(frozen=True)
class Latitud(Coordenada):
    ...


@dataclass(frozen=True)
class Longitud(Coordenada):
    ...


@dataclass(frozen=True)
class Ubicacion(ObjetoValor):
    latitud: Latitud
    longitud: Longitud
    ciudad: Ciudad = None


@dataclass(frozen=True)
class NombreCentroDistribucion(ObjetoValor):
    nombre: str


@dataclass(frozen=True)
class Item(ObjetoValor):
    descripcion: str


@dataclass(frozen=True)
class Usuario(ObjetoValor):
    nombre: str


class EstadoOrden(str, Enum):
    REGISTRADA = "Registrada"
    APROBADA = "Aprobada"
    PENDIENTE = "Pendiente"
