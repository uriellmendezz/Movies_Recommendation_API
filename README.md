# Proyecto API Recomendación de Películas

El objetivo de este proyecto es poder adquirir y consultar información de peliculas a traves de una API. Esta misma fue desarrollada gracias al framework de FastAPI. Ademas, el proyecto cuenta con un sistema de recomendación de filmaciones, gracias a un modelo de machine learning que utiliza la puntuacion del coseno de similitud entre las peliculas para recomendar titulos similares al requerido.

La API está desplegada en la plataforma Render y ofrece diversas funcionalidades relacionadas con el mundo del cine, como obtener información sobre el elenco/director que participa en una película, a

- **Consultar la cantidad de filmaciones en un mes determinado:** El usuario podra obtener la cantidad histórica de películas estrenadas en un mes específico. La respuesta incluirá el nombre del mes y la cantidad de filmaciones.

- **Consultar la cantidad de filmaciones en un día de la semana determinado:** Adquirir la cantidad histórica de películas estrenadas en un día de la semana específico devolviendo la cantidad total de peliculas que se estrenaron tal dia.

- **Obtener el score de una película por su título:** Conseguir información sobre el título de una película en particular, como por ejemplo el año de estreno y su puntaje de popularidad en el mundo del cine.

- **Obtener información sobre los votos de una película por su título:** Consultar por información detallada sobre los votos de una película en particular como la cantidad de votos recibidos y el valor promedio de las votaciones. Además, si la película tiene menos de 2000 votos, se mostrará un mensaje indicando que no se cumplen las condiciones mínimas de votación.

- **Obtener información sobre un actor específico:** Pedir por detalles sobre un actor en particular que se encuentre en el conjunto de datos, como por ejemplo el nombre del actor, la cantidad de filmaciones en las que ha participado, el retorno total generado por sus películas y el promedio de retorno por película.

- **Obtener información sobre un director específico:** Permite obtener información sobre un director en particular que se encuentre en el conjunto de datos, recibiendo el nombre del director, el retorno total generado por sus películas y detalles de cada película dirigida por él, como el título, el año de lanzamiento, el retorno individual, el costo y la ganancia.

<br>

Además de estas funciones, cabe recalcar que la API también cuenta con un **sistema de recomendación basado en Machine Learning**. De este modo, el usuario podra obtener recomendaciones de películas similares a una película específica. La respuesta incluirá una lista con cinco de las películas más similares a la película de interés.

<br>

*Es importante destacar que los datos disponibles en la API abarcan un período de **146 años**, que va desde peliculas del año 1870 hasta la actualidad. Esto significa que se pueden realizar consultas y obtener información sobre películas en un extenso período de tiempo, brindando un amplio panorama histórico del mundo del cine.*

## Índice

- [Introducción](#introducción)
- [Procesos](#procesos)
  - [Extracción, Transformación y Carga de Datos (ETL)](#extracción-transformación-y-carga-de-datos-etl)
  - [Creación de la API](#creación-de-la-api)
  - [Análisis Exploratorio de Datos (EDA)](#análisis-exploratorio-de-datos-eda)
  - [Creación del Modelo de Machine Learning](#creación-del-modelo-de-machine-learning)
- [Requisitos](#requisitos)
- [Uso de la API](#uso-de-la-api)

## Introducción

Este proyecto es un ejemplo de cómo se pueden combinar los campos de Data Engineering y Machine Learning para crear una API sencilla y potente. La implementación de esta API implica la realización de tareas de data engineering, como la extracción, transformación y carga (ETL) de datos, y también incorpora técnicas de Machine Learning para proporcionar funcionalidades como la recomendación de películas.

La combinación de estas dos disciplinas en esta API permite ofrecer una experiencia rica y completa a los usuarios que la usen. Los procesos de Data Engineering aseguran que los datos estén estructurados y listos para su uso, mientras que las tecnicas de machine learning agregan inteligencia y personalización a través de la recomendación de películas. Esta combinación crea una API que simula como los algoritmos de los servicios de streaming populares como Netflix, Disney+, Amazon Prime y muchos mas funcionan realmente, obviamente a una escala mucho menor computacionalmente pero que en definitiva hace lo mismo.


La etapa de Data Engineering involucró la recopilación de datos de múltiples fuentes, como archivos CSV y bases de datos públicas. Estos datos fueron procesados y transformados para crear un conjunto de datos limpio y estructurado que se puede utilizar para alimentar la API. Además, se realizaron tareas de análisis exploratorio de datos (EDA) para obtener información relevante sobre las películas y sus características. Esto ayudó a comprender mejor los datos y tomar decisiones informadas en la creación del modelo de Machine Learning.

La etapa de Machine Learning fue fundamental para proporcionar la funcionalidad de recomendación de películas. Se utilizó un modelo de machine learning que utilizó un vectorizador para convertir los textos de las películas en representaciones numéricas y luego calculó la similitud coseno entre las películas. Este enfoque permitió generar recomendaciones personalizadas basadas en la similitud entre las películas, brindando a los usuarios sugerencias relevantes y adaptadas a sus preferencias.


## Procesos

El desarrollo de este proyecto involucró varios procesos clave:

### Extracción, Transformación y Carga de Datos (ETL)

El primer paso consistió en realizar el proceso de extracción, transformación y carga (ETL) de los datos de películas. Se recopilaron datos de diferentes fuentes, como archivos CSV y bases de datos públicas. Estos datos se procesaron para crear un conjunto de datos limpio y estructurado.

### Creación de la API

Una vez obtenido el conjunto de datos de películas, se proced