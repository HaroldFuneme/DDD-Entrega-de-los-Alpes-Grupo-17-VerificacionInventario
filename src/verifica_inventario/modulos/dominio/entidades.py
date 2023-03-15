"""Entidades del dominio de verificación de inventario

En este archivo usted encontrará las entidades del dominio de verificación de inventario

"""
from __future__ import annotations

from dataclasses import dataclass, field

from verifica_inventario.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from .eventos import OrdenVerificada
from .objetos_valor import Descripcion, TipoProducto, Direccion, NombreBodega, Ubicacion, \
    NombreCentroDistribucion, Item, Usuario, EstadoOrden


@dataclass
class Producto(Entidad):
    descripcion: Descripcion = None
    tipo_producto: TipoProducto = None


@dataclass
class Bodega(Entidad):
    id_bodega: str = None
    nombre_bodega: NombreBodega = None
    direccion: Direccion = None
    ubicacion: Ubicacion = None


@dataclass
class CentroDistribucion(Bodega):
    nombre_centro_distribucion: NombreCentroDistribucion = None


@dataclass
class UbicacionItem(Entidad):
    item: Item = None
    bodega: Bodega = None


@dataclass
class Orden(AgregacionRaiz):
    id_orden: str = None
    usuario: Usuario = None
    direccion_usuario: Direccion = None
    items: list[Item] = field(default_factory=list[Item])
    ubicacion_items: list[UbicacionItem] = field(default_factory=list[UbicacionItem])
    estado: EstadoOrden = field(default=EstadoOrden.REGISTRADA)
    items_bodegas: list[UbicacionItem] = field(default_factory=list[UbicacionItem])
    items_centros: list[UbicacionItem] = field(default_factory=list[UbicacionItem])
    items_pendientes: list[UbicacionItem] = field(default_factory=list[UbicacionItem])

    def registrar_orden(self, orden: Orden):
        self.id_orden = orden.id_orden
        self.usuario = orden.usuario
        self.direccion_usuario = orden.direccion_usuario
        self.items = orden.items
        self.estado = orden.estado

        # self.agregar_evento(
        #     OrdenRegistrada(id=orden.id, id_orden=orden.id_orden, usuario=orden.usuario, estado=orden.estado))

    def verificar_orden(self, evento_id: str):
        self.items_bodegas = list()
        self.items_centros = list()
        self.items_pendientes = list()
        for ubicacion_item in self.ubicacion_items:
            if ubicacion_item.bodega and ubicacion_item.bodega.__class__ == CentroDistribucion:
                self.items_centros.append(ubicacion_item)
            elif ubicacion_item.bodega and ubicacion_item.bodega.__class__ == Bodega:
                self.items_bodegas.append(ubicacion_item)
            else:
                self.items_pendientes.append(ubicacion_item)

        self.agregar_evento(
            OrdenVerificada(id=evento_id, id_orden=self.id_orden, usuario=self.usuario,
                            direccion_usuario=self.direccion_usuario,
                            items_bodegas=self.items_bodegas, items_centros=self.items_centros,
                            items_pendientes=self.items_pendientes))
