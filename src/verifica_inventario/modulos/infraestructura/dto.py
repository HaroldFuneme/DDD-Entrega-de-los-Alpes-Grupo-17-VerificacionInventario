from sqlalchemy import Table, Column, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship

from verifica_inventario.config.db import Base

ordenes_creadas_items = Table(
    "ordenes_creadas_items",
    Base.metadata,
    Column("orden_creada_id", String(40), ForeignKey("ordenes_creadas.id_orden")),
    Column("item_id", String(40), ForeignKey("items.id")),
)


class OrdenCreada(Base):
    __tablename__ = "ordenes_creadas"
    id_orden = Column(String(40), primary_key=True)
    usuario = Column(String(30), nullable=True)
    direccion_usuario = Column(String(100), nullable=True)
    items = relationship('Item', secondary=ordenes_creadas_items, backref='ordenes_creadas')


class Item(Base):
    __tablename__ = "items"
    id = Column(String(40), primary_key=True)
    descripcion = Column(String(50), nullable=True)


class EventosOrden(Base):
    __tablename__ = "eventos_orden"
    id = Column(String(40), primary_key=True)
    id_entidad = Column(String(40), nullable=False)
    fecha_evento = Column(DateTime, nullable=False)
    version = Column(String(10), nullable=False)
    tipo_evento = Column(String(100), nullable=False)
    formato_contenido = Column(String(10), nullable=False)
    nombre_servicio = Column(String(40), nullable=False)
    contenido = Column(Text, nullable=False)
