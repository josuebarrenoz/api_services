import requests
from bs4 import BeautifulSoup
import re
import urllib3
import time
from typing import Tuple, Dict, List, Any

def get_binance_p2p_prices(trade_type: str, asset:str = "usdt",payTypes:list =[],page:int = 1) -> Tuple[float, float, float]:
    """ Obtiene los precios del P2P de Binance para un tipo de operación (BUY o SELL).
        Parámetros:
            trade_type: "BUY" o "SELL"
            asset: Criptomoneda a consultar (por defecto "usdt")
            payTypes: Lista de métodos de pago a filtrar (por defecto todos)
            page: Página de resultados a consultar (por defecto 1)
        Retorna:
            first_price: Primer precio listado
            simple_avg: Promedio simple de los precios listados
            weighted_avg: Promedio ponderado por volumen de los precios listados
    """

    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "clienttype": "web",
    }
    payload = {
        "asset": asset.upper(),
        "fiat": "VES",
        "tradeType": trade_type,
        "page": page,
        "rows": 20,
        "payTypes": payTypes, #Se deja vacio para que escoja todas las opciones de pago.
	#En las proximas versiones se mejorará la funcion para que reciba varios
	#payTypes y otros parametros para este POST.
        "publisherType": None
    }

    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()  # Lanza una excepción si la petición falla
    data = r.json()["data"]

    if not data:
        # Si no hay datos, devuelve valores que no afecten los cálculos
        return 0, 0, 0

    prices = [float(ad["adv"]["price"]) for ad in data]
    volumes = [float(ad["adv"]["surplusAmount"]) for ad in data]

    # Cálculos
    first_price = prices[0]
    simple_avg = sum(prices) / len(prices)
    weighted_avg = sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)

    return first_price, simple_avg, weighted_avg

if __name__ == "__main__":
    compra_pp, compra_avg, compra_pond = get_binance_p2p_prices("BUY")
    venta_pp, venta_avg, venta_pond = get_binance_p2p_prices("SELL")
    print(f"Compra - Primer Precio: {compra_pp}, Promedio Simple: {compra_avg}, Promedio Ponderado: {compra_pond}")
    print(f"Venta - Primer Precio: {venta_pp}, Promedio Simple: {venta_avg}, Promedio Ponderado: {venta_pond}")