# FastAPI Movie Collection API
Este proyecto es una API construida con FastAPI que permite gestionar una colección de películas. La aplicación utiliza SQLite, SQLAlchemy, Pydantic, y PyJWT para la gestión de base de datos, validación de datos y autenticación respectivamente.

## Características
- Agregar Película: Permite agregar nuevas películas a la colección con la siguiente estructura:
  ````
  class Config:
    schema_extra = {
        "example": {
            "id": 1,
            "title": "Mi película",
            "overview": "Descripción de la película",
            "year": 2022,
            "rating": 9.8,
            "category": "Acción"
        }
    }
  ````
- Listar Películas: Recupera la lista de todas las películas almacenadas en la base de datos.

- Autenticación JWT: Protege ciertos endpoints mediante la autenticación con JSON Web Tokens (JWT).

# Tecnologías Utilizadas
- FastAPI: Framework web rápido para Python.
- SQLite: Motor de base de datos ligero y sin servidor.
- SQLAlchemy: Biblioteca de mapeo objeto-relacional (ORM) para la interacción con la base de datos.
- Pydantic: Facilita la validación de datos y la serialización en la aplicación.
- PyJWT: Implementa la generación y verificación de JSON Web Tokens.

  # Clona este repositorio:

````
git clone https://github.com/ManuelPiano/my-movie-api.git
````
