from fastapi import APIRouter, HTTPException
from typing import List
from db import get_connection
from models import Pagamento, PagamentoUpdate

router = APIRouter()
@router.post("/pagamentos")
async def criar_pagamento(pag: PagamentoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Verifica se CPF existe
        cur.execute("SELECT 1 FROM condomino WHERE CPF_Condomino = %s", (pag.CPF_Condomino,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Condômino não encontrado")

        # Verifica se apartamento existe
        cur.execute("SELECT 1 FROM apartamento WHERE Numero_Apartamento = %s", (pag.Numero_Apartamento,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Apartamento não encontrado")

        cur.execute("""
            INSERT INTO pagamento (CPF_Condomino, Numero_Apartamento)
            VALUES (%s, %s)
            RETURNING ID_Pagamento
        """, (pag.CPF_Condomino, pag.Numero_Apartamento))

        new_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pagamento: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pagamento registrado com sucesso", "ID_Pagamento": new_id}

@router.get("/pagamentos", response_model=List[Pagamento])
async def listar_pagamentos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagamento")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Pagamento(
            ID_Pagamento=row[0],
            CPF_Condomino=row[1],
            Numero_Apartamento=row[2]
        ) for row in rows
    ]

@router.put("/pagamentos/{id_pagamento}")
async def atualizar_pagamento(id_pagamento: int, pag: PagamentoUpdate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE pagamento
            SET CPF_Condomino = %s,
                Numero_Apartamento = %s
            WHERE ID_Pagamento = %s
        """, (pag.CPF_Condomino, pag.Numero_Apartamento, id_pagamento))

        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pagamento: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pagamento atualizado com sucesso"}

@router.delete("/pagamentos/{id_pagamento}")
async def deletar_pagamento(id_pagamento: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM pagamento WHERE ID_Pagamento = %s", (id_pagamento,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pagamento: {str(e)}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Pagamento deletado com sucesso"}
