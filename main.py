from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Sesion, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JwtBearer(HTTPBearer):
     async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['username'] != "admin":
            raise HTTPException(status_code=403, detail="Credenciales inválidas")
        
        
     


class user(BaseModel):
    username: str
    password: str


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

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: user):
     if user.username == "admin" and user.password == "admin":
         token: str = create_token(user.dict())
         return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies() -> List[Movie]:
    db = Sesion()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie, dependencies=[Depends(JwtBearer())])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Sesion()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Sesion()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
         return JSONResponse(status_code=404, content={"message": "No se ha encontrado la película"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201, dependencies=[Depends(JwtBearer())])
def create_movie(movie: Movie) -> dict:
    db = Sesion()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JwtBearer())])
def update_movie(id: int, movie: Movie)-> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200, dependencies=[Depends(JwtBearer())])
def delete_movie(id: int)-> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})