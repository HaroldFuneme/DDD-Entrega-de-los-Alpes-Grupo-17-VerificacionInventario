from dataclasses import dataclass

from verifica_inventario.seedwork.dominio.eventos import EventoDominio


class EventoVerificaInventario(EventoDominio):
    ...


@dataclass
class OrdenRegistrada(EventoVerificaInventario):
    id_orden: str = None
    usuario: str = None
    estado: str = None


@dataclass
class OrdenVerificada(EventoVerificaInventario):
    id_orden: str = None
    usuario: str = None
    direccion_usuario: str = None
    items_bodegas: list() = None
    items_centros: list() = None
    items_pendientes: list() = None
