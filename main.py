from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, orders
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(orders.router)