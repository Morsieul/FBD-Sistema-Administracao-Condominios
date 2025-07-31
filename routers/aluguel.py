from fastapi import APIRouter, HTTPException
from typing import List
from db import get_connection
from models import Aluguel, AluguelUpdate

router = APIRouter()

@router.post("/aluguel")
async def criar_aluguel(alg: AluguelUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verifica se o apartamento existe
        cur.execute("SELECT 1 FROM apartamento WHERE Numero_Apartamento = %s", (alg.Numero_Apartamento,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Apartamento não encontrado")

        # Se CPF informado, verifica se o condômino existe
        if alg.CPF_Condomino:
            cur.execute("SELECT 1 FROM condomino WHERE CPF_Condomino = %s", (alg.CPF_Condomino,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Condômino não encontrado")

        cur.execute("""
            INSERT INTO aluguel (Numero_Apartamento, CPF_Condomino, Valor, Data_Entrada, Data_Saida)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING ID_Aluguel
        """, (
            alg.Numero_Apartamento, alg.CPF_Condomino, alg.Valor,
            alg.Data_Entrada, alg.Data_Saida
        ))

        new_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar aluguel: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Aluguel criado com sucesso", "ID_Aluguel": new_id}

@router.get("/aluguel", response_model=List[Aluguel])
async def listar_alugueis():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM aluguel")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Aluguel(
            ID_Aluguel=r[0],
            Numero_Apartamento=r[1],
            CPF_Condomino=r[2],
            Valor=float(r[3]),
            Data_Entrada=r[4],
            Data_Saida=r[5]
        ) for r in rows
    ]

@router.put("/aluguel/{id_aluguel}")
async def atualizar_aluguel(id_aluguel: int, alg: AluguelUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE aluguel
            SET Numero_Apartamento = %s,
                CPF_Condomino = %s,
                Valor = %s,
                Data_Entrada = %s,
                Data_Saida = %s
            WHERE ID_Aluguel = %s
        """, (
            alg.Numero_Apartamento,
            alg.CPF_Condomino,
            alg.Valor,
            alg.Data_Entrada,
            alg.Data_Saida,
            id_aluguel
        ))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluguel não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar aluguel: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Aluguel atualizado com sucesso"}

@router.delete("/aluguel/{id_aluguel}")
async def deletar_aluguel(id_aluguel: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM aluguel WHERE ID_Aluguel = %s", (id_aluguel,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aluguel não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar aluguel: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Aluguel deletado com sucesso"}
