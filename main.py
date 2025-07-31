from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from routers import condominos, dependentes,areas, telefones, apartamentos, reservas, aluguel, pagamento

app = FastAPI(
    tittle = "Api Condominio",
    version= "1.0"
)

app.include_router(condominos.router, prefix="/condominios", tags=["Condôminos"])
app.include_router(dependentes.router, prefix="/dependentes", tags=["Dependentes"])
app.include_router(telefones.router, prefix="/telefones", tags=["Telefones"])
app.include_router(areas.router, prefix="/areas-comuns", tags=["AreasComuns"])
app.include_router(reservas.router, prefix="/reservas", tags=["ReservaAreaComum"])
app.include_router(apartamentos.router, prefix="/apartamentos", tags= ["Apartamento"])
app.include_router(aluguel.router, prefix = "/aluguel", tags=["Aluguel"])
app.include_router(pagamento.router, prefix = "/pagamentos", tags=["Pagamentos"])