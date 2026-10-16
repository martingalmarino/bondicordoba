# Bondi Córdoba

Sitio web con información de las líneas de transporte público de Córdoba Capital.

## Datos

Los datos provienen del GTFS oficial de la Municipalidad de Córdoba, publicado en marzo de 2023.

- **Fuente:** [Portal de Gobierno Abierto de Córdoba](https://gobiernoabierto.cordoba.gob.ar/data/datos-abiertos/categoria/transporte-urbano/gtfs-de-la-ciudada-de-cordoba/3319)
- **Última actualización:** 16/03/2023
- **Total de líneas:** 79 líneas
- **Empresas:** Coniferal, ERSA, TAMSE

## Estructura del Proyecto

```
bondicordoba/
├── app/                      # Aplicación Next.js
│   ├── page.tsx             # Página principal
│   ├── layout.tsx           # Layout principal
│   ├── globals.css          # Estilos globales
│   ├── sitemap.ts           # Generador de sitemap
│   ├── robots.ts            # Archivo robots.txt
│   └── lineas/
│       └── [numero]/
│           └── page.tsx     # Páginas dinámicas de líneas
├── src/
│   └── data/
│       └── lineas/          # Datos JSON de las líneas
│           ├── index.json   # Índice de todas las líneas
│           └── linea-*.json # Datos de cada línea
├── scripts/
│   └── parse_gtfs.py        # Script para parsear GTFS
├── package.json
├── tsconfig.json
└── next.config.js

```

## Desarrollo

### Requisitos

- Node.js 18+
- npm o yarn

### Instalación

```bash
npm install
```

### Desarrollo

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

### Build

```bash
npm run build
```

### Exportar sitio estático

```bash
npm run export
```

## Procesamiento de Datos GTFS

Para actualizar los datos desde el GTFS:

1. Descarga el GTFS más reciente de la Municipalidad
2. Extrae el contenido en `/tmp/gtfs-cordoba/`
3. Ejecuta el script de parseo:

```bash
python3 scripts/parse_gtfs.py
```

Esto generará/actualizará los archivos JSON en `src/data/lineas/`.

## Licencia

Los datos son propiedad de la Municipalidad de Córdoba y están disponibles bajo licencia CC-BY-SA-AR (CBA).

Este sitio es no oficial y solo tiene fines informativos.

## Disclaimer

⚠️ **Importante:** Los recorridos y horarios pueden haber cambiado desde la última actualización del GTFS. 
Siempre verificá la información actualizada en:
- App oficial Tu Bondi
- Sitios web de las empresas operadoras
- Paradas y carteles oficiales
