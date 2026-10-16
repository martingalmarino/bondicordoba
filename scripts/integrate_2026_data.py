#!/usr/bin/env python3
"""
Integración de datos 2026 desde lineas_transporte_cba scraper.
Combina datos reales del scraper con fallback a GTFS 2023 donde no haya datos.
Solo aplica renombramientos confirmados en noticias oficiales.
"""
import json
import os
import geopandas as gpd
from collections import defaultdict

# Paths
SCRAPER_RECORRIDOS = "/tmp/lineas_transporte_cba/recorridos_cordoba.gpkg"
SCRAPER_PARADAS = "/tmp/lineas_transporte_cba/paradas_cordoba.gpkg"
DATA_DIR_2023 = "/workspace/src/data/lineas"
OUTPUT_DIR = "/workspace/src/data/lineas"
REPORT_FILE = "/workspace/data_sources_report.md"

# Renombramientos CONFIRMADOS en noticias (1/03/2026)
# Fuente: https://cordoba.gob.ar/marzo-lineas-a1-b1-c1-c2/
RENOMBRAMIENTOS = {
    "A1": "36A",
    "B1": "81B", 
    "C1": "10C",
    "C2": "B10",
}

# Nueva línea confirmada (1/08/2026)
# Fuente: https://www.perfil.com/noticias/cordoba/...corredor-7.phtml
LINEAS_NUEVAS = ["76"]

def load_scraper_data():
    """Carga datos del scraper si existen."""
    if not os.path.exists(SCRAPER_RECORRIDOS):
        return None, None
    
    try:
        recorridos_gdf = gpd.read_file(SCRAPER_RECORRIDOS)
        paradas_gdf = gpd.read_file(SCRAPER_PARADAS)
        return recorridos_gdf, paradas_gdf
    except Exception as e:
        print(f"Error cargando scraper data: {e}")
        return None, None

def load_gtfs_2023_data():
    """Carga datos GTFS 2023 existentes."""
    lineas_2023 = {}
    for filename in os.listdir(DATA_DIR_2023):
        if not filename.startswith('linea-') or not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(DATA_DIR_2023, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            numero = data.get('numero', '')
            if numero:
                lineas_2023[numero] = data
    
    return lineas_2023

def extract_paradas_from_gdf(paradas_gdf, linea, sentido=None):
    """Extrae lista de paradas de un GeoDataFrame."""
    if paradas_gdf is None:
        return []
    
    query = paradas_gdf['linea_nombre'] == linea
    if sentido:
        query &= paradas_gdf['sentido_txt'] == sentido
    
    paradas_subset = paradas_gdf[query]
    if len(paradas_subset) == 0:
        return []
    
    # Ordenar por secuencia si existe
    if 'secuencia' in paradas_subset.columns:
        paradas_subset = paradas_subset.sort_values('secuencia')
    
    paradas = paradas_subset['parada_nombre'].unique().tolist() if 'parada_nombre' in paradas_subset.columns else []
    
    # Limitar a paradas principales (primera, última, algunas intermedias)
    if len(paradas) > 8:
        indices = [0]
        step = len(paradas) // 7
        for i in range(1, 7):
            idx = min(i * step, len(paradas) - 1)
            if idx not in indices:
                indices.append(idx)
        indices.append(len(paradas) - 1)
        paradas = [paradas[i] for i in sorted(set(indices))]
    
    return paradas

def integrate_data():
    """Integra datos de scraper 2026 con fallback a GTFS 2023."""
    print("="*70)
    print("INTEGRACIÓN DATOS 2026")
    print("="*70)
    
    # Cargar datos
    print("\n1. Cargando datos del scraper 2026...")
    recorridos_gdf, paradas_gdf = load_scraper_data()
    
    if recorridos_gdf is None:
        print("   ⚠️  SCRAPER DATA NO DISPONIBLE AÚN")
        print("   Esperando a que termine el scraper...")
        return False
    
    print(f"   ✓ Recorridos: {len(recorridos_gdf)} rutas")
    print(f"   ✓ Paradas: {len(paradas_gdf)} paradas")
    
    print("\n2. Cargando datos GTFS 2023 (fallback)...")
    lineas_2023 = load_gtfs_2023_data()
    print(f"   ✓ Líneas GTFS 2023: {len(lineas_2023)}")
    
    # Procesar datos del scraper
    print("\n3. Procesando datos del scraper 2026...")
    lineas_scraper = defaultdict(lambda: {"rutas": [], "empresa": None})
    
    for _, row in recorridos_gdf.iterrows():
        linea = row['linea_nombre']  # Columna correcta
        empresa = row['empresa']
        sentido = row['sentido_txt']
        
        lineas_scraper[linea]["empresa"] = empresa
        lineas_scraper[linea]["rutas"].append({
            "sentido": sentido,
            "geometry": row['geometry']
        })
    
    print(f"   ✓ Líneas únicas en scraper: {len(lineas_scraper)}")
    
    # Conteo por empresa
    empresas_count = defaultdict(int)
    for linea, data in lineas_scraper.items():
        empresas_count[data["empresa"]] += 1
    
    print("\n   Líneas por operador (2026 real):")
    for emp, count in sorted(empresas_count.items()):
        print(f"     {emp}: {count} líneas")
    
    # Generar JSONs integrados
    print("\n4. Generando archivos JSON integrados...")
    report = []
    report.append("# Reporte de Fuentes de Datos - Actualización 2026\n")
    report.append(f"Total líneas en scraper 2026: {len(lineas_scraper)}\n")
    report.append(f"Total líneas en GTFS 2023: {len(lineas_2023)}\n\n")
    report.append("| Línea | Fuente | Operador 2026 | Operador 2023 | Notas |\n")
    report.append("|-------|--------|---------------|---------------|-------|\n")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lineas_procesadas = []
    
    # Procesar líneas del scraper 2026
    for linea, scraper_data in sorted(lineas_scraper.items()):
        numero_original = linea
        numero_final = linea
        
        # Aplicar renombramiento si aplica
        if linea in RENOMBRAMIENTOS:
            numero_final = RENOMBRAMIENTOS[linea]
            nota_renombre = f"Renombrada de {linea} a {numero_final}"
        else:
            nota_renombre = ""
        
        empresa_2026 = scraper_data["empresa"]
        empresa_2023 = lineas_2023.get(numero_original, {}).get('empresa', 'N/A')
        
        # Extraer paradas
        paradas_principales = extract_paradas_from_gdf(paradas_gdf, linea)
        
        # Crear JSON
        json_data = {
            "numero": numero_final,
            "nombre": f"Línea {numero_final}",
            "esEjemplo": False,
            "empresa": empresa_2026,
            "descripcionCorta": f"Línea {numero_final} - {empresa_2026}",
            "recorrido": {
                "ida": {
                    "descripcion": "Datos del scraper Tu Bondi 2026",
                    "calles": []  # Requiere procesamiento geométrico adicional
                },
                "vuelta": {
                    "descripcion": "Datos del scraper Tu Bondi 2026",
                    "calles": []
                }
            },
            "paradasPrincipales": paradas_principales,
            "horarios": {
                "lunesAViernes": {
                    "tipo": "frecuencia",
                    "descripcion": "Consultá horarios en la app Tu Bondi",
                    "horarioInicio": "",
                    "horarioFin": ""
                },
                "sabados": {
                    "tipo": "frecuencia",
                    "descripcion": "Consultá horarios en la app Tu Bondi",
                    "horarioInicio": "",
                    "horarioFin": ""
                },
                "domingosYFeriados": {
                    "tipo": "frecuencia",
                    "descripcion": "Consultá horarios en la app Tu Bondi",
                    "horarioInicio": "",
                    "horarioFin": ""
                }
            },
            "tarifas": {
                "efectivo": "Consultá la tarifa vigente en el sitio de la Municipalidad de Córdoba",
                "redBus": "Consultá descuentos disponibles con tarjeta Red Bus"
            },
            "mapsEmbedUrl": "",
            "ultimaActualizacion": "2026-08-07",
            "fuente": "Tu Bondi (Municipalidad de Córdoba) via scraper lineas_transporte_cba (MIT) - Agosto 2026",
            "notas": f"Datos obtenidos del scraper Tu Bondi/Micronauta agosto 2026. {nota_renombre}".strip()
        }
        
        filename = f"linea-{numero_final}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        lineas_procesadas.append(numero_final)
        
        # Agregar a reporte
        fuente = "Scraper 2026"
        cambio_empresa = "✓" if empresa_2026 != empresa_2023 else ""
        notas_reporte = f"{nota_renombre} {cambio_empresa}".strip()
        report.append(f"| {numero_final} | {fuente} | {empresa_2026} | {empresa_2023} | {notas_reporte} |\n")
    
    # Procesar líneas que están en GTFS 2023 pero NO en scraper (fallback)
    print("\n5. Procesando líneas con fallback a GTFS 2023...")
    lineas_fallback = 0
    
    for numero_2023, data_2023 in sorted(lineas_2023.items()):
        # Si ya está en scraper, skip
        if numero_2023 in lineas_scraper:
            continue
        
        # Si fue renombrada, skip (ya está con nuevo nombre)
        if numero_2023 in RENOMBRAMIENTOS:
            continue
        
        # Mantener datos de 2023
        data_2023['notas'] = f"Datos de GTFS 2023 (no disponibles en scraper 2026). {data_2023.get('notas', '')}".strip()
        data_2023['fuente'] = "GTFS Municipalidad de Córdoba 2023 (fallback)"
        
        filename = f"linea-{numero_2023}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_2023, f, ensure_ascii=False, indent=2)
        
        lineas_procesadas.append(numero_2023)
        lineas_fallback += 1
        
        report.append(f"| {numero_2023} | GTFS 2023 (fallback) | {data_2023.get('empresa', 'N/A')} | {data_2023.get('empresa', 'N/A')} | No en scraper 2026 |\n")
    
    print(f"   ✓ Líneas con fallback GTFS 2023: {lineas_fallback}")
    
    # Guardar reporte
    print("\n6. Generando reporte...")
    report.append(f"\n## Resumen\n")
    report.append(f"- **Líneas del scraper 2026**: {len(lineas_scraper)}\n")
    report.append(f"- **Líneas fallback GTFS 2023**: {lineas_fallback}\n")
    report.append(f"- **Total líneas**: {len(lineas_procesadas)}\n")
    report.append(f"- **Renombramientos aplicados**: {len(RENOMBRAMIENTOS)}\n")
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(report)
    
    print(f"   ✓ Reporte guardado: {REPORT_FILE}")
    
    print("\n" + "="*70)
    print("INTEGRACIÓN COMPLETADA")
    print("="*70)
    print(f"Total líneas procesadas: {len(lineas_procesadas)}")
    print(f"  - Desde scraper 2026: {len(lineas_scraper)}")
    print(f"  - Fallback GTFS 2023: {lineas_fallback}")
    
    return True

if __name__ == "__main__":
    success = integrate_data()
    exit(0 if success else 1)
