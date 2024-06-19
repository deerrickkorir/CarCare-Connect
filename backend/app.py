from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.category import Category
from models.catalogue import Catalogue
from models.user import User
from models.bought import Bought
from validation_models import CatalogueModel, BoughtModel

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict this based on your requirements
    allow_credentials=True,
    allow_methods=["*"],   # Allow all methods (GET, POST, etc.)
    allow_headers=["*"]    # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/categories')
def categories():
    categories = Category.find_all()
    return categories

@app.get('/catalogue')
def get_catalogues():
    catalogues = Catalogue.find_all()
    return catalogues

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    catalogue = Catalogue(data.name, data.description, data.image, data.booking_fee, data.author, data.category_id, data.date_published)
    catalogue.save()
    return catalogue.to_dict()

@app.post('/bought')
def buy_catalogue(data: BoughtModel):
    user = User.find_one_by_phone(data.phone)
    catalogue = Catalogue.find_one(data.catalogue_id)

    if user:
        bought = Bought(data.bought_from, data.bought_to, catalogue.booking_fee, catalogue.id, user.id)
        bought.save()

        catalogue.is_bought = True
        catalogue.update()

        return {"message": "Purchase successful"}
    else:
        user = User(data.name, data.phone)
        user.save()

        bought = Bought(data.bought_from, data.bought_to, catalogue.booking_fee, catalogue.id, user.id)
        bought.save()

        return {"message": "Purchase successful"}
