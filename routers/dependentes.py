from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Dependente
from typing import List, Optional

router = APIRouter()

@router.post("/Dependentes")
async def criar_dependente(dpd: Dependente):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            (dpd.ID_Dependente, dpd.CPF_Dependente, dpd.CPF_Dependente, dpd.Nome_Dependente)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro :(")
    finally:
        cur.close()
        conn.close()
    return {"msg: Dependente criado com sucesso!"}


@router.get("/Dependentes", response_model=List[Dependente])
async def listar_Dependentes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Dependente")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Dependente(
            ID_Dependente=d[0],
            CPF_Dependente=d[1],
            CPF_Condomino=d[2],
            Nome_Dependente=d[3]
        ) for d in rows
    ]

@router.delete("/Dependentes/{ID_Dependente}")
async def deletar_Dependente(ID_Dependente):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Dependente WHERE ID_Dependente = %s", (ID_Dependente))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dependente não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Dependente deletado com sucesso"}