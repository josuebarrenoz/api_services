import requests
from bs4 import BeautifulSoup
import re
import urllib3
import time
from typing import Optional, List, Tuple, Dict, Any


def scrap_get_bcv_rate(moneda:str = "dolar") -> float:
    """Scrapea la página del BCV para obtener la tasa de cambio.
       Parámetros:
           moneda: "dolar" o "euro" (por defecto "dolar")
       Retorna:
           Tasa de cambio como float
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

        #Buscar directamente por el ID moneda
        dolar_element = soup.find('div', {'id': moneda}) #or soup.find('div', class_=re.compile(f'herald-sidebar.*{moneda}'))
        if dolar_element:
            # Buscar la tasa dentro del elemento moneda
            for element in dolar_element.find_all(['div', 'span', 'strong']):
                text = element.get_text(strip=True)
                # Buscar números con formato de tasa, incluyendo formatos más largos
                if re.match(r'^\d{1,3}[,\.]\d{2,8}$', text):
                    rate_value = float(text.replace(',', '.'))
                    return rate_value
        raise Exception("No se encontró la tasa de cambio en la página del BCV.")

    except requests.RequestException as e:
        raise Exception(f"Error al obtener datos del BCV: {e}")
    except Exception as e:
        raise Exception(f"Error procesando la tasa del BCV: {e}")

def get_bcv_rate(moneda:str = "usd") -> float:
    """Obtiene la tasa de cambio del BCV para la moneda especificada. 
         Parámetros:
              moneda: "usd" o "euro" (por defecto "usd")
            Retorna:
              Tasa de cambio como float
    """
    #print(f"Obteniendo tasa BCV para moneda: {moneda}")
    if moneda.lower() == "usd" or moneda.lower() == "dolar":
        mon = "dolar"
    elif moneda.lower() == "euro" or moneda.lower() == "eur":
        mon = "euro"
    elif moneda.lower() == "yuan" or moneda.lower() == "cny":
        mon = "yuan"
    elif moneda.lower() == "lira" or moneda.lower() == "try":
        mon = "lira"
    elif moneda.lower() == "rublo" or moneda.lower() == "rub":
        mon = "rublo"
    else:
        raise ValueError("Moneda no soportada. Use 'usd' o 'euro'.")
    #print(f"Obteniendo tasa BCV para: {mon}")
    return scrap_get_bcv_rate(mon)

if __name__ == "__main__":
    tasa = get_bcv_rate()
    print(f"Tasa BCV obtenida: {tasa}")