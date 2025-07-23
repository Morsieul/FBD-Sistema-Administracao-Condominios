from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Condomino
from typing import List, Optional

router = APIRouter()

@router.post("/Condominos")
async def criar_condominio(cdm : Condomino):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            ("INSERT INTO condomino (CPF_Condomino, Nome_Condomino, Data_Nasc, ID_Telefone) values (%s, %s, %s, %s)", (cdm.CPF_Condomino, cdm.Nome_Condomino, cdm.Data_Nasc, cdm.ID_Telefone))
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro :(")
    finally:
        cur.close()
        conn.close()
    return {"msg: Condômino criado com sucesso!"}


@router.get("/Condominos", response_model= List[Condomino])
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

@router.put("/Condominos/{cpf}")
async def atualizar_condomino(cpf: str, cdm: Condomino):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE condomino
            SET Nome_Condomino = %s, Data_Nasc = %s, ID_Telefone = %s
            WHERE CPF_Condomino = %s
            """,
            (cdm.Nome_Condomino, cdm.Data_Nasc, cdm.ID_Telefone, cpf)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Condomino não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Condomino atualizado com sucesso"}

@router.delete("/Condominos/{cpf}")
async def deletar_condomino(cpf: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM condomino WHERE CPF_Condomino = %s", (cpf,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Condomino não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Condomino deletado com sucesso"}
