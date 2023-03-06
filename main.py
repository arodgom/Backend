from fastapi import FastAPI, status, Response
import pandas as pd
import json
import csv
from models import Iris, Predict
import pickle
import settings

app = FastAPI()



@app.get('/')
async def test():
    return "Bienvenido a FastAPI"


# Método GET a la url "/iris/"
# llamaremos a nuestra aplicación (<app name> + <método permitido>)
@app.get('/iris/')
async def iris(response:Response):
    try:
        # Crear un dataframe con la información de Iris:
        df = pd.read_csv(settings.MEDIA_ROOT)
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
    with open(settings.MEDIA_ROOT, "a", newline="") as csvfile:
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


# PUT actualizar la última línea del csv
# Método PUT a la url "/updateData/" + ID a modificar
@app.put("/updateData/{item_id}")
async def updataData(item_id: int, item:Iris):
    # Leer el csv con ayuda de pandas:
    df = pd.read_csv(settings.MEDIA_ROOT)
    # Modificamos el último dato con los valores que nos lleguen
    df.loc[df.index[-1], "sepal_length"] = item.sepal_length
    df.loc[df.index[-1], "sepal_width"] = item.sepal_width
    df.loc[df.index[-1], "petal_length"] = item.petal_length
    df.loc[df.index[-1], "petal_width"] = item.petal_width
    df.loc[df.index[-1], "species"] = item.species
    
    # convertir a csv
    df.to_csv(settings.MEDIA_ROOT, index=False)
    # retornamos el id que hemos modificado y el dato en formato diccionario
    return {"item_id": item_id, **item.dict()}

# POST realizamos la predicción
# Método POST a la url "/prediccion/"
@app.post("/prediccion/", status_code=201)
async def predict(item: Predict):
    pickle_model = pickle.load(open(settings.MEDIA_MODEL, 'rb'))
    result = pickle_model.predict([[item.sepal_length, item.sepal_width,
                                    item.petal_length, item.petal_width]])
    iris = {"Setosa": 0, "Versicolor": 1, "Virginica": 2}
    for key, value in iris.items():
        if value == result[0].item():
            return  key


# DELETE eliminar la última línea del csv
# Método Delete a la url "/deleteData/" + id
@app.delete("/deleteData/{item_id}")
async def deleteData(item_id: int):
    # Leer el csv
    df = pd.read_csv(settings.MEDIA_ROOT)
    # Eliminar la última fila
    df.drop(df.index[-1], inplace=True)
    # Convertir a csv
    df.to_csv(settings.MEDIA_ROOT, index=False)
    return {"item_id": item_id, "msg": "Eliminado"}