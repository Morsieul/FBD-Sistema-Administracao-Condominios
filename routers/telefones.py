from fastapi import APIRouter, HTTPException
from typing import List
from db import get_connection
from models import Telefone, TelefoneCreate  # Telefones separados para POST

router = APIRouter()

@router.post("/telefones")
async def criar_telefone(tel: TelefoneCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO telefone (DDD, Telefone)
            VALUES (%s, %s)
            RETURNING ID_Telefone
            """,
            (tel.DDD, tel.Telefone)
        )
        id_telefone = cur.fetchone()[0]
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar telefone: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Telefone criado com sucesso!", "ID_Telefone": id_telefone}

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
            DDD=d[1],
            Telefone=d[2]
        ) for d in rows
    ]

@router.put("/telefones/{ID_Telefone}")
async def atualizar_telefone(ID_Telefone: int, tel: TelefoneCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE telefone
            SET DDD = %s, Telefone = %s
            WHERE ID_Telefone = %s
            """,
            (tel.DDD, tel.Telefone, ID_Telefone)
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
        cur.execute("DELETE FROM telefone WHERE ID_Telefone = %s", (ID_Telefone,))
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
