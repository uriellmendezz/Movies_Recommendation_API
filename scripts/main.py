import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')
import datetime
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

meses_1 = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
meses_2 = [mes.upper() for mes in meses_1]
meses_3 = [mes.capitalize() for mes in meses_1]
meses = meses_1 + meses_2 + meses_3

meses_numeros = [numero for numero in range(1,13)]
meses_numeros = meses_numeros * 3

data = pd.read_csv('../final_data/combined_data.csv',sep=',')
cast = pd.read_csv('../final_data/final_cast.csv')

app = FastAPI()

@app.get('/')
def home():
    return {'mensaje':'Movie Recommendation API'}

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    if mes not in meses:
        return {'mensaje':'Ingresar un mes en idioma Español'}
    else:
        mes_index = meses.index(mes)
        mes_numero = meses_numeros[mes_index]
        
        cantidad_xmes = float(data['movie_id'].loc[data.release_month == mes_numero].count())
        data_json = {'mes':mes,'cantidad_fimaciones_mes':cantidad_xmes}

        json_str = json.dumps(data_json, indent=4, default=str)
        return Response(content=json_str, media_type='application/json')

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    dia = int(dia)
    dias = [dia for dia in range(1,32)]
    if dia not in dias:
        data_json = {'dia':dia, 'cantidad_filmaciones_dia':0}
    
    else:
        cantidad_xdia = data.movie_id.loc[data.release_day == dia].count()
        data_json = {'dia':dia, 'cantidad_filmaciones_dia':int(cantidad_xdia)}

    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
                        

@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    filmaciones = list(data.title.unique())
    if titulo not in filmaciones:
        data_json = {'titulo':'No se encuentra la pelicula en la base de datos'}
    else:
        movie_index = data.loc[data.title == titulo].index
        movie_year = data.release_year.iloc[movie_index]
        movie_score = data.popularity.iloc[movie_index]

        if pd.isna(movie_year).any():
            movie_year = 'Desconocido'
        else:
            movie_year = int(movie_year)

        if pd.isna(movie_score).any():
            movie_score = 'Desconocido'
        else:
            movie_score = float(movie_score)

        data_json = {'titulo':titulo,
                    'anio':movie_year,
                    'popularity':movie_score}

    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    filmaciones = list(data.title.unique())
    if titulo not in filmaciones:
        data_json = {'titulo': 'Movie not found'}
    else:
        movie_index = data.loc[data.title == titulo].index
        movie_year = data.release_year.iloc[movie_index].item() if pd.notna(data.release_year.iloc[movie_index]).any() else 'Desconocido'
        movie_vote_count = data.vote_count.iloc[movie_index].item() if pd.notna(data.vote_count.iloc[movie_index]).any() else 'Desconocido'
        movie_vote_average = data.vote_average.iloc[movie_index].item() if pd.notna(data.vote_average.iloc[movie_index]).any() else 'Desconocido'

        if pd.notna(movie_vote_count) and int(movie_vote_count) < 2000:
            movie_vote_count = 'Insuficientes votos'
            movie_vote_average = 'Insuficientes votos'
            mensaje = 'Este titulo tiene menos de 2000 votos'

        data_json = {
            'titulo': titulo,
            'anio': int(movie_year) if isinstance(movie_year, float) else movie_year,
            'votos': int(movie_vote_count) if isinstance(movie_vote_count, float) else movie_vote_count,
            'valoracion_promedio': float(movie_vote_average) if isinstance(movie_vote_average, float) else movie_vote_average,
            'mensaje': mensaje if 'mensaje' in locals() else None}
        
    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')
    
    

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    all_actors = list(cast.name.unique())

    if nombre_actor not in all_actors:
        data_json = {'mensaje':'Actor not found'}
    else:
        cantidad_titulos_actor = int(data.movie_id.loc[data.actors.fillna('').str.contains(nombre_actor)].count())
        retorno_actor = float(data['return'].loc[data.actors.fillna('').str.contains(nombre_actor)].sum())
        promedio_x_pelicula = retorno_actor / cantidad_titulos_actor

        data_json = {'actor':nombre_actor,
                'cantidad_filmaciones':cantidad_titulos_actor,
                'retorno_total_del_actor':retorno_actor,
                'promedio_de_retorno_por_pelicula':promedio_x_pelicula}
    
    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    
    if nombre_director not in data.director.unique():
        data_json = {'mensaje':'Director no encontrado en la base de datos'}
    else:
        retorno_total_director = data['return'].loc[data.director == nombre_director].sum()
        movies_indexes = data.title.loc[data.director == nombre_director].index
        movies_data = []
        for index in movies_indexes:
            movie_title = data.title.iloc[index]
            movie_release_year = data.release_year.iloc[index]
            movie_return = data['return'].iloc[index]
            movie_budget = data.budget.iloc[index]
            movie_revenue = data.revenue.iloc[index]

            info = {'title':movie_title,
                    'release_year':movie_release_year,
                    'return':movie_return,
                    'budget':movie_budget,
                    'revenue':movie_revenue}
            movies_data.append(info)
            
        data_json = {'director':nombre_director,
                'retorno_total_director':retorno_total_director,
                'peliculas':movies_data}
    
    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    return {'lista recomendada': respuesta}

