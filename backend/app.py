from fastapi import FastAPI
from pydantic import BaseModel
from model.catalogue import Category

app = FastAPI()

class CatalogueModel(BaseModel):
    name: str
    description: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/category')
def get_categories():
    categories = Category.find_all()
    return categories

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    category = Category(name=data.name, description=data.description)
    category.save()
    return category.to_dict()
