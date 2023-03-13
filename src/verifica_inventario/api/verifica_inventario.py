import json

from flask import Response
from flask import request

import verifica_inventario.seedwork.presentacion.api as api
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorOrdenCreadaDTOJson
from verifica_inventario.modulos.infraestructura.despachadores import Despachador
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada, OrdenCreada
from verifica_inventario.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint('verifica-inventario', '/verifica-inventario')


@bp.route('/verificar-orden', methods=('POST',))
def reservar_usando_comando():
    try:
        orden_creada_dict = request.json

        map_orden_creada = MapeadorOrdenCreadaDTOJson()
        orden_creada_dto = map_orden_creada.externo_a_dto(orden_creada_dict)

        orden_creada = OrdenCreada(ordenId=orden_creada_dto.id_orden, user=orden_creada_dto.usuario,
                                   user_address=orden_creada_dto.direccion_usuario, items=orden_creada_dto.items)

        evento = EventoOrdenCreada(eventId=orden_creada_dto.event_id, payload=orden_creada)

        # Se propaga el evento a través del broker para hacerlo asíncrono
        despachador = Despachador()
        despachador.publicar_mensaje(evento, 'eventos-ordenes-creadas')

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
