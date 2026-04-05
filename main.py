from fastapi import FastAPI, Query
from pydantic import BaseModel
from statistics import median

app = FastAPI(
    title="API FUNCIME Pesquisa de Preços",
    version="0.2.0"
)

@app.get("/")
def raiz():
    return {"mensagem": "API da FUNCIME funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/buscar-referencias-item")
def buscar_referencias_item(
    descricao: str = Query(..., description="Descrição do item"),
    unidade: str = Query(..., description="Unidade do item"),
    quantidade: float | None = Query(None, description="Quantidade")
):
    return {
        "itemConsultado": descricao,
        "unidadeConsultada": unidade,
        "quantidadeConsultada": quantidade,
        "referencias": [
            {
                "fonte": "exemplo_publico_1",
                "descricaoEncontrada": descricao,
                "unidadeEncontrada": unidade,
                "precoUnitario": 10.0,
                "observacao": "Referência de exemplo para testar a Action"
            },
            {
                "fonte": "exemplo_publico_2",
                "descricaoEncontrada": descricao,
                "unidadeEncontrada": unidade,
                "precoUnitario": 12.5,
                "observacao": "Referência de exemplo para testar a Action"
            },
            {
                "fonte": "exemplo_publico_3",
                "descricaoEncontrada": descricao,
                "unidadeEncontrada": unidade,
                "precoUnitario": 11.0,
                "observacao": "Referência de exemplo para testar a Action"
            }
        ]
    }

class EquivalenciaEntrada(BaseModel):
    descricaoDemandada: str
    unidadeDemandada: str
    descricaoEncontrada: str
    unidadeEncontrada: str

@app.post("/avaliar-equivalencia")
def avaliar_equivalencia(dados: EquivalenciaEntrada):
    desc_dem = dados.descricaoDemandada.strip().lower()
    desc_enc = dados.descricaoEncontrada.strip().lower()
    und_dem = dados.unidadeDemandada.strip().lower()
    und_enc = dados.unidadeEncontrada.strip().lower()

    if und_dem != und_enc:
        return {
            "classificacao": "invalida",
            "observacoes": ["Unidade incompatível."]
        }

    if desc_dem == desc_enc:
        return {
            "classificacao": "valida",
            "observacoes": ["Descrição e unidade compatíveis."]
        }

    return {
        "classificacao": "valida_com_ressalva",
        "observacoes": ["Descrição aproximada; exige conferência humana."]
    }

class Referencia(BaseModel):
    fonte: str
    descricaoEncontrada: str
    unidadeEncontrada: str
    precoUnitario: float

class SerieEntrada(BaseModel):
    referencias: list[Referencia]

@app.post("/montar-serie-precos")
def montar_serie_precos(dados: SerieEntrada):
    precos = [r.precoUnitario for r in dados.referencias]

    if not precos:
        return {
            "quantidadeValidas": 0,
            "mediana": None,
            "conclusao": "Base insuficiente."
        }

    return {
        "quantidadeValidas": len(precos),
        "mediana": median(precos),
        "conclusao": "Série consolidada."
    }
