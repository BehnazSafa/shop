from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.get("/curtains/standard", response_model=list[schemas.CurtainVariantRead])
def list_curtains(db: Session = Depends(get_db)):
    return db.query(models.CurtainVariant).all()


@router.get("/{slug}", response_model=schemas.ProductRead)
def get_product(slug: str, db: Session = Depends(get_db)):
    obj = db.query(models.Product).filter(models.Product.slug == slug).first()
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj
