from pydantic import BaseModel


class OrdenCreadaPayload(BaseModel):
    ordenId: str
    user: str
    user_address: str
    items: list = []


class OrdenCreadaBody(BaseModel):
    eventId: str
    eventName: str
    eventDataFormat: str
    payload: OrdenCreadaPayload
