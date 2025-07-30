from fastapi import APIRouter, HTTPException
from db import get_connection
from models import AreaComum
from typing import List, Optional

router = APIRouter()

@router.post("/AreasComuns")
async def criar_AreaComum(ac: AreaComum):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            (ac.ID_AreaComum, ac.Nome_Local)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Erro ao adicionar Área Comum")
    finally:
        cur.close()
        conn.close()
    return {"msg: Área Comum criada com sucesso!"}


@router.get("/AreasComuns", response_model=List[AreaComum])
async def listar_AreasComuns():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM area_comum")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        AreaComum(
            ID_Area=d[0],
            Nome_Local=d[1],
        ) for d in rows
    ]

@router.put("/AreasComuns/{ID_Area}")
async def atualizar_AreaComum(ID_Area: int, ac: AreaComum):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE AreaComum
            SET ID_AreaComum = %s, Nome_Local = %s
            WHERE ID_AreaComum = %s
            """,
            (ac.ID_Telefone, ac.Nome_Local)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Área Comum não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Área Comum atualizada com sucesso"}

@router.delete("/AreasComuns/{ID_AreaComum}")
async def deletar_AreaComum(ID_AreaComum: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM AreaComum WHERE ID_AreaComum = %s", (ID_AreaComum))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Área Comum não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Área Comum deletada com sucesso"}