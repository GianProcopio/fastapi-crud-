from fastapi import FastAPI, Query, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Text,List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi api"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "gian@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] | None
    title: str = Field(min_length=5, max_length=20)
    overview: Text
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=6, max_length=10)

    class Config:
        schema_extra = {
           'example': {
            'id': 1,
            'title': 'My movie',
            'overview': 'Some description...',
            'rating': 7.5,
            'category':'Action'            
        }
    }

movies = [
    {
        'id': 1,
        'title': 'My movie',
        'overview': 'Some description...',
        'rating': 7.5,
        'category':'Action' 
    }
]

@app.get('/', tags=['home'])
def greeting():
    return HTMLResponse('<h1>Hola mundo!</h1>')

#Login
@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == 'gian@gmail.com' and user.password == '1234':
        token = create_token(user.dict())
        return JSONResponse(content=token,status_code=201)
    else: raise HTTPException(status_code=401,detail='Incorrect email or password')         

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() ->List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/', tags=['movies'], response_model=dict ,status_code=200)
def get_movies_by_id(id: int = Query(ge=1,le=2000)) -> dict:
    for movie in movies:
        if movie['id'] == id:
            return JSONResponse(content=movie,status_code=200)
        else:
            return JSONResponse(status_code=404, content={'message':'Movie not found'})

@app.post('/movies', tags=['movies'],response_model=dict, status_code=201)
def create_movie(movie: Movie) ->dict:  
    movies.append(movie.dict())
    return JSONResponse(content=movies, status_code=201)

@app.put('/movies/', tags=['movies'], response_model=dict, status_code=200)
def update_movie(movie:Movie,id:int = Query(ge=1,le=2000)) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content=movies, status_code=200)
        else:
            raise HTTPException(status_code=404, detail='Movie not found')

@app.delete('/movies/', status_code=200, tags=['movies'])
def delete_movie(id:int = Query(ge=1,le=2000)):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content=movies, status_code=200)
        else:
            raise HTTPException(status_code=404, detail='Movie not found')
                                






