from fastapi import FastAPI, status, Response
import pandas as pd
import json
import csv
from models import Iris

app = FastAPI()

MEDIA_ROOT = "./media/iris.csv"

@app.get('/')
async def test():
    return "Bienvenido a FastAPI"


# Método GET a la url "/iris/"
# llamaremos a nuestra aplicación (<app name> + <método permitido>)
@app.get('/iris/')
async def iris(response:Response):
    try:
        # Crear un dataframe con la información de Iris:
        df = pd.read_csv(MEDIA_ROOT)
        # print(df)
        # lo transformamos a json para poder gestionarlo desde el front:
        data = df.to_json(orient="index")
        # cargar la infromación con formato json:
        data = json.loads(data)
        return data    
    except Exception as e:
        print("Error al cargar el csv %s" % str(e))
        response.status_code = status.HTTP_404_NOT_FOUND
        return "404 NOT FOUND"        

    
# POST de insertar un nuevo dato en el csv, última línea
# Método POST a la url "/insertData/"
@app.post("/insertData/", status_code=201)
async def insert(item:Iris):
    with open(MEDIA_ROOT, "a", newline="") as csvfile:
        # Nombres de los campos:
        fieldnames = ['sepal_length','sepal_width',
                      'petal_length','petal_width',
                      'species']
        # escribimos el csv:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # insertar los valores en la ultima fila:
        writer.writerow({'sepal_length': item.sepal_length, 
                         'sepal_width': item.sepal_width,
                         'petal_length': item.petal_length,
                         'petal_width': item.petal_width,
                         'species': item.species})
        return item

# TODO: PUT actualizar la última línea del csv
# TODO: DELETE eliminar la última línea del csv