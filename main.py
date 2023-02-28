from fastapi import FastAPI, status, Response
import pandas as pd
import json
import csv
from models import Iris

app = FastAPI() # primera app con fastapi

MEDIA_ROOT = "iris.csv"

@app.get('/')
async def test():
    return "Bienvenido a FastAPI"


# Método GET a la URL "/iris/"
# llamaremos a nuestra aplicación (app name + método permitido)
@app.get('/iris/')
async def iris(response:Response):
    try:
        # Crear un dataframe con la información de Iris
        df = pd.read_csv(MEDIA_ROOT)
        print(df)
        # lo transformamos a json para poder getsionarlo desde el front
        data = df.to_json(orient="index")
        # cargar la info con formato json:
        data = json.loads(data)
        return data
    
    except Exception as e:
        print("Error al cargar el csv %s" % str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return "404 NOT FOUND"
    
# TODO: POST de insertar un nuevo dato en el csv
# metodo post a la url "isertData/"
@app.post("/insertData", status_code=201)
async def insertData(item:Iris)
    with open(MEDIA_ROOT, "a", newline="") as csvfile:
        # nombres de los campos:
        fieldnames = ['sepal_length' Sepal_Length: float
Sepal_Width: float
Setal_Length: float
Petal_Width: float
Species: str]
        write = csv_DictWriter(csvfile, fieldnames=fieldnames)
        #insertar los valores en la última fila
        writer.writerow('sepal_length': item.sepal_length)
        




# TODO: PUT actualizar la última linea del csv
# TODO: DELETE eliminar la últma linea del csv
