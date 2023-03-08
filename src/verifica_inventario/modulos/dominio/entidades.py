"""Entidades del dominio de verificación de inventario

En este archivo usted encontrará las entidades del dominio de verificación de inventario

"""
from __future__ import annotations
from dataclasses import dataclass, field

from verifica_inventario.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from .eventos import OrdenRegistrada, OrdenVerificada
from .objetos_valor import Descripcion, TipoProducto, Direccion, NombreBodega, Ubicacion, \
    NombreCentroDistribucion, Item, Usuario, EstadoOrden, UbicacionItem


@dataclass
class Producto(Entidad):
    descripcion: Descripcion = None
    tipo_producto: TipoProducto = None


@dataclass
class Bodega(Entidad):
    nombre_bodega: NombreBodega = None
    direccion: Direccion = None
    ubicacion: Ubicacion = None


class CentroDistribucion(Bodega):
    nombre_centro_distribucion: NombreCentroDistribucion = None


@dataclass
class InventarioBodega(AgregacionRaiz):
    bodega: Bodega = field(default=None)
    productos: list[Producto] = field(default_factory=list[Producto])


@dataclass
class Orden(AgregacionRaiz):
    id_orden: str = None
    usuario: Usuario = None
    direccion_usuario: Direccion = None
    items: list[Item] = field(default_factory=list[Item])
    estado: EstadoOrden = field(default=EstadoOrden.REGISTRADA)
    items_bodegas: list[UbicacionItem] = field(default_factory=list[Item])
    items_centros: list[UbicacionItem] = field(default_factory=list[Item])
    items_pendientes: list[UbicacionItem] = field(default_factory=list[Item])

    def registrar_orden(self, orden: Orden):
        self.id_orden = orden.id_orden
        self.usuario = orden.usuario
        self.direccion_usuario = orden.direccion_usuario
        self.items = orden.items
        self.estado = orden.estado

        # self.agregar_evento(
        #     OrdenRegistrada(id=orden.id, id_orden=orden.id_orden, usuario=orden.usuario, estado=orden.estado))

    def verificar_inventario(self, inventario_bodega: list[InventarioBodega]):
        self.items_bodegas = list(UbicacionItem)
        self.items_centros = list(UbicacionItem)
        self.items_pendientes = list(UbicacionItem)
        for inventario in inventario_bodega:
            for producto in inventario.productos:
                for item in self.items:
                    if producto.descripcion == item and inventario.bodega == CentroDistribucion.__class__:
                        ubicacion_item = UbicacionItem(item=item, direccion=inventario.bodega.direccion)
                        self.items_centros.append(ubicacion_item)
                    elif producto.descripcion == item:
                        ubicacion_item = UbicacionItem(item=item, direccion=inventario.bodega.direccion)
                        self.items_bodegas.append(ubicacion_item)
                    else:
                        ubicacion_item = UbicacionItem(item=item, direccion=Direccion(direccion="No encontrado"))
                        self.items_pendientes.append(ubicacion_item)

        self.agregar_evento(
            OrdenVerificada(id=self.id, id_orden=self.id_orden, usuario=self.usuario,
                            direccion_usuario=self.direccion_usuario, estado=self.estado,
                            items_bodegas=self.items_bodegas, items_centros=self.items_centros))
