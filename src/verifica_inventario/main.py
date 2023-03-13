import asyncio

from fastapi import FastAPI

from verifica_inventario.api.v1.router import router as v1
from verifica_inventario.config.api import app_configs
from verifica_inventario.modulos.infraestructura.consumidores import suscribirse_a_topico
from verifica_inventario.modulos.infraestructura.schema.v1.eventos import EventoOrdenCreada

app = FastAPI(**app_configs)
tasks = list()


@app.on_event("startup")
async def app_startup():
    global tasks
    task1 = asyncio.ensure_future(
        suscribirse_a_topico("eventos-ordenes-creadas", "sub-eventos-ordenes-creadas", EventoOrdenCreada))
    tasks.append(task1)


@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
