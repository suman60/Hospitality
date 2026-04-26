from fastapi import FastAPI
from . import models
from .database import engine
from .routers import transactions, analytics
from app.routers import auth
# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospitality Analytics Platform")

# Include the routes from our routers folder
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hospitality Analytics API"}