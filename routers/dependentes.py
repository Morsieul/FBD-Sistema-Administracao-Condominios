from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Dependente, DependenteUpdate
from typing import List, Optional

router = APIRouter()

@router.post("/dependentes")
async def criar_dependente(dep: Dependente):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Verifica se o CPF do condômino existe
        cur.execute("SELECT 1 FROM condomino WHERE CPF_Condomino = %s", (dep.CPF_Condomino,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="CPF do condômino não encontrado")

        cur.execute(
            """
            INSERT INTO dependente (CPF_Dependente, CPF_Condomino, Nome_Dependente)
            VALUES (%s, %s, %s)
            RETURNING ID_Dependente
            """,
            (dep.CPF_Dependente, dep.CPF_Condomino, dep.Nome_Dependente)
        )
        novo_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar dependente: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Dependente criado com sucesso!", "ID_Dependente": novo_id}


@router.get("/dependentes", response_model=List[Dependente])
async def listar_dependentes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dependente")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Dependente(
            ID_Dependente=row[0],
            CPF_Dependente=row[1],
            CPF_Condomino=row[2],
            Nome_Dependente=row[3]
        ) for row in rows
    ]

@router.put("/dependentes/{id_dependente}")
async def atualizar_dependente(id_dependente: int, dep: DependenteUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            UPDATE dependente
            SET CPF_Dependente = %s, Nome_Dependente = %s
            WHERE ID_Dependente = %s
            """,
            (dep.CPF_Dependente, dep.Nome_Dependente, id_dependente)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dependente não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar dependente: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Dependente atualizado com sucesso"}

@router.delete("/dependentes/{id_dependente}")
async def deletar_dependente(id_dependente: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM dependente WHERE ID_Dependente = %s", (id_dependente,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dependente não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar dependente: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Dependente deletado com sucesso"}
