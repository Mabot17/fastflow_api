from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from core.router.api_metadata import TITLE_API

routerDocs = APIRouter()

# Swagger UI documentation
@routerDocs.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{TITLE_API} - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@routerDocs.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

# ReDoc documentation
@routerDocs.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{TITLE_API} - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )

# RapiDoc documentation
# render-style="view" -> ini juga cukup bagus mirip swagger
@routerDocs.get("/rapidoc", include_in_schema=False)
async def rapidoc_html():
    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{TITLE_API} - RapiDoc</title>
            <meta charset="utf-8"/>
            <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
        </head>
        <body>
            <rapi-doc 
                spec-url="/openapi.json" 
                theme="light"
                render-style="read"
                show-header="true"
                allow-authentication="true"
                allow-spec-file-download="true"
            ></rapi-doc>
        </body>
        </html>
        """,
        status_code=200
    )
