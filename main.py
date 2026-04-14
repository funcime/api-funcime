from fastapi import FastAPI, Query, HTTPException
from urllib.request import urlopen
from urllib.parse import urlencode
import json

app = FastAPI(
    title="API FUNCIME - Pesquisa de Preços",
    version="1.0.0",
    description="API auxiliar para pesquisa de preços e identificação de itens no Compras.gov."
)

BASE_COMPRAS = "https://dadosabertos.compras.gov.br"


@app.get("/")
def raiz():
    return {"mensagem": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/buscar-item-por-descricao")
def buscar_item_por_descricao(
    descricaoItem: str = Query(..., description="Descrição do item para busca no catálogo")
):
    url_base = BASE_COMPRAS + "/modulo-material/4_consultarItemMaterial"
    params = {
        "descricaoItem": descricaoItem,
        "pagina": 1
    }
    url = url_base + "?" + urlencode(params)

    try:
        with urlopen(url, timeout=30) as resposta:
            texto = resposta.read().decode("utf-8")
            dados = json.loads(texto)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    resultado = dados.get("resultado", []) if isinstance(dados, dict) else []

    itens = []
    for item in resultado[:10]:
        itens.append({
            "codigoItemCatalogo": item.get("codigoItem"),
            "descricaoItem": item.get("descricaoItem"),
            "nomeGrupo": item.get("nomeGrupo"),
            "nomeClasse": item.get("nomeClasse"),
            "nomePdm": item.get("nomePdm"),
            "statusItem": item.get("statusItem"),
        })

    return {
        "descricaoPesquisada": descricaoItem,
        "quantidade": len(resultado),
        "itens": itens
    }


@app.get("/buscar-precos-comprasgov")
def buscar_precos_comprasgov(
    codigoItemCatalogo: int = Query(..., description="Código do item catálogo")
):
    url_base = BASE_COMPRAS + "/modulo-pesquisa-preco/1_consultarMaterial"
    params = {
        "codigoItemCatalogo": codigoItemCatalogo,
        "pagina": 1,
        "tamanhoPagina": 10
    }
    url = url_base + "?" + urlencode(params)

    try:
        with urlopen(url, timeout=30) as resposta:
            texto = resposta.read().decode("utf-8")
            dados = json.loads(texto)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    resultado = dados.get("resultado", []) if isinstance(dados, dict) else []

    return {
        "codigoItemCatalogo": codigoItemCatalogo,
        "quantidade": len(resultado),
        "resultado": resultado[:10]
    }
