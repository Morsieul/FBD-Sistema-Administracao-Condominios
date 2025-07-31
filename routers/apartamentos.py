# routers/apartamento.py
from fastapi import APIRouter, HTTPException
from typing import List
from db import get_connection
from models import Apartamento

router = APIRouter()

@router.post("/Apartamentos")
async def criar_apartamento(ap: Apartamento):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Verifica se CPF informado existe, se não for None
        if ap.CPF_Condomino:
            cur.execute("SELECT 1 FROM condomino WHERE CPF_Condomino = %s", (ap.CPF_Condomino,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="CPF do condômino não encontrado")

        cur.execute(
            """
            INSERT INTO apartamento 
            (Numero_Apartamento, CPF_Condomino, Descricao_Comodo, qtd_quartos, Valor)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (ap.Numero_Apartamento, ap.CPF_Condomino, ap.Descricao_Comodo, ap.qtd_quartos, ap.Valor)
        )
        conn.commit()
    except HTTPException:
        raise  # repassa HTTPException personalizada
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar apartamento: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Apartamento criado com sucesso!"}

@router.get("/Apartamentos", response_model=List[Apartamento])
async def listar_apartamentos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM apartamento")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        Apartamento(
            Numero_Apartamento=r[0],
            CPF_Condomino=r[1],
            Descricao_Comodo=r[2],
            qtd_quartos=r[3],
            Valor=r[4]
        )
        for r in rows
    ]

@router.put("/Apartamentos/{numero}")
async def atualizar_apartamento(numero: int, ap: Apartamento):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE apartamento
            SET CPF_Condomino = %s, Descricao_Comodo = %s, qtd_quartos = %s, Valor = %s
            WHERE Numero_Apartamento = %s
            """,
            (ap.CPF_Condomino, ap.Descricao_Comodo, ap.qtd_quartos, ap.Valor, numero)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Apartamento não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"msg": "Apartamento atualizado com sucesso"}

@router.delete("/Apartamentos/{numero}")
async def deletar_apartamento(numero: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM apartamento WHERE Numero_Apartamento = %s", (numero,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Apartamento não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return {"msg": "Apartamento deletado com sucesso"}
