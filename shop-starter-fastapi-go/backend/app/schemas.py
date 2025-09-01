from pydantic import BaseModel, Field
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    slug: str

class CategoryRead(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    slug: str
    description: str = ""
    price: float
    in_stock: bool = True
    category_id: Optional[int] = None

class ProductRead(ProductBase):
    id: int
    category: Optional[CategoryRead] = None
    class Config:
        from_attributes = True

class CurtainVariantBase(BaseModel):
    name: str
    material: str
    width_cm: int
    height_cm: int
    price: float
    in_stock: bool = True

class CurtainVariantRead(CurtainVariantBase):
    id: int
    class Config:
        from_attributes = True

# Pricing quote schemas
class QuoteRequest(BaseModel):
    width_cm: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    material: str  # "pvc" or "mesh"
    magnet_spacing_cm: float | None = None

class QuoteResponse(BaseModel):
    total_price: float
    area_sqm: float
    material_rate_per_sqm: float
    magnet_count: int
    magnet_unit_price: float
    magnets_cost: float
    notes: str | None = None
