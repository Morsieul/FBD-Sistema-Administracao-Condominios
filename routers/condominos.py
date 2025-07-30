from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Condomino
from typing import List, Optional

router = APIRouter()

@router.post("/Condominos")
async def criar_condomino(cdm: Condomino):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            (cdm.CPF_Condomino, cdm.Nome_Condomino, cdm.Data_Nasc, cdm.ID_Telefone)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao adicionar condômino")
    finally:
        cur.close()
        conn.close()
    return {"msg: Condômino criado com sucesso!"}


@router.get("/Condominos", response_model=List[Condomino])
async def listar_condominos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM condomino")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Condomino(
            CPF_Condomino=d[0],
            Nome_Condomino = d[1],
            Data_Nasc = d[2],
            ID_Telefone=d[3]
        ) for d in rows
    ]

@router.put("/Condominos/{CPF}")
async def atualizar_condomino(CPF: str, cdm: Condomino):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE condomino
            SET Nome_Condomino = %s, Data_Nasc = %s, ID_Telefone = %s
            WHERE CPF_Condomino = %s
            """,
            (cdm.Nome_Condomino, cdm.Data_Nasc, cdm.ID_Telefone, CPF)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Condômino não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Condômino atualizado com sucesso"}

@router.delete("/Condominos/{CPF}")
async def deletar_condomino(CPF: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM condomino WHERE CPF_Condomino = %s", (CPF))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Condômino não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Condômino deletado com sucesso"}