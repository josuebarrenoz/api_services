import api_services as svc
from api_services import get_bcv_rate
from api_services import get_binance_p2p_prices

if __name__ == "__main__":
    # Ejemplo de uso
    try:
        first_price, simple_avg, weighted_avg = get_binance_p2p_prices("BUY")
        print(f"Primer precio: {first_price}, Promedio simple: {simple_avg}, Promedio ponderado: {weighted_avg}")
        bcv_price = get_bcv_rate()
        print(f"Tasa de cambio del BCV: {bcv_price}")
    except Exception as e:
        print(f"Error obteniendo precios de Binance P2P: {e}")

    # Ejemplo de uso
    try:
        first_price, simple_avg, weighted_avg = svc.get_binance_p2p_prices("BUY")
        print(f"Primer precio: {first_price}, Promedio simple: {simple_avg}, Promedio ponderado: {weighted_avg}")
        bcv_price = svc.get_bcv_rate()
        print(f"Tasa de cambio del BCV: {bcv_price}")
    except Exception as e:
        print(f"Error obteniendo precios de Binance P2P: {e}")
