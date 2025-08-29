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

def scrap_get_bcv_rate():
    """
    Obtiene la tasa de cambio del BCV haciendo scraping del sidebar dolar en la página oficial.
    Usa el XPath específico: /html/body/div[4]/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[7]/div/div/div[2]
    """
    # Deshabilitar advertencias SSL para la página del BCV
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    url = "https://www.bcv.org.ve/estadisticas/tipo-de-cambio-de-referencia"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Hacer request con verificación SSL deshabilitada
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Método 1: Buscar directamente por el ID "dolar" (más confiable)
        dolar_element = soup.find('div', {'id': 'dolar'})
        if dolar_element:
            # Buscar la tasa dentro del elemento dolar
            for element in dolar_element.find_all(['div', 'span', 'strong']):
                text = element.get_text(strip=True)
                # Buscar números con formato de tasa, incluyendo formatos más largos
                if re.match(r'^\d{1,3}[,\.]\d{2,8}$', text):
                    rate_value = float(text.replace(',', '.'))
                    return rate_value
        
        # Método 2: Usar el XPath específico como fallback
        try:
            body = soup.find('body')
            if body:
                # Navegar siguiendo el XPath: /html/body/div[4]/div/div[2]/div/div[2]/div/div/section[1]/div/div[2]/div/div[7]/div/div/div[2]
                divs_level1 = body.find_all('div', recursive=False)
                if len(divs_level1) >= 4:
                    current_element = divs_level1[3]  # div[4]
                    
                    # Navegar por el path exacto
                    path_navigation = [
                        ('div', 0),           # div[4]/div
                        ('div', 1),           # div[4]/div/div[2]
                        ('div', 0),           # div[4]/div/div[2]/div
                        ('div', 1),           # div[4]/div/div[2]/div/div[2]
                        ('div', 0),           # div[4]/div/div[2]/div/div[2]/div
                        ('div', 0),           # div[4]/div/div[2]/div/div[2]/div/div
                        ('section', 0),       # div[4]/div/div[2]/div/div[2]/div/div/section[1]
                        ('div', 0),           # .../section[1]/div
                        ('div', 1),           # .../section[1]/div/div[2]
                        ('div', 0),           # .../section[1]/div/div[2]/div
                        ('div', 6),           # .../div/div[7]
                        ('div', 0),           # .../div[7]/div
                        ('div', 0),           # .../div[7]/div/div
                        ('div', 1)            # .../div[7]/div/div/div[2]
                    ]
                    
                    for tag, index in path_navigation:
                        elements = current_element.find_all(tag, recursive=False)
                        if len(elements) > index:
                            current_element = elements[index]
                        else:
                            break
                    
                    # Buscar la tasa en el elemento final
                    if current_element:
                        final_text = current_element.get_text(strip=True)
                        if re.match(r'^\d{1,3}[,\.]\d{2,8}$', final_text):
                            rate_value = float(final_text.replace(',', '.'))
                            return rate_value
        
        except Exception as xpath_error:
            pass  # Continuar con el método 3
        
        # Método 3: Buscar en el sidebar como última opción
        sidebar = soup.find('div', {'id': 'sidebar_first'}) or soup.find('div', class_=re.compile('herald-sidebar'))
        if sidebar:
            for element in sidebar.find_all(['div', 'span', 'strong']):
                text = element.get_text(strip=True)
                if re.match(r'^\d{1,3}[,\.]\d{2,8}$', text):
                    rate_value = float(text.replace(',', '.'))
                    return rate_value
        
        raise ValueError("No se pudo encontrar la tasa de cambio del BCV en el sidebar dolar")
        
    except requests.RequestException as e:
        raise Exception(f"Error al obtener datos del BCV: {e}")
    except Exception as e:
        raise Exception(f"Error procesando la tasa del BCV: {e}")

def get_bcv_rate():
    """Obtiene la tasa de cambio del BCV desde la API de pydolarve.
    """ 
    try:
        if not requests.get("https://pydolarve.org/api/v2/dollar", timeout=1).ok:
            raise requests.RequestException("No se pudo conectar a pydolarve")
        r = requests.get("https://pydolarve.org/api/v2/dollar", params={"page": "bcv"})
        r.raise_for_status()
        return r.json()["monitors"]["usd"]["price"]
    except requests.RequestException:
        #start_time = time.time()
        #sgbr=scrap_get_bcv_rate()
        #final_time = time.time()
        #print(f"Respuesta {final_time - start_time:.2f} seconds")
        return scrap_get_bcv_rate() #sgbr


if __name__ == "__main__":
    # Ejemplo de uso
    try:
        first_price, simple_avg, weighted_avg = get_binance_p2p_prices("BUY")
        print(f"Primer precio: {first_price}, Promedio simple: {simple_avg}, Promedio ponderado: {weighted_avg}")
        bcv_price = get_bcv_rate()
        print(f"Tasa de cambio del BCV: {bcv_price}")
    except Exception as e:
        print(f"Error obteniendo precios de Binance P2P: {e}")