from fastapi import APIRouter, Query, Path, Depends
from typing import Optional, List
from config.database import Sesion
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JwtBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from services.movie import Movie_Service



movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies() -> List[Movie]:
    db = Sesion()
    result = Movie_Service(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Sesion()
    result = Movie_Service(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Sesion()
    result = Movie_Service(db).get_movies_by_category(category)
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201, dependencies=[Depends(JwtBearer())])
def create_movie(movie: Movie) -> dict:
    db = Sesion()
    Movie_Service(db).create_movie(MovieModel(**movie.dict()))
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JwtBearer())])
def update_movie(id: int, movie: Movie)-> dict:
    db = Sesion()
    result = Movie_Service(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    Movie_Service(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha actualizado la película"})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JwtBearer())])
def delete_movie(id: int)-> dict:
    db = Sesion()
    result = Movie_Service(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    Movie_Service(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})