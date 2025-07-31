from fastapi import APIRouter, HTTPException
from db import get_connection
from models import AreaComum, AreaComumUpdate
from typing import List, Optional

router = APIRouter()

@router.post("/areas-comuns")
async def criar_area(area: AreaComumUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO area_comum (Nome_Local)
            VALUES (%s)
            RETURNING ID_Area
            """,
            (area.Nome_Local,)
        )
        id_area = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar área comum: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Área comum criada com sucesso", "ID_Area": id_area}

@router.get("/areas-comuns", response_model=List[AreaComum])
async def listar_areas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM area_comum")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        AreaComum(ID_Area=row[0], Nome_Local=row[1]) for row in rows
    ]

@router.put("/areas-comuns/{id_area}")
async def atualizar_area(id_area: int, area: AreaComumUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE area_comum
            SET Nome_Local = %s
            WHERE ID_Area = %s
            """,
            (area.Nome_Local, id_area)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Área comum não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar área comum: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Área comum atualizada com sucesso"}

@router.delete("/areas-comuns/{id_area}")
async def deletar_area(id_area: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM area_comum WHERE ID_Area = %s", (id_area,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Área comum não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar área comum: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Área comum deletada com sucesso"}
