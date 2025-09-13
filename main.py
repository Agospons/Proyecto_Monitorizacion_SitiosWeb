from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import engine, Base
from security.error_handeler import ErrorHandler
from starlette.middleware.cors import CORSMiddleware
from routers.usuarios import usuarios_router
from routers.sitios import sitios_routers
from routers.log_chequeos import logeos_routers
from routers.alertas import alertas_routers
from routers.dashboard import dashboard_router

app = FastAPI()
app.title = "Gestion Sitios"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(usuarios_router)
app.include_router(sitios_routers)
app.include_router(logeos_routers)
app.include_router(alertas_routers)
app.include_router(dashboard_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Gestion de sitios web</h1>')

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
