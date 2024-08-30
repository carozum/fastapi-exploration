from fastapi import FastAPI
import models
from database import engine
from routers import books, readers, loans
from auth import authentication

from routers import books, readers, loans

app = FastAPI()
app.include_router(readers.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(authentication.router)


@app.get("/")
def get_root():
    return "Welcome to the books api !"

# to run : uvicorn book-api.main:app --reload

###########################################
# 3. Création de la db dans le main


models.Base.metadata.create_all(engine)
