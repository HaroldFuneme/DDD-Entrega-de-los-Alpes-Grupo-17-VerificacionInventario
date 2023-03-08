from verifica_inventario.modulos.dominio.objetos_valor import Item
from verifica_inventario.seedwork.dominio.reglas import ReglaNegocio


class MinimoUnItem(ReglaNegocio):
    items: list[Item]

    def __init__(self, items, mensaje='La orden debe tener al menos un item'):
        super().__init__(mensaje)
        self.items = items

    def es_valido(self) -> bool:
        return len(self.items) > 0 and isinstance(self.items[0], Item)
