from verifica_inventario.modulos.dominio.fabricas import FabricaVerificacionInventario
from verifica_inventario.modulos.infraestructura.fabricas import FabricaRepositorio
from verifica_inventario.seedwork.aplicacion.comandos import ComandoHandler, Comando


class VerificaInventarioBaseHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_verificacion_inventario: FabricaVerificacionInventario = FabricaVerificacionInventario()

    def handle(self, comando: Comando):
        pass

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_verificacion_inventario(self):
        return self._fabrica_verificacion_inventario
