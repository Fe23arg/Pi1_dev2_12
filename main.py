# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from fastapi import FastAPI, HTTPException
from pandasql import sqldf
from datetime import datetime

os.environ["OPENBLAS_L2SIZE"]="512k"

app = FastAPI(title = 'Consultas en Plataforma sobre Peliculas')

dft=pd.read_csv('https://raw.githubusercontent.com/Fe23arg/Pi1_12_DEV/main/raw/final_Api_12.csv')
#--------------------------------------------------------------------------------------
@app.get("/")   
def index():
    multi_line_string = """
* Para el correcto funcionamiento de la API se debe considerar lo siguiente:
* Modificar el valor del parámetro introduciendo valores válidos que se encuentren 
* en el Dataset.Respetar siempre la ubicación que cada parámetro como se provee en el código.
"""
    return  multi_line_string

#--------------------------------------------------------------------------------------

@app.get("/contacto")
def contacto():
    return "Email:                / Github: Fe23arg"
 
#--------------------------------------------------------------------------------------
 
@app.get("/peliculas_idioma/{Idioma}")
def peliculas_idioma( Idioma: str ):
  #debe ingresar la abreiatura de idioma ya que estan en una misma denominacion del alfabeto
  cant=0
  for i in range (len(dft["original_language"])):
      if Idioma == dft['original_language'][i]:
          cant=cant +1
  if cant==0:
      return ("Ingreso incorrecto, recuerde escribir todo en minúsculas.")
  else:
      return {'Cantidad de pelicula que fueron estrenadas':cant,' en el Idioma':Idioma}
# ---------------------
# peliculas_idioma('en')
#--------------------------------------------------------------------------------------

@app.get("/peliculas_duracion/{Pelicula}")        
def peliculas_duracion( Pelicula: str ):
#Se ingresa una pelicula. Debe devolver la la duracion y el año.

  for i in range(len(dft["title"])):
      cop=(dft["title"][i])
      if (Pelicula)==cop:
          anio=str(dft["release_year"][i])
          duracion=str(dft["runtime"][i])
          return{' Titulo de la pelicula':Pelicula,' duracion':duracion,' Año de estreno':anio}

#--------------------------------- 
#peliculas_duracion('Jumanji') 
#------------------------------------------------------------------------------------------

@app.get("/franquicia/{Franquicia}")
def franquicia( Franquicia:str ):
  
  ganancia=0
  cant=0
  for i  in range(len(dft)):
      if dft.Franquicia_P[i]==Franquicia:
          cant=cant+1
          ganancia=ganancia+dft.revenue[i]       
  if cant==0:
      return{'Ingreso incorrecto,o pelicula sin franquicia,recuerde respetar mayusculas y minusculas en el nombre'}
  else:
      return{'La franquicia':Franquicia, 'posee peliculas':cant, 'una ganancia total de': ganancia,' y una ganancia promedio de':ganancia/cant}
    
# ---------------------------------------
#franquicia("Toy Story Collection")
#---------------------------------------------------------------------------------------

@app.get("/peliculas_pais/{Pais}")
def peliculas_pais( Pais: str ):
# Se ingresa un país (como están escritos en el dataset, no hay que
# traducirlos!), retornando la cantidad de peliculas producidas en el mismo.
#                   Ejemplo de retorno: Se produjeron X películas en el país X

  cant=0
  for i  in range(len(dft.paises)):

      if type(dft.paises[i])==list:
          for j in dft.paises[i]:
              if j==Pais:
                  cant=cant+1
      else:
          if dft.paises[i]==Pais:
              cant=cant+1

  if cant==0:
      return{'Ingreso incorrecto,recuerde escribir todo en minusculas'}
  else:     
      return{'Se produjeron ':cant,'películas en el país ':Pais}

#----------------------------------------------------
# peliculas_pais('United States of America')
#---------------------------------------------------------------------------------------
       
@app.get("/productoras_exitosas/{Productora}")
def productoras_exitosas( Productora: str ):
#Se ingresa la productora, entregandote el revunue total y la cantidad de
#peliculas que realizo.

  ganancia=0
  band=False
  cant=0
  for i  in range(len(dft.productoras)):

      if type(dft.productoras[i])==list:

          for j in dft.productoras[i]:

              if j==Productora:
                  band=True
                  ganancia=ganancia+dft.revenue[i]
                  cant=cant+1
      else:
          if dft.productoras[i]==Productora:
              band=True
              ganancia=ganancia+dft.revenue[i]
              cant=cant+1
  if band==False:
      return{' Ingreso incorrecto,recuerde diferenciar mayuscula y minusculas'}
  else:
      return{' La productora: ':Productora,' revenue_total ':ganancia,'cantidad':str(cant)}
#------------------------------------
#productoras_exitosas('Warner Bros.') 
#----------------------------------------------------------------------------------------     
@app.get("/get_director/{nombre_director}")
def get_director( nombre_director:str ):
# Se ingresa el nombre de un director que se encuentre dentro de un dataset
# debiendo devolver el éxito del mismo medido a través del retorno. Además,
# deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno
# individual, costo y ganancia de la misma.  
  li=[]
  resu=''
  acum=0
  band=True
  for i in range(len(dft.directores)):
      
      if type(dft.directores[i])==list:
          #nom_dir=dft.directores[i]
          for  n in dft.directores[i]:
              if nombre_director == n:
                  band=True
                  tit=dft["title"][i]
                  fec=dft["release_year"][i]
                  costo=dft["budget"][i]
                  ganancia=dft['revenue'][i]
                  acum=acum+(ganancia-costo)
                  ret=ganancia-costo
                  resu='director: '+str(nombre_director)+'  retorno_total_director: '+str(acum)+'  pelicula: '+str(tit)+'  anio: '+str(fec)+'  retorno_pelicula: '+str(ret)+'  budget_pelicula: '+str(costo)+' revenue_pelicula: '+str(ganancia)
                  li.append(resu)
         
      else:
          if nombre_director == dft.directores[i]:
                  band=True
                  tit=dft["title"][i]
                  fec=dft["release_year"][i]
                  costo=dft["budget"][i]
                  ganancia=dft['revenue'][i]
                  acum=acum+(ganancia-costo)
                  ret=ganancia-costo
                  resu='director: '+str(nombre_director)+'  retorno_total_director: '+str(acum)+'  pelicula: '+str(tit)+'  anio: '+str(fec)+'  retorno_pelicula: '+str(ret)+'  budget_pelicula: '+str(costo)+' revenue_pelicula: '+str(ganancia)
                  li.append(resu)
  if band==False:
      return{' Ingreso incorrecto,Recuerde diferenciar mayuscula y minusculas'}
  else:
      return{'lista':li}             
 

# -------------------------------------
# get_director('Forest Whitaker')
# get_director('Michelle Danner')
#----------------------------------------------------------------------------------------
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo:str):
  
   #Usamos solo la primeras 15000 filas para el modelo por recurso dispobles de calculo
  movieRatings = dft[0:5000].pivot_table(index=['id'],columns=['title'],values='vote_average') 
  
  titu_df = movieRatings[titulo]

  # Correlamos el resto de peliculas (columnas) con la seleccionada (Jumanji)  
  similarMovies = movieRatings.corrwith(titu_df)  
  similarMovies = similarMovies.dropna()  
  df = pd.DataFrame(similarMovies)

  # Las ordenamos por el valor de score que hemos generado, de forma descendente  
  similarMovies.sort_values(ascending=False)  

  # agregamos por titulo y devolvemos el  
  # numero de veces que se puntuo, y la media de puntuacion  
  movieStats = dft[0:5000].groupby('title').agg({'vote_average': [np.size, np.mean]})

  # nos quedamos con todas las que tengan mas de 3 puntuaciones  
  # de distintos usuarios  
  popularMovies = movieStats['vote_average']['size'] >= 2
   
  # ordenamos por la puntuación asignada  
  movieStats[popularMovies].sort_values([('vote_average', 'mean')], ascending=False)[:15] 
  # tambien de esta forma se puede dff=pd.merge(peliculasVotadas[peliculasPopulares],dfff ,how='outer',on='title')
  # hacemos el join  
  df = movieStats[popularMovies].join(pd.DataFrame(similarMovies, columns=['similarity']))
 
  # Ordenamos el dataframe por similaridad, y vemos los primeros 5 resultados  
  df.sort_values(['similarity'], ascending=False)[:5]  

  dff=df.sort_values(['similarity'], ascending=False)[:5] 
  li=[]
  lista=''
  fx=dff.index
  i=0
  for x in fx:
    i=i+1
    lista=lista+x+' , ' 
    li.append(x)
  
  dfg=pd.Series(li)
    
     
  return {'recomendadas por prioridad descendente':dfg}