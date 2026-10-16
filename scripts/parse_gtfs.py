#!/usr/bin/env python3
"""
Script para parsear el GTFS de Córdoba y generar archivos JSON de líneas de transporte.
"""
import csv
import json
import os
from collections import defaultdict
from typing import Dict, List, Any

# Paths
GTFS_DIR = "/tmp/gtfs-cordoba"
OUTPUT_DIR = "/workspace/src/data/lineas"

def load_csv(filename: str) -> List[Dict[str, str]]:
    """Carga un archivo CSV del GTFS y retorna una lista de diccionarios."""
    path = os.path.join(GTFS_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_agency_name(agency_id: str, agencies: List[Dict]) -> str:
    """Obtiene el nombre de la empresa por su ID."""
    for agency in agencies:
        if agency['agency_id'] == agency_id:
            return agency['agency_name']
    return ""

def get_route_trips(route_id: str, trips: List[Dict]) -> List[Dict]:
    """Obtiene todos los viajes de una ruta."""
    return [trip for trip in trips if trip['route_id'] == route_id]

def get_trip_stops(trip_id: str, stop_times: List[Dict], stops: List[Dict]) -> List[Dict]:
    """Obtiene las paradas de un viaje en orden."""
    trip_stops = [st for st in stop_times if st['trip_id'] == trip_id]
    trip_stops.sort(key=lambda x: int(x['stop_sequence']))
    
    # Enriquecer con información de la parada
    result = []
    for st in trip_stops:
        stop = next((s for s in stops if s['stop_id'] == st['stop_id']), None)
        if stop:
            result.append({
                'stop_id': st['stop_id'],
                'stop_name': stop['stop_name'],
                'stop_lat': stop['stop_lat'],
                'stop_lon': stop['stop_lon'],
                'stop_sequence': st['stop_sequence'],
                'arrival_time': st.get('arrival_time', ''),
                'departure_time': st.get('departure_time', '')
            })
    return result

def extract_main_stops(all_stops: List[Dict], max_stops: int = 8) -> List[str]:
    """Extrae las paradas principales de una lista de paradas."""
    if len(all_stops) <= max_stops:
        return [stop['stop_name'] for stop in all_stops]
    
    # Tomar primera, última y algunas intermedias
    indices = [0]  # Primera
    step = len(all_stops) // (max_stops - 1)
    for i in range(1, max_stops - 1):
        indices.append(min(i * step, len(all_stops) - 1))
    indices.append(len(all_stops) - 1)  # Última
    
    # Eliminar duplicados manteniendo orden
    seen = set()
    result = []
    for idx in indices:
        name = all_stops[idx]['stop_name']
        if name not in seen:
            seen.add(name)
            result.append(name)
    
    return result

def get_street_names_from_stops(stops: List[Dict]) -> List[str]:
    """Intenta extraer nombres de calles de las paradas."""
    streets = []
    for stop in stops:
        name = stop['stop_name']
        # Muchas paradas en GTFS tienen formato "Calle1 y Calle2" o similar
        # Tomamos el nombre de la parada como referencia de ubicación
        if name and name not in streets:
            streets.append(name)
    return streets[:15]  # Limitar a 15 para no tener listas muy largas

def create_maps_embed_url(stops: List[Dict]) -> str:
    """Crea una URL de Google Maps con las paradas."""
    if not stops:
        return ""
    
    # Usar la primera y última parada para crear una ruta
    first = stops[0]
    last = stops[-1]
    
    origin = f"{first['stop_lat']},{first['stop_lon']}"
    destination = f"{last['stop_lat']},{last['stop_lon']}"
    
    # Agregar algunos waypoints intermedios si hay
    waypoints = ""
    if len(stops) > 2:
        # Tomar hasta 3 paradas intermedias
        middle_indices = [len(stops) // 4, len(stops) // 2, 3 * len(stops) // 4]
        middle_stops = [stops[i] for i in middle_indices if i < len(stops)]
        waypoint_coords = [f"{s['stop_lat']},{s['stop_lon']}" for s in middle_stops]
        if waypoint_coords:
            waypoints = "&waypoints=" + "|".join(waypoint_coords)
    
    return f"https://www.google.com/maps/embed/v1/directions?key=YOUR_API_KEY&origin={origin}&destination={destination}{waypoints}&mode=transit"

def parse_route(route: Dict, agencies: List[Dict], trips: List[Dict], 
                stop_times: List[Dict], stops: List[Dict]) -> Dict[str, Any]:
    """Parsea una ruta del GTFS y la convierte al formato JSON requerido."""
    
    route_id = route['route_id']
    route_number = route['route_short_name'].strip()
    route_name = route['route_long_name'].strip() or f"Línea {route_number}"
    
    # Obtener empresa
    agency_name = get_agency_name(route['agency_id'], agencies)
    
    # Obtener viajes de la ruta
    route_trips = get_route_trips(route_id, trips)
    
    # Agrupar viajes por dirección (direction_id)
    trips_by_direction = defaultdict(list)
    for trip in route_trips:
        direction = trip.get('direction_id', '0')
        trips_by_direction[direction].append(trip)
    
    # Procesar recorridos (ida y vuelta)
    recorridos = {}
    
    for direction, dir_trips in trips_by_direction.items():
        if not dir_trips:
            continue
            
        # Tomar el primer viaje como representativo de la dirección
        sample_trip = dir_trips[0]
        trip_stops = get_trip_stops(sample_trip['trip_id'], stop_times, stops)
        
        if not trip_stops:
            continue
        
        # Determinar si es ida o vuelta
        direction_key = "vuelta" if direction == "1" else "ida"
        
        # Descripción del recorrido
        if len(trip_stops) >= 2:
            descripcion = f"{trip_stops[0]['stop_name']} - {trip_stops[-1]['stop_name']}"
        else:
            descripcion = "Recorrido circular"
        
        # Calles (nombres de paradas como referencia)
        calles = get_street_names_from_stops(trip_stops)
        
        recorridos[direction_key] = {
            "descripcion": descripcion,
            "calles": calles
        }
    
    # Si no hay vuelta, dejar el objeto vacío
    if "ida" not in recorridos:
        recorridos["ida"] = {
            "descripcion": "",
            "calles": []
        }
    if "vuelta" not in recorridos:
        recorridos["vuelta"] = {
            "descripcion": "",
            "calles": []
        }
    
    # Paradas principales (usar las de ida)
    paradas_principales = []
    if route_trips:
        sample_trip = route_trips[0]
        trip_stops = get_trip_stops(sample_trip['trip_id'], stop_times, stops)
        paradas_principales = extract_main_stops(trip_stops)
    
    # Crear URL de Google Maps
    maps_url = ""
    if route_trips:
        sample_trip = route_trips[0]
        trip_stops = get_trip_stops(sample_trip['trip_id'], stop_times, stops)
        maps_url = create_maps_embed_url(trip_stops)
    
    # Crear objeto JSON
    linea_data = {
        "numero": route_number,
        "nombre": route_name,
        "empresa": agency_name,
        "descripcionCorta": f"Línea {route_number} - {agency_name}",
        "recorrido": recorridos,
        "paradasPrincipales": paradas_principales,
        "horarios": [],
        "tarifas": [],
        "mapsEmbedUrl": maps_url,
        "ultimaActualizacion": "2023-03-16",
        "fuente": "https://gobiernoabierto.cordoba.gob.ar/data/datos-abiertos/categoria/transporte-urbano/gtfs-de-la-ciudada-de-cordoba/3319",
        "notas": "Datos del GTFS oficial de la Municipalidad de Córdoba (2023); el recorrido puede haber cambiado. Verificá en la app Tu Bondi.",
        "esEjemplo": False
    }
    
    return linea_data

def main():
    """Función principal."""
    print("Cargando datos del GTFS...")
    
    # Cargar todos los archivos necesarios
    agencies = load_csv('agency.txt')
    routes = load_csv('routes.txt')
    trips = load_csv('trips.txt')
    stops = load_csv('stops.txt')
    
    print(f"Encontradas {len(routes)} rutas")
    print("Cargando stop_times... (puede tomar un momento)")
    stop_times = load_csv('stop_times.txt')
    print(f"Cargados {len(stop_times)} registros de stop_times")
    
    # Crear directorio de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Procesar cada ruta
    print("\nProcesando rutas...")
    processed = 0
    
    for route in routes:
        try:
            route_number = route['route_short_name'].strip()
            if not route_number:
                # Usar parte del nombre largo si no hay número
                route_long = route['route_long_name'].strip()
                if route_long:
                    # Intentar extraer un número del nombre
                    import re
                    match = re.search(r'\d+', route_long)
                    if match:
                        route_number = match.group()
                    else:
                        route_number = route['route_id']
                else:
                    route_number = route['route_id']
            
            print(f"  Procesando línea {route_number}...")
            
            linea_data = parse_route(route, agencies, trips, stop_times, stops)
            
            # Guardar JSON
            filename = f"linea-{route_number}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(linea_data, f, ensure_ascii=False, indent=2)
            
            processed += 1
            
        except Exception as e:
            print(f"  Error procesando ruta {route.get('route_id', 'unknown')}: {e}")
            continue
    
    print(f"\n✓ Procesadas {processed} líneas exitosamente")
    print(f"✓ Archivos guardados en {OUTPUT_DIR}")
    
    # Crear índice de líneas
    index_data = {
        "totalLineas": processed,
        "ultimaActualizacion": "2023-03-16",
        "fuente": "GTFS oficial Municipalidad de Córdoba",
        "lineas": []
    }
    
    # Listar todas las líneas generadas
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if filename.endswith('.json') and filename.startswith('linea-'):
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                index_data['lineas'].append({
                    "numero": data['numero'],
                    "nombre": data['nombre'],
                    "empresa": data['empresa'],
                    "archivo": filename
                })
    
    # Guardar índice
    index_path = os.path.join(OUTPUT_DIR, 'index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Índice creado en {index_path}")

if __name__ == '__main__':
    main()
