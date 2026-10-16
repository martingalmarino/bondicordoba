#!/usr/bin/env python3
import json, os, re, geopandas as gpd

SCRAPER_PARADAS = "/tmp/lineas_transporte_cba/paradas_cordoba.gpkg"
DATA_DIR = "/workspace/src/data/lineas"
DATA_2023 = "/tmp/lineas_backup_2023"

def extract_street(p):
    if not p: return None
    m = re.match(r'^(.+?)\s+\d+', p)
    return m.group(1).strip() if m else p.strip()

def get_streets(gdf, linea, sentido):
    ps = gdf[(gdf['linea_nombre'] == linea) & (gdf['sentido_txt'] == sentido)].sort_values('orden')
    if len(ps) == 0: return [], []
    
    nombres = ps['parada_nombre'].tolist()
    calles = [extract_street(p) for p in nombres]
    
    # Dedup consecutive
    dedup = []
    prev = None
    for c in calles:
        if c and c != prev:
            dedup.append(c)
            prev = c
    
    # Paradas principales
    step = max(1, len(nombres) // 8)
    indices = list(range(0, len(nombres), step))
    if len(nombres) - 1 not in indices:
        indices.append(len(nombres) - 1)
    principales = [nombres[i] for i in indices]
    
    return dedup, principales

print("Extrayendo recorridos...")
paradas = gpd.read_file(SCRAPER_PARADAS)
lineas = sorted(paradas['linea_nombre'].unique())

stats = {'completo': 0, 'parcial': 0, 'fallback': 0, 'sin_datos': 0}
report = []

renom = {"A1": "36A", "B1": "81B", "C1": "10C", "C2": "B10"}

for ln in lineas:
    num = renom.get(ln, ln)
    fp = f"{DATA_DIR}/linea-{num}.json"
    
    if not os.path.exists(fp):
        stats['sin_datos'] += 1
        continue
    
    with open(fp) as f: data = json.load(f)
    
    ci, pi = get_streets(paradas, ln, 'Ida')
    cv, pv = get_streets(paradas, ln, 'Vuelta')
    
    if not ci and not cv:
        # Fallback 2023
        fp23 = f"{DATA_2023}/linea-{ln}.json"
        if os.path.exists(fp23):
            with open(fp23) as f: d23 = json.load(f)
            ci23 = d23.get('recorrido', {}).get('ida', {}).get('calles', [])
            cv23 = d23.get('recorrido', {}).get('vuelta', {}).get('calles', [])
            if ci23 or cv23:
                data['recorrido']['ida']['calles'] = ci23
                data['recorrido']['ida']['descripcion'] = "Recorrido desde GTFS 2023 (fallback)"
                data['recorrido']['vuelta']['calles'] = cv23
                data['recorrido']['vuelta']['descripcion'] = "Recorrido desde GTFS 2023 (fallback)"
                data['notas'] = f"{data.get('notas', '')} Recorrido de GTFS 2023.".strip()
                stats['fallback'] += 1
                report.append(f"{num}: Fallback 2023 ({len(ci23)}/{len(cv23)})")
            else:
                stats['sin_datos'] += 1
                report.append(f"{num}: Sin datos")
        else:
            stats['sin_datos'] += 1
            report.append(f"{num}: Sin datos")
    else:
        if ci:
            data['recorrido']['ida']['calles'] = ci
            data['recorrido']['ida']['descripcion'] = f"Por {', '.join(ci[:5])}{'...' if len(ci) > 5 else ''}"
        if cv:
            data['recorrido']['vuelta']['calles'] = cv
            data['recorrido']['vuelta']['descripcion'] = f"Por {', '.join(cv[:5])}{'...' if len(cv) > 5 else ''}"
        
        # Combinar paradas
        comb = []
        for i in range(max(len(pi), len(pv))):
            if i < len(pi) and len(comb) < 8: comb.append(pi[i])
            if i < len(pv) and len(comb) < 8: comb.append(pv[i])
        
        seen = set()
        dedup_p = []
        for p in comb:
            if p not in seen:
                dedup_p.append(p)
                seen.add(p)
        
        data['paradasPrincipales'] = dedup_p[:8]
        
        if ci and cv:
            stats['completo'] += 1
            report.append(f"{num}: ✓ Completo ({len(ci)}/{len(cv)} calles)")
        else:
            stats['parcial'] += 1
            report.append(f"{num}: Parcial ({len(ci)}/{len(cv)})")
    
    # Notas especiales
    if num in ['21', '25']:
        nota = "Tu Bondi lista Coniferal; Municipalidad indica corredor 2 (Tamsau). Dato de Tu Bondi."
        if nota not in data.get('notas', ''):
            data['notas'] = f"{data.get('notas', '')} {nota}".strip()
    
    with open(fp, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nCompleto: {stats['completo']}, Parcial: {stats['parcial']}, Fallback: {stats['fallback']}, Sin datos: {stats['sin_datos']}")
for r in report:
    print(f"  {r}")

with open('/workspace/recorridos_coverage.txt', 'w') as f:
    f.write("COBERTURA RECORRIDOS\n" + "="*60 + "\n")
    for r in report:
        f.write(r + "\n")
    f.write(f"\n{'='*60}\n")
    f.write(f"Completo: {stats['completo']}\nParcial: {stats['parcial']}\nFallback: {stats['fallback']}\nSin datos: {stats['sin_datos']}\n")
