from dataclasses import dataclass

from verifica_inventario.modulos.aplicacion.comandos.base import VerificaInventarioBaseHandler
from verifica_inventario.modulos.aplicacion.dto import ItemDTO, OrdenCreadaDTO
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorOrdenCreada
from verifica_inventario.modulos.dominio.entidades import Orden, InventarioBodega, Producto, Bodega, CentroDistribucion
from verifica_inventario.modulos.dominio.objetos_valor import Descripcion, TipoProducto, Direccion, \
    NombreCentroDistribucion
from verifica_inventario.modulos.dominio.repositorios import RepositorioOrdenesCreadas
from verifica_inventario.seedwork.aplicacion.comandos import Comando
from verifica_inventario.seedwork.aplicacion.comandos import ejecutar_commando as comando
from verifica_inventario.seedwork.infraestructura.uow import UnidadTrabajoVerificaInventario


@dataclass
class AgregarOrdenCreada(Comando):
    event_id: str
    id_orden: str
    usuario: str
    direccion_usuario: str
    items: list[ItemDTO]

    def inicializa_estado_comando(self, orden_creada_dto: OrdenCreadaDTO):
        self.event_id = orden_creada_dto.event_id
        self.id_orden = orden_creada_dto.id_orden
        self.usuario = orden_creada_dto.usuario
        self.direccion_usuario = orden_creada_dto.direccion_usuario


def obtener_productos():
    productos = list()
    for i in range(4):
        producto = Producto(descripcion=Descripcion(descripcion=f'item{i}'), tipo_producto=TipoProducto.BIENES_CONSUMO)
        productos.append(producto)
    return productos


def obtener_inventario():
    inventario_eda = list()
    for i in range(3):
        bodega = Bodega(nombre_bodega=f'Bodega {i}',
                        direccion=Direccion(direccion=f'Calle {i} # {i} - {i}'))
        inventario_bodega = InventarioBodega(bodega=bodega, productos=obtener_productos())
        inventario_eda.append(inventario_bodega)

    for i in range(2):
        nombre_centro_dist = NombreCentroDistribucion(nombre=f'Centro de Distribucion {i}')
        centro_distribucion = CentroDistribucion(nombre_centro_distribucion=nombre_centro_dist,
            direccion=Direccion(direccion=f'Carrera {i} # {i} - {i}'))
        inventario_centro_dist = InventarioBodega(bodega=centro_distribucion, productos=obtener_productos())
        inventario_eda.append(inventario_centro_dist)

    return inventario_eda


class AgregarOrdenCreadaHandler(VerificaInventarioBaseHandler):

    def handle(self, comando: AgregarOrdenCreada):
        orden_creada_dto = OrdenCreadaDTO(
            event_id=comando.event_id
            , id_orden=comando.id_orden
            , usuario=comando.usuario
            , direccion_usuario=comando.direccion_usuario
            , items=comando.items)

        # Crea objeto de dominio a partir de objeto de capa de aplicación
        orden: Orden = self.fabrica_verificacion_inventario.crear_objeto(orden_creada_dto,
                                                                         MapeadorOrdenCreada())

        # Se agrega evento de registro/aceptación de la orden
        orden.registrar_orden(orden)
        orden.verificar_inventario(obtener_inventario())

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenesCreadas)

        UnidadTrabajoVerificaInventario.registrar_batch(repositorio.agregar, orden)
        UnidadTrabajoVerificaInventario.commit()


@comando.register(AgregarOrdenCreada)
def ejecutar_comando_crear_reserva(comando: AgregarOrdenCreada):
    handler = AgregarOrdenCreadaHandler()
    handler.handle(comando)
