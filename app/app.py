from fastapi import FastAPI
from . import models, db, routers

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="Tron Wallet Service")
app.include_router(routers.router)
