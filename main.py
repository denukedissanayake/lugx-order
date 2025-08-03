from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Order
from database import engine, SessionLocal
from pydantic import BaseModel

app = FastAPI(root_path="/order")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OrderCreate(BaseModel):
    item_name: str
    quantity: int

@app.get("/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

@app.post("/")
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(item_name=order.item_name, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

