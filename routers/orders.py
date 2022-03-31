import sys
sys.path.append("..")

from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/order",
    tags=["orders"],
    responses={404: {"description": "Not found"}}
)


models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Order(BaseModel):
    product: str
    price: int
    delivery_address: str
    owner_id : int

@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

# @router.get("/user")
# async def read_all_by_user(user: dict = Depends(get_current_user),
#                            db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     return db.query(models.Todos)\
#         .filter(models.Todos.owner_id == user.get("id"))\
#         .all()
#
# @router.get("/{user_id}")
# async def read_order(user_id: int,
#                     user: dict = Depends(get_current_user),
#                     db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     order_model = db.query(models.Todos)\
#         .filter(models.Todos.owner_id == user_id).first()
#         # .filter(models.Todos.owner_id == user.get("id"))\
#         # .first()
#     if order_model is not None:
#         return order_model
#     raise http_exception()







@router.post("/")
async def create_order(order: Order,
                      #user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # if user is None:
    #     raise get_user_exception()
    order_model = models.Todos()
    order_model.product = order.product
    order_model.price = order.price
    order_model.delivery_address = order.delivery_address
    order_model.owner_id = order.owner_id

    db.add(order_model)
    db.commit()

    return successful_response(201)

@router.put("/{order_id}")
async def update_order(order_id: int,
                      order: Order,
                      #user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # if user is None:
    #     raise get_user_exception()

    order_model = db.query(models.Todos)\
        .filter(models.Todos.order_no == order_id).first()
        # .filter(models.Todos.owner_id == user.get("id"))\
        # .first()

    if order_model is None:
        raise http_exception()

    order_model.product = order.product
    order_model.price = order.price
    order_model.delivery_address = order.delivery_address
    order_model.owner_id = order.owner_id

    db.add(order_model)
    db.commit()

    return successful_response(200)


@router.delete("/{order_id}")
async def delete_order(order_id: int,
                     # user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    # if user is None:
    #     raise get_user_exception()

    order_model = db.query(models.Todos)\
        .filter(models.Todos.order_no == order_id).first()
        # .filter(models.Todos.owner_id == user.get("id"))\
        # .first()

    if order_model is None:
        raise http_exception()

    db.query(models.Todos)\
        .filter(models.Todos.order_no == order_id)\
        .delete()

    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
