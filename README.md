# BondiCórdoba

Portal informativo sobre líneas de colectivos en Córdoba Capital, Argentina.

🚌 **[Ver sitio en vivo](https://bondicordoba.com.ar)** (cuando esté deployado)

## Descripción

BondiCórdoba es un sitio web estático construido con Astro que proporciona información completa sobre las líneas de colectivos en Córdoba Capital. Incluye:

- 📍 Recorridos detallados de cada línea (ida y vuelta)
- 🕐 Horarios y frecuencias
- 🚏 Paradas principales
- 💳 Guías sobre tarjeta Red Bus y tarifas
- 🗺️ Información sobre cómo llegar a destinos populares
- 📰 Sección de novedades y avisos
- 💰 Preparado para monetización con Google AdSense

## Tecnologías utilizadas

- **[Astro](https://astro.build)** - Framework estático moderno
- **TypeScript** - Para tipado seguro
- **@astrojs/sitemap** - Generación automática de sitemap

## Requisitos

- Node.js 18.0.0 o superior
- npm o pnpm

## Instalación y desarrollo local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/bondicordoba.git
   cd bondicordoba
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Iniciar servidor de desarrollo**
   ```bash
   npm run dev
   ```
   
   El sitio estará disponible en `http://localhost:4321`

4. **Construir para producción**
   ```bash
   npm run build
   ```
   
   Los archivos se generarán en el directorio `dist/`

5. **Vista previa de la build de producción**
   ```bash
   npm run preview
   ```

## Estructura del proyecto

```
bondicordoba/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── AdSense.astro   # Componente de anuncios
│   │   ├── Breadcrumbs.astro
│   │   └── LineCard.astro  # Tarjeta de línea de colectivo
│   ├── data/
│   │   └── lineas/         # Archivos JSON con datos de líneas
│   ├── layouts/
│   │   └── BaseLayout.astro # Layout principal con SEO
│   ├── pages/              # Páginas del sitio (rutas automáticas)
│   │   ├── index.astro     # Página principal
│   │   ├── lineas/
│   │   │   ├── index.astro
│   │   │   └── [numero].astro # Página dinámica por línea
│   │   ├── como-llegar/    # Guías de destinos
│   │   ├── guias/          # Guías útiles
│   │   ├── novedades/      # Blog/noticias
│   │   └── *.astro         # Páginas legales
│   ├── utils/
│   │   └── lineas.ts       # Utilidades para cargar líneas
│   └── types.ts            # Tipos TypeScript
├── public/                 # Archivos estáticos
│   ├── robots.txt
│   └── ads.txt             # Configuración de AdSense
├── astro.config.mjs
├── package.json
└── README.md
```

## Agregar datos de líneas de colectivos

### Formato de datos

Los datos de cada línea se almacenan en archivos JSON individuales en `src/data/lineas/`.

**Ejemplo: `src/data/lineas/linea-10.json`**

```json
{
  "numero": "10",
  "nombre": "Línea 10 - Villa El Libertador - Arguello",
  "esEjemplo": false,
  "empresa": "Empresa de Transporte SA",
  "descripcionCorta": "Villa El Libertador - Centro - Arguello",
  "recorrido": {
    "ida": {
      "descripcion": "Desde Villa El Libertador hasta Arguello",
      "calles": [
        "Villa El Libertador - Terminal",
        "Av. Circunvalación",
        "Av. Cruz Roja",
        "Av. Colón",
        "Av. Rafael Núñez",
        "Av. Richieri",
        "Destino: Arguello"
      ]
    },
    "vuelta": {
      "descripcion": "Desde Arguello hasta Villa El Libertador",
      "calles": [
        "Arguello",
        "Av. Richieri",
        "Av. Rafael Núñez",
        "Av. Colón",
        "Av. Cruz Roja",
        "Av. Circunvalación",
        "Destino: Villa El Libertador"
      ]
    }
  },
  "paradasPrincipales": [
    "Villa El Libertador - Terminal",
    "Av. Colón y Cruz Roja",
    "Centro - Av. Colón",
    "Av. Rafael Núñez",
    "Arguello - Terminal"
  ],
  "horarios": {
    "lunesAViernes": {
      "tipo": "frecuencia",
      "descripcion": "Cada 12-18 minutos",
      "horarioInicio": "05:30",
      "horarioFin": "23:30"
    },
    "sabados": {
      "tipo": "frecuencia",
      "descripcion": "Cada 18-25 minutos",
      "horarioInicio": "06:00",
      "horarioFin": "23:00"
    },
    "domingosYFeriados": {
      "tipo": "frecuencia",
      "descripcion": "Cada 25-35 minutos",
      "horarioInicio": "07:00",
      "horarioFin": "22:00"
    }
  },
  "tarifas": {
    "efectivo": "Ver tarifas vigentes en TAMSE",
    "redBus": "Descuento aplicado automáticamente"
  },
  "mapsEmbedUrl": "",
  "ultimaActualizacion": "2026-10-16",
  "fuente": "TAMSE - Municipalidad de Córdoba",
  "notas": ""
}
```

### Campos del JSON

- **numero**: Número de la línea (string)
- **nombre**: Nombre completo de la línea
- **esEjemplo**: `true` si son datos de ejemplo, `false` para datos reales
- **empresa**: Nombre de la empresa operadora
- **descripcionCorta**: Descripción breve del recorrido
- **recorrido**: Objeto con `ida` y `vuelta`, cada uno con descripción y array de calles
- **paradasPrincipales**: Array con las paradas más importantes
- **horarios**: Objeto con `lunesAViernes`, `sabados` y `domingosYFeriados`
  - **tipo**: "frecuencia" u "horarios"
  - **descripcion**: Frecuencia o cantidad de servicios
  - **horarioInicio/Fin**: Hora de primer y último servicio
- **tarifas**: Información sobre tarifas en efectivo y Red Bus
- **mapsEmbedUrl**: (Opcional) URL de iframe de Google Maps
- **ultimaActualizacion**: Fecha en formato YYYY-MM-DD
- **fuente**: Fuente de la información
- **notas**: (Opcional) Notas adicionales o advertencias

### Agregar una nueva línea

1. Crear un nuevo archivo en `src/data/lineas/` (ej: `linea-50.json`)
2. Completar el JSON con la información de la línea
3. El sitio generará automáticamente la página en la próxima build

### Fuentes de datos oficiales

Para obtener información actualizada:

- **TAMSE**: [tamse.gob.ar](https://tamse.gob.ar)
- **Municipalidad de Córdoba**: [cordoba.gob.ar](https://www.cordoba.gob.ar)

## Configuración de Google AdSense

### 1. Obtener el ID de cliente de AdSense

1. Crea una cuenta en [Google AdSense](https://www.google.com/adsense/)
2. Obtén tu ID de editor (formato: `ca-pub-XXXXXXXXXXXXXXXX`)

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
PUBLIC_ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
PUBLIC_ADSENSE_SLOT_ID=YYYYYYYYYY
```

### 3. Actualizar ads.txt

Edita `public/ads.txt` con tu información:

```
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

### 4. Habilitar anuncios

Los anuncios están deshabilitados por defecto. Para habilitarlos, pasa `enabled={true}` al componente:

```astro
<AdSense enabled={true} />
```

### 5. Agregar script de AdSense

Agrega el script en `src/layouts/BaseLayout.astro` dentro del `<head>`:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

## Deploy

El sitio puede ser deployado en cualquier plataforma de hosting estático:

### Vercel

1. Instala Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel`
3. Para producción: `vercel --prod`

O conecta tu repositorio de GitHub directamente en [vercel.com](https://vercel.com)

### Netlify

1. Conecta tu repositorio en [netlify.com](https://netlify.com)
2. Configuración de build:
   - Build command: `npm run build`
   - Publish directory: `dist`

### Cloudflare Pages

1. Conecta tu repositorio en [pages.cloudflare.com](https://pages.cloudflare.com)
2. Configuración de build:
   - Build command: `npm run build`
   - Build output directory: `dist`

## SEO

El sitio incluye:

- ✅ Meta tags optimizados (title, description)
- ✅ Open Graph para redes sociales
- ✅ Twitter Cards
- ✅ URLs canónicas
- ✅ Sitemap.xml automático
- ✅ robots.txt
- ✅ JSON-LD (Structured Data)
- ✅ Breadcrumbs con Schema.org

## Performance

- ✅ Renderizado estático (SSG)
- ✅ CSS inline automático
- ✅ Compresión HTML
- ✅ JavaScript mínimo
- ✅ Mobile-first responsive
- ✅ Lazy loading de imágenes

## Licencia

Este proyecto está disponible bajo licencia MIT. Los datos de líneas de colectivos son de dominio público o recopilados de fuentes oficiales.

## Disclaimer

⚠️ **Este no es un sitio oficial**. BondiCórdoba es un proyecto independiente y no está afiliado con la Municipalidad de Córdoba, TAMSE, ni ninguna empresa de transporte. 

Para información oficial, consultar:
- **Municipalidad de Córdoba**: [cordoba.gob.ar](https://www.cordoba.gob.ar)
- **TAMSE**: [tamse.gob.ar](https://tamse.gob.ar)

## Contribuir

Si encontrás información desactualizada o querés contribuir:

1. Fork del repositorio
2. Creá una branch con tu cambio
3. Hacé commit de los cambios
4. Push a la branch
5. Abrí un Pull Request

## Contacto

Para consultas o sugerencias, usá la [página de contacto](https://bondicordoba.com.ar/contacto) del sitio.

---

Hecho con ❤️ para la comunidad de Córdoba
