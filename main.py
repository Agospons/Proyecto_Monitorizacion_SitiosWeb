from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import engine, Base
from security.error_handeler import ErrorHandler
from starlette.middleware.cors import CORSMiddleware
#from routers.usuarios import usuariofinal_router

app = FastAPI()
app.title = "proyecto de datos"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

#app.include_router(usuariofinal_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Gestor de cobro</h1>')