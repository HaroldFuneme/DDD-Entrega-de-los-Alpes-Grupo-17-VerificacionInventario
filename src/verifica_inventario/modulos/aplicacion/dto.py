from dataclasses import dataclass, field

from verifica_inventario.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class ItemDTO(DTO):
    descripcion: str = field(default_factory=str)


@dataclass(frozen=True)
class OrdenCreadaDTO(DTO):
    event_id: str = field(default_factory=str)
    id_orden: str = field(default_factory=str)
    usuario: str = field(default_factory=str)
    direccion_usuario: str = field(default_factory=str)
    items: list[str] = field(default_factory=list[str])
