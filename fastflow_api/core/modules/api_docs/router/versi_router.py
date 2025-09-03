from fastapi import APIRouter
from core.router.api_metadata import VERSI_API

routerVersi = APIRouter(tags=["Version"])


@routerVersi.get("/", include_in_schema=False)
@routerVersi.get("/version")
async def versi():
    return {"version": VERSI_API}
