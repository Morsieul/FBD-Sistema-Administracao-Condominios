from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Telefone
from typing import List, Optional

router = APIRouter()

@router.post("/telefones")
async def criar_telefone(tel: Telefone):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            (tel.ID_Telefone, tel.telefone)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro: ")
    finally:
        cur.close()
        conn.close()
    return {"msg: Condômino criado com sucesso!"}


@router.get("/telefones", response_model=List[Telefone])
async def listar_telefones():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM telefone")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Telefone(
            ID_Telefone=d[0],
            ddd=d[1],
            telefone=d[2]
        ) for d in rows
    ]

@router.put("/telefones/{ID_Telefone}")
async def atualizar_telefone(ID_Telefone: int, tel: Telefone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE telefone
            SET ddd = %s, telefone = %s
            """,
            (tel.ddd, tel.telefone)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Telefone não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Telefone atualizado com sucesso"}

@router.delete("/telefones/{ID_Telefone}")
async def deletar_telefone(ID_Telefone: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM telefone WHERE ID_Telefone = %s", (ID_Telefone))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Telefone não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Telefone deletado com sucesso"}