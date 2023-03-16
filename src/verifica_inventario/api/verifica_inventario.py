import json
import os

from flask import Response
from flask import request

import verifica_inventario.seedwork.presentacion.api as api
from verifica_inventario.modulos.aplicacion.mapeadores import MapeadorOrdenCreadaDTOJson
from verifica_inventario.modulos.infraestructura.despachadores import Despachador
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada, OrdenCreada, \
    InventarioVerificadoCompensacion, InventarioVerificadoPayload
from verifica_inventario.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint('verifica-inventario', '/verifica-inventario')


@bp.route('/verificar-orden', methods=('POST',))
def verificar_orden():
    try:
        orden_creada_dict = request.json

        orden_creada_dto = MapeadorOrdenCreadaDTOJson().externo_a_dto(orden_creada_dict)

        orden_creada = OrdenCreada(ordenId=orden_creada_dto.id_orden, user=orden_creada_dto.usuario,
                                   user_address=orden_creada_dto.direccion_usuario, items=orden_creada_dto.items)

        evento = EventoOrdenCreada(eventId=orden_creada_dto.event_id, payload=orden_creada)

        # Se propaga el evento a través del broker para hacerlo asíncrono
        topico_eventos_orden = os.getenv('TOPICO_EVENTOS_ORDEN', default="evento-orden-a")
        despachador = Despachador()
        despachador.publicar_mensaje(evento, topico_eventos_orden)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/verificar-orden-compensacion', methods=('POST',))
def compensar_orden_verificada():
    try:
        orden_creada_dict = request.json

        orden_creada_dto = MapeadorOrdenCreadaDTOJson().externo_a_dto(orden_creada_dict)

        orden_verificada = InventarioVerificadoPayload(ordenId=orden_creada_dto.id_orden,
                                                       user=orden_creada_dto.usuario,
                                                       user_address=orden_creada_dto.direccion_usuario,
                                                       items_bodegas=list(),
                                                       items_centros=list(),
                                                       items_pendientes=list())

        evento = InventarioVerificadoCompensacion(eventId=orden_creada_dto.event_id, payload=orden_verificada)

        # Se propaga el evento a través del broker para hacerlo asíncrono
        topico_eventos_orden = os.getenv('TOPICO_COMANDOS', default="verifica-inventario-compensacion")
        despachador = Despachador()
        despachador.publicar_mensaje(evento, topico_eventos_orden)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
