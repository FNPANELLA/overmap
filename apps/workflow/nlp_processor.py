import spacy
from django.conf import settings
import re
from typing import Dict, Any, List, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json

try:
    NLP = spacy.load(settings.SPACY_MODEL)
except Exception as e:
    print(f"ERROR: No se pudo cargar el modelo de SpaCy '{settings.SPACY_MODEL}'. Ejecute: python -m spacy download {settings.SPACY_MODEL}")
    NLP = None

class QueryTranslator:
    # clase encargada de procesar el lenguaje natural usando spacy y convertirlo en un formato estructurado para Overpass QL.
    def __init__(self):
        self.poi_map = {
            'cafetería': 'amenity=cafe',
            'cafeterías': 'amenity=cafe',
            'restaurante': 'amenity=restaurant',
            'restaurantes': 'amenity=restaurant',
            'tienda': 'shop',
            'tiendas': 'shop',
            'biblioteca': 'amenity=library',
            'bibliotecas': 'amenity=library',
            'oficina de correos': 'amenity=post_office', 
            'correos': 'amenity=post_office',
            'museo': 'tourism=museum',
            'museos': 'tourism=museum',
            'supermercado': 'shop=supermarket',
            'supermercados': 'shop=supermarket',
            'banco': 'amenity=bank',
            'bancos': 'amenity=bank',
            'farmacia': 'amenity=pharmacy',
            'farmacias': 'amenity=pharmacy',
        }

    def _geocode_location(self, location_name: str) -> Optional[Dict[str, float]]:
        #nominator bbox
        geolocator = Nominatim(user_agent="Overmap-Project-Automation-V1")
        try:
            location = geolocator.geocode(location_name, exactly_one=True, timeout=5)
            
            if location and location.raw.get('boundingbox'):
                bbox = location.raw['boundingbox']
                return {
                    'min_lat': float(bbox[0]),
                    'max_lat': float(bbox[1]),
                    'min_lon': float(bbox[2]),
                    'max_lon': float(bbox[3]),
                }
            return None
            
        except (GeocoderTimedOut, GeocoderServiceError, ValueError) as e:
            print(f"Error de geocodificación para {location_name}: {e}")
            return None

    def extract_entities(self, query_nl: str) -> Dict[str, Any]:
        if not NLP:
            return {'poi': None, 'location': None, 'filters': []}
        doc = NLP(query_nl.lower())
        extracted = {
            'poi': None, 
            'location': None, 
            'filters': [],
        }
        
        locations = [ent.text for ent in doc.ents if ent.label_ in ['LOC', 'GPE']]
        if locations:
            extracted['location'] = locations[0].title()
        for token in doc:
            if token.text in self.poi_map:
                extracted['poi'] = self.poi_map[token.text]

            # IDENTIFICAR FILTROS HIPER BASICO. NECESITO MAS
            if token.text in ['wifi', 'wlan', 'internet']:
                extracted['filters'].append('internet_access=wlan')
            if token.text in ['parking', 'aparcamiento']:
                extracted['filters'].append('parking')
                # FILTROS DE HORARIO 
            if token.text in ['abierto', 'abierta']:
                
                extracted['filters'].append('opening_hours=~^.{1,100}$') # Verifica la existencia del tag

            # FILTROS DE PRECIO/COSTO
            if token.text in ['barato', 'económico']:
                # Filtra por el nivel de precio más bajo
                extracted['filters'].append('price_level=1') 
            if token.text in ['caro', 'lujoso']:
                # Filtra por un nivel de precio alto
                extracted['filters'].append('price_level=3')

        return extracted
    
    def generate_overpass_ql(self, query_nl: str) -> str:
        entities = self.extract_entities(query_nl)
        poi = entities.get('poi')
        location_name = entities.get('location')
        filters = entities.get('filters')
        
        if not poi:
            raise ValueError("No se pudo identificar el Punto de Interés (POI) en la consulta.")
        

        bbox_filter = ""
        if location_name:
            bbox_coords = self._geocode_location(location_name)
            if not bbox_coords:
                raise ValueError(f"No se pudo geocodificar la ubicación: {location_name}")
            
            # Formato de BBox para Overpass: (min_lat, min_lon, max_lat, max_lon)

            bbox_filter = f"({bbox_coords['min_lat']},{bbox_coords['min_lon']},{bbox_coords['max_lat']},{bbox_coords['max_lon']})"

        ql_code = "[out:json][timeout:60];\n"
        

        poi_key, poi_value = poi.split('=') if '=' in poi else (poi, '*')
        
        # Construir la consulta de nodo (node, way, relation)
        ql_body = ""
        
        for tag_type in ['node', 'way', 'relation']:
            # Base del filtro de etiquetas ([amenity=cafe])
            tag_filter = f"[\"{poi_key}\"=\"{poi_value}\"]"
            

            final_tag_filter = tag_filter
            for f in filters:
                if f.startswith('opening_hours='):
                    # Filtro especial para existencia de opening_hours
                    final_tag_filter += f"[opening_hours]" 
                elif '=' in f:
                    f_key, f_value = f.split('=')
                    final_tag_filter += f"[\"{f_key}\"=\"{f_value}\"]"
                else:
                    final_tag_filter += f"[\"{f}\"]"
            
            # El filtro de BBox se añade justo después del tag filter
            ql_body += f"  {tag_type}{final_tag_filter}{bbox_filter};\n"
            

        ql_code += "(\n"
        ql_code += ql_body
        ql_code += ");\n"
        
        ql_code += "out center;\n"

        return ql_code