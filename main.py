from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import errorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)
app.add_middleware(errorHandler)
app.include_router(movie_router)
app.include_router(user_router)


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

