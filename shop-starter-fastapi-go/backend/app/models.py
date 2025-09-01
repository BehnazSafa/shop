from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    price = Column(Float, nullable=False)  # base price for ready-made items
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

class CurtainVariant(Base):
    """
    Ready-made curtain sizes with fixed prices.
    """
    __tablename__ = "curtain_variants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "90x210 Mesh"
    material = Column(String, nullable=False)  # "pvc" or "mesh"
    width_cm = Column(Integer, nullable=False)
    height_cm = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
