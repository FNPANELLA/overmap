import requests
import json
from typing import Dict, List, Any
from requests.exceptions import RequestException
class QueryExec:
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
    def __init__(self):
        pass
    def execute_query(self, ql_code: str) -> List[Dict[str, Any]]:
        data = {'data': ql_code} 
        try:
            response = requests.post(self.OVERPASS_API_URL, data=data, timeout=60)
            # s el estado es 504 (Timeout) o 4xx, raise_for_status() lanzará RequestException
            response.raise_for_status()
            json_data = response.json()
            return self._process_elements(json_data.get('elements', []))
        except RequestException as e:
            # esto maneja el timeout, 504, 400 , y otros errores de conexión
            print(f"Fallo al contactar la API de overpass: {e}")
            return [] 
        except json.JSONDecodeError:
            print("ERROR: Respuesta de Overpass no es JSON válido.")


            #tuve q usar bbox para convertir la ubicacion a un set de cordenadas para poder deilimtar mejor el area pq no devolvia resultados
            return []
    def _process_elements(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for element in elements:
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lat')
            if element.get('center'):
                lat = element['center'].get('lat')
                lon = element['center'].get('lon')
            elif element.get('lat') and element.get('lon'):
                lat = element.get('lat')
                lon = element.get('lon')
            else:
                continue
            if not lat or not lon:
                continue
            result = {
                'osm_id': element.get('id'),
                'type': element.get('type'),
                'lat': lat,
                'lon': lon,
                'name': element.get('tags', {}).get('name', 'N/A'),
                'address': element.get('tags', {}).get('addr:street', 'N/A'),
                'phone': element.get('tags', {}).get('phone'),
                'website': element.get('tags', {}).get('website'),
                'tags': element.get('tags', {})
            }
            results.append(result)
        return results