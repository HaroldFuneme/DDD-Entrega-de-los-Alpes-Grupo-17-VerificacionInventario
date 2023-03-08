""" Fábricas para la creación de objetos del dominio de verificacion de inventario

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de verificacion de inventario

"""

from dataclasses import dataclass

from verifica_inventario.modulos.dominio.entidades import Orden
from verifica_inventario.modulos.dominio.excepciones import TipoObjetoNoExisteEnDominioVerificacionInventarioExcepcion
from verifica_inventario.modulos.dominio.reglas import MinimoUnItem
from verifica_inventario.seedwork.dominio.entidades import Entidad
from verifica_inventario.seedwork.dominio.eventos import EventoDominio
from verifica_inventario.seedwork.dominio.fabricas import Fabrica
from verifica_inventario.seedwork.dominio.repositorios import Mapeador


@dataclass
class _FabricaOrdenCreada(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:
            # Mapea datos de aplicación recibidos desde evento de integración, a Objeto de dominio
            ordenCreada: Orden = mapeador.dto_a_entidad(obj)

            self.validar_regla(MinimoUnItem(ordenCreada.items))

            return ordenCreada


@dataclass
class FabricaVerificacionInventario(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Orden.__class__:
            fabrica_orden_creada = _FabricaOrdenCreada()
            return fabrica_orden_creada.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioVerificacionInventarioExcepcion()
