# Informe de Implementación: Datos GTFS Reales de Córdoba

## Resumen Ejecutivo

Se ha completado exitosamente la implementación de datos reales del GTFS oficial de la Municipalidad de Córdoba, reemplazando los datos de ejemplo del proyecto.

---

## 📊 Estadísticas Generales

- **Total de líneas cargadas:** 71
- **Total de archivos JSON generados:** 72 (71 líneas + 1 índice)
- **Fecha de datos GTFS:** 16 de marzo de 2023
- **Fuente oficial:** [Portal de Gobierno Abierto de Córdoba](https://gobiernoabierto.cordoba.gob.ar/data/datos-abiertos/categoria/transporte-urbano/gtfs-de-la-ciudada-de-cordoba/3319)

---

## 🚌 Líneas por Empresa Operadora

### Coniferal - 22 líneas
```
10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 34, 60, 61, 62, 63, 64, 65, 66, 67, 68, B60
```

### ERSA - 25 líneas  
```
20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 40, 41, 42, 43, 44, 45, 50, 51, 52, 70, 71, 72, 73, 74, 75
```

### TAMSE - 24 líneas
```
31, 32, 33, 35, 36, 53, 54, 80, 81, 82, 83, 84, 85, 600, 601, A, A1, B, B1, B80, C, C1, C2, AEROBUS (322)
```

---

## ✅ Campos Completados (100% derivados del GTFS)

| Campo | Cobertura | Descripción |
|-------|-----------|-------------|
| **Información básica** | 71/71 (100%) | Número, nombre, empresa |
| **Recorrido IDA** | 70/71 (98%) | Descripción y calles del recorrido de ida |
| **Recorrido VUELTA** | 70/71 (98%) | Descripción y calles del recorrido de vuelta |
| **Paradas principales** | 71/71 (100%) | Lista de paradas más importantes |
| **esEjemplo** | 71/71 (100%) | Marcado como `false` (datos reales) |
| **fuente** | 71/71 (100%) | URL del GTFS oficial |
| **ultimaActualizacion** | 71/71 (100%) | Fecha 2023-03-16 |
| **notas** | 71/71 (100%) | Disclaimer sobre antigüedad |

---

## ⚠️ Campos Vacíos (no disponibles en GTFS)

### Horarios (0/71 - 0%)
**Razón:** El GTFS incluye `stop_times` pero estos datos no son confiables para mostrar horarios específicos de salida sin una validación adicional con las empresas operadoras.

**Solución implementada:** Se muestra el mensaje:
> "Información de horarios pendiente de confirmación. Consultá los horarios en la app Tu Bondi o en las paradas."

### Tarifas (0/71 - 0%)
**Razón:** Las tarifas no están incluidas en el GTFS oficial. Además, las tarifas del transporte público varían según el tipo de tarjeta SUBE y descuentos aplicables.

**Solución implementada:** Se muestra el mensaje:
> "Información de tarifas no disponible. Consultá las tarifas vigentes con tu tarjeta SUBE o en las boleterías."

### URLs de Google Maps
**Estado:** Generadas como placeholders que requieren una API key válida de Google Maps.

**Acción requerida:** Para activar los mapas embebidos, se debe:
1. Obtener una API key de Google Maps
2. Reemplazar `YOUR_API_KEY` en el campo `mapsEmbedUrl` de cada línea
3. Alternativamente, usar un servicio de mapas alternativo (OpenStreetMap, Mapbox, etc.)

---

## 🏗️ Estructura del Proyecto

```
bondicordoba/
├── src/data/lineas/
│   ├── index.json              # Índice con las 71 líneas
│   ├── linea-10.json           # Línea 10 (Coniferal)
│   ├── linea-11.json           # Línea 11 (Coniferal)
│   └── ...                     # 71 archivos de líneas
├── app/
│   ├── page.tsx                # Página principal con listado
│   ├── lineas/[numero]/
│   │   └── page.tsx            # Páginas dinámicas de líneas
│   ├── sitemap.ts              # Generador de sitemap (72 URLs)
│   └── robots.ts               # Archivo robots.txt
├── scripts/
│   └── parse_gtfs.py           # Script de procesamiento GTFS
└── ...
```

---

## 🔍 Detalles Técnicos

### Esquema JSON de cada Línea

```json
{
  "numero": "31",
  "nombre": "Línea 31",
  "empresa": "TAMSE",
  "descripcionCorta": "Línea 31 - TAMSE",
  "recorrido": {
    "ida": {
      "descripcion": "Punto A - Punto B",
      "calles": ["Calle 1", "Calle 2", ...]
    },
    "vuelta": {
      "descripcion": "Punto B - Punto A",
      "calles": ["Calle 3", "Calle 4", ...]
    }
  },
  "paradasPrincipales": ["Parada 1", "Parada 2", ...],
  "horarios": [],
  "tarifas": [],
  "mapsEmbedUrl": "https://www.google.com/maps/embed/v1/directions?...",
  "ultimaActualizacion": "2023-03-16",
  "fuente": "https://gobiernoabierto.cordoba.gob.ar/...",
  "notas": "Datos del GTFS oficial de la Municipalidad de Córdoba (2023); el recorrido puede haber cambiado. Verificá en la app Tu Bondi.",
  "esEjemplo": false
}
```

### Build y Deploy

- **Framework:** Next.js 14 con generación de sitios estáticos
- **Páginas generadas:** 72 (1 principal + 71 de líneas)
- **Sitemap:** ✅ Generado automáticamente
- **Build:** ✅ Exitoso (con advertencia menor no crítica)

---

## ⚠️ Disclaimers Implementados

### En la página principal:
> ⚠️ **Importante:** Los datos provienen del GTFS oficial de la Municipalidad de Córdoba (marzo 2023). Los recorridos y horarios pueden haber cambiado. Verificá la información actualizada en la app Tu Bondi.

### En cada página de línea:
> ℹ️ Datos del GTFS oficial de la Municipalidad de Córdoba (2023); el recorrido puede haber cambiado. Verificá en la app Tu Bondi.

### Footer (todas las páginas):
> Datos abiertos de la Municipalidad de Córdoba  
> Sitio no oficial - Solo con fines informativos

---

## 📝 Reglas Seguidas

✅ **NUNCA inventar datos** - Todos los datos provienen directamente del GTFS  
✅ **Solo campos derivables** - Solo se completaron campos con información verificable  
✅ **Empresas desde agency** - Nombres de empresas desde `agency.txt`  
✅ **Horarios vacíos** - No derivables con certeza, se dejaron vacíos con mensaje  
✅ **Tarifas vacías** - No disponibles en GTFS, se dejaron vacías con mensaje  
✅ **esEjemplo: false** - Todas las líneas marcadas como datos reales  
✅ **Fuente correcta** - URL del GTFS oficial en todos los archivos  
✅ **Fecha correcta** - ultimaActualizacion con fecha del GTFS (2023-03-16), no fecha actual  
✅ **Disclaimers visibles** - Advertencias sobre antigüedad de datos en todas las páginas  
✅ **Build funcional** - El sitio compila y genera páginas estáticas correctamente  

---

## 🔗 Enlaces

- **Pull Request:** [#2 - Reemplazar datos de ejemplo con GTFS real](https://github.com/martingalmarino/bondicordoba/pull/2)
- **Fuente de datos:** [GTFS Oficial Municipalidad de Córdoba](https://gobiernoabierto.cordoba.gob.ar/data/datos-abiertos/categoria/transporte-urbano/gtfs-de-la-ciudada-de-cordoba/3319)
- **Licencia de datos:** CC-BY-SA-AR (CBA)

---

## ✨ Próximos Pasos (Opcional)

1. **Horarios:** Contactar con empresas operadoras para obtener horarios oficiales actualizados
2. **Tarifas:** Integrar información oficial de tarifas SUBE
3. **Mapas:** Obtener API key de Google Maps o migrar a OpenStreetMap
4. **Actualización:** Cuando haya un GTFS más reciente, ejecutar `scripts/parse_gtfs.py` nuevamente
5. **Imágenes:** Agregar fotos de las unidades de cada empresa
6. **Tiempo real:** Integrar APIs de seguimiento en tiempo real si están disponibles

---

**Fecha de implementación:** 16 de octubre de 2026  
**Estado:** ✅ Completado  
**Datos GTFS:** Marzo 2023 (Municipalidad de Córdoba)
