# Crearemos el modelo de los datos a aguardar
from pydantic import BaseModel

# Modelo de datos:
class Iris(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str


class Predict(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float