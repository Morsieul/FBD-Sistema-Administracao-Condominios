from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from routers import condominos, dependentes, telefones, areas


# python -m uvicorn main:app --reload

app = FastAPI(
    tittle = "API Condominio",
    version= "1.0"
)

app.include_router(condominos.router, prefix="/condominios", tags=["Condominios"])
app.include_router(dependentes.router, prefix="/dependentes", tags=["Dependentes"])
app.include_router(telefones.router, prefix="/telefones", tags=["Telefones"])
app.include_router(areas.router, prefix="/areascomuns", tags=["AreasComuns"])