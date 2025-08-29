import requests
from bs4 import BeautifulSoup
import re
import urllib3
import time

def get_binance_p2p_prices(trade_type: str):
    """
    Obtiene los precios del P2P de Binance para un tipo de operación (BUY o SELL).
    """
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "clienttype": "web",
    }
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": trade_type,
        "page": 1,
        "rows": 20,
        "payTypes": [], #Se deja vacio para que escoja todas las opciones de pago.
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