from fastapi import FastAPI, Query, HTTPException
from urllib.request import urlopen
from urllib.parse import urlencode
import json

app = FastAPI()

BASE_COMPRAS = "https://dadosabertos.compras.gov.br"


@app.get("/")
def raiz():
    return {"mensagem": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/buscar-item-por-descricao")
def buscar_item_por_descricao(descricaoItem: str = Query(...)):
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

    if isinstance(dados, dict):
        resultado = dados.get("resultado", [])
    else:
        resultado = []

    itens = []
    for item in resultado[:10]:
        itens.append({
            "codigoItem": item.get("codigoItem"),
            "descricaoItem": item.get("descricaoItem"),
            "nomeGrupo": item.get("nomeGrupo"),
            "nomeClasse": item.get("nomeClasse"),
            "nomePdm": item.get("nomePdm"),
            "statusItem": item.get("statusItem")
        })

    return {
        "descricaoPesquisada": descricaoItem,
        "quantidade": len(resultado),
        "itens": itens
    }


@app.get("/buscar-precos-comprasgov")
def buscar_precos_comprasgov(codigoItemCatalogo: int = Query(...)):
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

    if isinstance(dados, dict):
        resultado = dados.get("resultado", [])
    else:
        resultado = []

    return {
        "codigoItemCatalogo": codigoItemCatalogo,
        "quantidade": len(resultado),
        "resultado": resultado[:5]
    }
