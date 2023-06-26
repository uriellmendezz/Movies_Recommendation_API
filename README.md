# Proyecto API Recomendación de Peliculas

El objetivo de este proyecto es poder adquirir y consultar información de peliculas a traves de una API. Ademas, el proyecto cuenta con un sistema de recomendación de filmaciones, gracias a un modelo de machine learning que utiliza la puntuacion del coseno de similitud entre las peliculas para recomendar titulos similares al consultado.

La API se despliega en la plataforma Render y permite acceder a diversas funcionalidades relacionadas a caracteristicas del mundo del cine, como por ejemplo obtener los actores que participan en una filmación en especifico, el director tambien

## Índice

- [Introducción](#introducción)
- [Procesos](#procesos)
  - [ETL de datos](#etl-de-datos)
  - [Creación de la API](#creación-de-la-api)
  - [Análisis Exploratorio de Datos (EDA)](#análisis-exploratorio-de-datos-eda)
  - [Creación del modelo de Machine Learning](#creación-del-modelo-de-machine-learning)
- [Requisitos](#requisitos)
- [Uso de la API](#uso-de-la-api)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Introducción

Este proyecto tiene como objetivo proporcionar una API que permita a los usuarios realizar consultas y obtener recomendaciones de películas basadas en diferentes criterios. La API está desplegada en la plataforma Render para facilitar el acceso y la disponibilidad.

## Procesos

El proyecto se ha desarrollado siguiendo una serie de procesos clave:

### ETL de datos

El primer paso fue realizar la extracción, transformación y carga (ETL) de los datos de películas. Se recopilaron datos de diferentes fuentes, como archivos CSV y bases de datos públicas, y se procesaron para crear un conjunto de datos limpio y estructurado.

### Creación de la API

Una vez que se obtuvo el conjunto de datos de películas, se procedió a desarrollar la API utilizando el framework FastAPI en Python. Se crearon endpoints que permiten realizar consultas y obtener respuestas personalizadas basadas en los datos disponibles.

### Análisis Exploratorio de Datos (EDA)

Antes de implementar el modelo de Machine Learning, se realizó un análisis exploratorio de los datos para obtener información relevante sobre las películas y sus características. Se generaron visualizaciones y se realizaron cálculos estadísticos para comprender mejor los datos y tomar decisiones informadas en la creación del modelo.

### Creación del modelo de Machine Learning

Utilizando técnicas de aprendizaje automático, se desarrolló un modelo de recomendación de películas. El modelo utiliza algoritmos avanzados para generar recomendaciones personalizadas basadas en el historial del usuario, las preferencias y otros factores relevantes. El modelo se entrenó con el conjunto de datos y se ajustó para mejorar su rendimiento.

## Requisitos

Antes de ejecutar el proyecto, asegúrese de tener instaladas las siguientes dependencias:

- Python 3.x
- FastAPI
- Pandas
- NumPy
- Scikit-learn

Puede instalar las dependencias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
