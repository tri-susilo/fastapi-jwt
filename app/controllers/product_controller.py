from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from datetime import datetime

class ProductController:
    @staticmethod
    def create(db: Session, data: ProductCreate, user_id: int):
        product = Product(**data.dict(), owner_id=user_id)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).filter(Product.is_deleted == False)

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def update(db: Session, product_id: int, data: ProductUpdate, user_id: int):
        product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
        if not product or product.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Product not found")

        for field, value in data.dict().items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: int, user_id: int):
        product = db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()
        if not product or product.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Product not found")

        product.is_deleted = True
        product.deleted_at = datetime.utcnow()
        db.commit()
        return {"message": "Product deleted"}
