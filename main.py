from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title = "Mi api"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] | None
    title: str
    overview: str
    rating: float
    category: str

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
        'title': 'Spider-Man',
        'overview': 'A man is bitten by a spider...',
        'rating': '8',
        'category': 'Action'
    },
     {
        'id': 2,
        'title': 'The Enigma Code',
        'overview': 'The story of Alan Turing...',
        'rating': '10',
        'category': 'Drama'
    },
     {
        'id': 3,
        'title': 'The IT Crowd',
        'overview': '2 funny nerds in a company...',
        'rating': '10',
        'category': 'Comedy'
    }
]


@app.get('/movies/', tags=['movies'], response_model=dict,status_code=200)
def get_movies_by_id(id: int = Query(ge=1,le=2000)) -> dict:
    for movie in movies:
        if movie['id'] == id:
            return JSONResponse(content=movie,status_code=200)
        else:
            return JSONResponse(status_code=404, content={'message':'Movie not found'})

@app.post('/movies', tags=['movies'],response_model=dict, status_code=201)
def create_movie(movie: Movie) ->dict:  
    movies.append(movie)
    return JSONResponse(content={'message': 'The movie has been registrated'}, status_code=201)

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
            return JSONResponse(content={'message':'Movie not found'},status_code=404)

@app.delete('/movies/', status_code=200, tags=['movies'])
def delete_movie(id:int = Query(ge=1,le=2000)):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content=movies, status_code=200)
        else:
            return JSONResponse(content={'message': 'Movie not found'}, status_code=404)
                                
