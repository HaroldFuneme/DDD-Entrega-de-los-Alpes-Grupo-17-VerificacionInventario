import enum
from typing import List

from verifica_inventario.config.db import db

ordenes_creadas_items = db.Table(
    "ordenes_creadas_items",
    db.Model.metadata,
    db.Column("orden_creada_id", db.String(40), db.ForeignKey("ordenes_creadas.id_orden")),
    db.Column("item_id", db.String(40), db.ForeignKey("items.id")),
)


class OrdenCreada(db.Model):
    __tablename__ = "ordenes_creadas"
    id_orden = db.Column(db.String(40), primary_key=True)
    usuario = db.Column(db.String(30), nullable=True)
    direccion_usuario = db.Column(db.String(100), nullable=True)
    items = db.relationship('Item', secondary=ordenes_creadas_items, backref='ordenes_creadas')
    ubicacion_items = db.relationship("UbicacionItem", back_populates="orden")


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.String(40), primary_key=True)
    descripcion = db.Column(db.String(50), nullable=True)


class TipoAlmacenamiento(enum.Enum):
    BODEGA = 1
    CENTRO_DISTRIBUCION = 2


class Bodega(db.Model):
    __tablename__ = "bodegas"
    id = db.Column(db.String(40), primary_key=True)
    nombre_bodega = db.Column(db.String(40), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.Enum(TipoAlmacenamiento), nullable=False)


class InventarioBodega(db.Model):
    __tablename__ = "inventario_bodega"
    bodega_id = db.Column(db.String(40), db.ForeignKey("bodegas.id"), primary_key=True)
    item_id = db.Column(db.String(40), primary_key=True)
    cantidad_disponible = db.Column(db.Integer, nullable=False)


class UbicacionItem(db.Model):
    item_id = db.Column(db.String(40), primary_key=True)
    orden_id = db.Column(db.String(40), db.ForeignKey("ordenes_creadas.id_orden"), nullable=False)
    bodega_id = db.Column(db.String(40), db.ForeignKey("bodegas.id"), nullable=True)
    bodega = db.relationship("Bodega")
    orden = db.relationship("OrdenCreada", back_populates="ubicacion_items")


class EventosOrden(db.Model):
    __tablename__ = "eventos_orden"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
