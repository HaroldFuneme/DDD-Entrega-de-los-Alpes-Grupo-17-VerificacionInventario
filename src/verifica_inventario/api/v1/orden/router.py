from fastapi import APIRouter, status

from verifica_inventario.api.v1.orden.dto import OrdenCreadaBody
from verifica_inventario.modulos.infraestructura.despachadores import Despachador
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import OrdenCreada, EventoOrdenCreada
from verifica_inventario.seedwork.presentacion.dto import RespuestaAsincrona

router = APIRouter()


@router.post("/verificar", status_code=status.HTTP_202_ACCEPTED, response_model=RespuestaAsincrona)
async def crear_orden(orden_creada: OrdenCreadaBody):
    orden_creada_record = OrdenCreada(ordenId=orden_creada.payload.ordenId, user=orden_creada.payload.user,
                                      user_address=orden_creada.payload.user_address, items=orden_creada.payload.items)
    evento = EventoOrdenCreada(eventId=orden_creada.eventId, payload=orden_creada_record)
    # Se propaga el evento a través del broker para hacerlo asíncrono
    despachador = Despachador()
    despachador.publicar_mensaje(evento, 'eventos-ordenes-creadas')
    return RespuestaAsincrona(mensaje="Verificación de Orden en proceso")
