from pydantic import BaseModel

class CatalogueModel(BaseModel):
    name: str
    description: str
    image: str
    supplie: str
    price: int
    
class BoughtModel(BaseModel):
    name: str
    phone: str
    bought_from: str
    bought_to: str
    catalogue_id: int