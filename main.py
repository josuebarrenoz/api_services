import api_services as svc
from api_services import get_bcv_rate
from api_services import get_binance_p2p_prices
from typing import Tuple

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        first_price: float
        simple_avg: float
        weighted_avg: float
        first_price, simple_avg, weighted_avg = get_binance_p2p_prices("BUY", "usdc")
        print(f"Primer precio: {first_price}, Promedio simple: {simple_avg}, Promedio ponderado: {weighted_avg}")
        bcv_price: float = get_bcv_rate("eur")
        print(f"Tasa de cambio del BCV: {bcv_price}")
    except Exception as e:
        print(f"Error obteniendo precios de Binance P2P: {e}")

    # Ejemplo de uso
    try:
        first_price2: float
        simple_avg2: float
        weighted_avg2: float
        first_price2, simple_avg2, weighted_avg2 = svc.get_binance_p2p_prices("BUY")
        print(f"Primer precio: {first_price2}, Promedio simple: {simple_avg2}, Promedio ponderado: {weighted_avg2}")
        bcv_price2: float = svc.get_bcv_rate("euro")
        print(f"Tasa de cambio del BCV: {bcv_price2}")
    except Exception as e:
        print(f"Error obteniendo precios de Binance P2P: {e}")
