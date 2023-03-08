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


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.String(40), primary_key=True)
    descripcion = db.Column(db.String(50), nullable=True)


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
