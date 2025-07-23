from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from routers import condominos

app = FastAPI(
    tittle = "Api Condominio",
    version= "1.0"
)

app.include_router(condominos.router, prefix="/condominios", tags=["Condominios"])