from fastapi import APIRouter, HTTPException
from db import get_connection
from models import ReservaAreaComum, ReservaUpdate
from typing import List, Optional

router = APIRouter()

@router.post("/reservas")
async def criar_reserva(reserva: ReservaUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verifica se o ID_Area existe
        cur.execute("SELECT 1 FROM area_comum WHERE ID_Area = %s", (reserva.ID_Area,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Área comum não encontrada")

        # Verifica se o CPF do condômino existe
        cur.execute("SELECT 1 FROM condomino WHERE CPF_Condomino = %s", (reserva.CPF_Condomino,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Condômino não encontrado")

        cur.execute(
            """
            INSERT INTO reserva_area (ID_Area, CPF_Condomino, Data_Reserva)
            VALUES (%s, %s, %s)
            RETURNING ID_Reserva
            """,
            (reserva.ID_Area, reserva.CPF_Condomino, reserva.Data_Reserva)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar reserva: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Reserva criada com sucesso", "ID_Reserva": new_id}

@router.get("/reservas", response_model=List[ReservaAreaComum])
async def listar_reservas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reserva_area")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        ReservaAreaComum(
            ID_Reserva=row[0],
            ID_Area=row[1],
            CPF_Condomino=row[2],
            Data_Reserva=row[3]
        ) for row in rows
    ]

@router.put("/reservas/{id_reserva}")
async def atualizar_reserva(id_reserva: int, reserva: ReservaUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE reserva_area
            SET ID_Area = %s, CPF_Condomino = %s, Data_Reserva = %s
            WHERE ID_Reserva = %s
            """,
            (reserva.ID_Area, reserva.CPF_Condomino, reserva.Data_Reserva, id_reserva)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar reserva: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Reserva atualizada com sucesso"}

@router.delete("/reservas/{id_reserva}")
async def deletar_reserva(id_reserva: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM reserva_area WHERE ID_Reserva = %s", (id_reserva,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar reserva: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Reserva deletada com sucesso"}
