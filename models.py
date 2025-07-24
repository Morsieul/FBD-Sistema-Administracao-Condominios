from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class Telefone(BaseModel):
    ID_Telefone: int 
    DDD: str
    Telefone: str

class TelefoneUpdate(BaseModel):
    DDD: str
    Telefone: str

class Condomino(BaseModel):
    CPF_Condomino: str
    Nome_Condomino: str
    Data_Nasc: datetime
    ID_Telefone: int

class CondominoUpdate(BaseModel):
    Nome_Condomino: str
    Data_Nasc: datetime
    ID_Telefone: int


class Dependente(BaseModel):
    ID_Dependente: int 
    CPF_Dependente: str
    CPF_Condomino: str
    Nome_Dependente: str

class AreaComum(BaseModel):
    ID_Area: int
    Nome_Local: str

class AreaComumUpdate(BaseModel):
    Nome_Local: str

class ReservaAreaComum(BaseModel):
    ID_Reserva: int
    ID_Area: int
    CPF_Condomino: str
    Data_Reserva: datetime

class ReservaUpdate(BaseModel):
    ID_Area: int
    CPF_Condomino: str
    Data_Reserva: datetime

class Apartamento(BaseModel): 
    Numero_Apartamento: int 
    CPF_Condomino: Optional[str] = None
    Descricao_Comodo: str
    qtd_quartos: int 
    Valor: float

class ApartamentoUpdate(BaseModel):  
    CPF_Condomino: Optional[str] = None
    Descricao_Comodo: str
    qtd_quartos: int 
    Valor: float

class Aluguel(BaseModel):
    ID_Aluguel: int
    Numero_Apartamento: int
    CPF_Condomino: Optional[str] = None
    Valor: float
    Data_Entrada: Optional[datetime] = None
    Data_Saida: Optional[datetime] = None

class AluguelUpdate(BaseModel):
    Numero_Apartamento: int
    CPF_Condomino: Optional[str] = None
    Valor: float
    Data_Entrada: Optional[datetime] = None
    Data_Saida: Optional[datetime] = None

class Pagamento(BaseModel):
    ID_Pagamento: int
    CPF_Condomino: str
    Numero_Apartamento: int

class PagamentoUpdate(BaseModel):
    CPF_Condomino: str
    Numero_Apartamento: int

class Recibo(BaseModel):
    ID_Recibo: int
    CPF_Condomino: str
    ID_Pagamento: int

class ReciboUpdate(BaseModel):
    CPF_Condomino: str
    ID_Pagamento: int