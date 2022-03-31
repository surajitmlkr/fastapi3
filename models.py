from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String, unique=True, index=True)
    mobile = Column(Integer)
    password = Column(String)


    ordertable = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "ordertable"
    order_no = Column(Integer, primary_key=True, index=True)
    product = Column(String)
    price = Column(Integer)
    delivery_address = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="ordertable")
