import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')
import datetime
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
app = FastAPI()

meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
dias_es = ['lunes', 'martes', 'miercoles', 'jueves','viernes','sabado','domingo',"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
dias_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Datasets
data = pd.read_csv('final_data/combined_data.csv',sep=',')
cast = pd.read_csv('final_data/final_cast.csv')

movies = data[['title','genres','director']]
movies = movies.dropna(subset=['genres']) # Elimino las peliculas que tienen vacio el campo de 'genres'

data.release_date = data.release_date.apply(lambda x: pd.to_datetime(x).date() if '-' in x else x)
data['release_weekday']= data.release_date.apply(lambda x: x.strftime('%A') if type(x) == datetime.date else np.nan)

@app.get('/')
def home():
    return {'mensaje':'Movie Recommendation API'}

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    if mes.lower() not in meses:
        return {'mensaje':'Ingresar un mes en idioma Español'}
    else:
        mes_numero = meses.index(mes)
        
        cantidad_xmes = float(data['movie_id'].loc[data.release_month == mes_numero].count())
        data_json = {'mes':mes,'cantidad_fimaciones_mes':cantidad_xmes}

        json_str = json.dumps(data_json, indent=4, default=str)
        return Response(content=json_str, media_type='application/json')

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    dia = dia.lower()
    if dia not in dias_es:
        data_json = {'mensaje':'Se requiere de un dia de la semana en idioma Espaniol (Spanish)'}
 
    else:
        dia_index = dias_es.index(dia)
        cantidad_xdia = data.movie_id.loc[data.release_weekday == dias_en[dia_index]].count()
        data_json = {'dia':dia.capitalize(), 'cantidad_filmaciones_dia':int(cantidad_xdia)}

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
from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

movies['genres'] = movies['genres'].str.replace('|',' ')
movies['joined_data'] = movies[['title','genres','director']].astype(str).apply(' '.join, axis=1)

vectorizer = TfidfVectorizer(stop_words='english') # Elimino las palabras mas comunes del ingles

@app.get('/recomendacion/{title}')
def recomendacion(title):
    """Get the recommendation for a given title"""
    # Obtengo los géneros de la pelicula
    if title not in movies.title.unique():
        data_json = {'mensaje':'Pelicula no encontrada'}
    else:
        # Obtengo los géneros de la pelicula
        movie_genres = movies['genres'].loc[movies['title'] == title]
        #movie_genres = movie_genres.values[pd.isna(movie_genres.values) == False].item()
        movie_genres = sorted(movie_genres, key= lambda x: len(x), reverse=True) # Ordenar los géneros en función del len()


        # Separo los generos en una lista
        #genres = [v.split(' ') for v in movie_genres if isinstance(v,str)]

        # Filtro el dataframe con las peliculas que tengan los mismos géneros que la pelicula de interes
        # y con las peliculas que tengan en su titulo el nombre de la pelicula de interes
        similar_movies = movies.loc[(movies.genres.fillna(' ').str.contains(movie_genres[0])) | (movies.title.str.contains(title))].reset_index(drop=True)
        max_len = 3500
        if len(similar_movies) > max_len:
            similar_movies = similar_movies.sort_values(by='popularity', ascending=False).reset_index(drop=True)[:max_len]

        # Obtengo el indice en el dataframe filtrado de la pelicula de interes
        movie_index = similar_movies.loc[similar_movies['title'] == title].index
        if len(movie_index) == 0:
            similar_movies = similar_movies.append(movies.loc[movies.title == title]).reset_index(drop=True)
            movie_index = similar_movies.loc[similar_movies['title'] == title].index

        # Vectorizo los datos
        data_matrix = vectorizer.fit_transform(similar_movies.joined_data)
        # Genero la matriz de puntuación de similitud entre las peliculas
        similarity_matrix = cosine_similarity(data_matrix,data_matrix)

        sim_movies = list(enumerate(similarity_matrix[movie_index[0]]))
        sim_movies = sorted(sim_movies, key=lambda x: x[1], reverse=True)
        top_similar_movies = [similar_movies.loc[i, 'title'] for i, _ in sim_movies[1:20] if similar_movies.loc[i, 'title'] != title][:5]
        data_json = {'similar_movies':top_similar_movies}

    json_str = json.dumps(data_json, indent=4, default=str)
    return Response(content=json_str, media_type='application/json')


# --------------------------
# Otra manera para el modelo:
"""
movie_genres = movies['genres'].loc[movies['title'] == title]

# Separo los generos en una lista
genres = [v.split(' ') for v in movie_genres if isinstance(v,str)]

# Filtro el dataframe con las peliculas que tengan los mismos géneros que la pelicula de interes
# y con las peliculas que tengan en su titulo el nombre de la pelicula de interes
similar_movies = movies.loc[movies.genres.fillna(' ').str.contains(movie_genres.values[0]) | movies.title.str.contains(title)].reset_index(drop=True)

# Vectorizo los datos
data_matrix = vectorizer.fit_transform(similar_movies.joined_data)
# Genero la matriz de puntuación de similitud entre las peliculas
similarity_matrix = cosine_similarity(data_matrix,data_matrix)

# Obtengo el indice en el dataframe filtrado de la pelicula de interes
movie_index = similar_movies.loc[similar_movies['title'] == title].index 

sim_movies = list(enumerate(similarity_matrix[movie_index[0]]))
sim_movies = sorted(sim_movies, key=lambda x: x[1], reverse=True)
top_similar_movies = [similar_movies.loc[i, 'title'] for i, _ in sim_movies[1:20] if similar_movies.loc[i, 'title'] != title][:5]
data_json = {'similar_movies':top_similar_movies}
"""