# Sistema de Diseño - Bondi Córdoba

## Introducción

Este documento define el sistema de diseño visual y de experiencia de usuario para bondicordoba.com.ar, un sitio de información sobre líneas de transporte público de Córdoba Capital.

## Principios de Diseño

1. **Claridad**: La información debe ser fácil de encontrar y entender
2. **Accesibilidad**: Cumplimiento WCAG AA, navegación con teclado, semántica HTML
3. **Performance**: Core Web Vitals óptimos, sin layout shifts
4. **Mobile-First**: Diseño priorizado para dispositivos móviles
5. **Profesionalismo**: Estética moderna y confiable

## Paleta de Colores

### Colores Principales

| Color | Token | Hex | Uso |
|-------|-------|-----|-----|
| Primary | `--color-primary` | `#0066CC` | Acciones principales, enlaces |
| Primary Dark | `--color-primary-dark` | `#004A99` | Hover estados, énfasis |
| Primary Light | `--color-primary-light` | `#E6F2FF` | Fondos sutiles, badges |

### Colores Neutrales

| Color | Token | Hex | Contraste |
|-------|-------|-----|-----------|
| Gray 900 | `--color-gray-900` | `#1A1A1A` | 15.2:1 |
| Gray 800 | `--color-gray-800` | `#333333` | 12.6:1 |
| Gray 700 | `--color-gray-700` | `#4D4D4D` | 9.1:1 |
| Gray 600 | `--color-gray-600` | `#666666` | 5.7:1 |
| Gray 500 | `--color-gray-500` | `#808080` | 3.9:1 |
| Gray 400 | `--color-gray-400` | `#999999` | 2.8:1 |
| Gray 300 | `--color-gray-300` | `#CCCCCC` | 1.6:1 |
| Gray 200 | `--color-gray-200` | `#E5E5E5` | 1.3:1 |
| Gray 100 | `--color-gray-100` | `#F5F5F5` | 1.1:1 |
| White | `--color-white` | `#FFFFFF` | 1:1 |

### Colores Semánticos

| Color | Token | Hex | Uso |
|-------|-------|-----|-----|
| Success | `--color-success` | `#059669` | Confirmaciones, estados activos |
| Warning | `--color-warning` | `#D97706` | Advertencias, pendientes |
| Error | `--color-error` | `#DC2626` | Errores, información crítica |
| Info | `--color-info` | `#0284C7` | Información adicional |

Todos los colores cumplen con WCAG AA (ratio ≥ 4.5:1 para texto normal, ≥ 3:1 para texto grande).

## Tipografía

### Fuentes

- **Encabezados**: [Outfit](https://fonts.google.com/specimen/Outfit) - Geométrica, moderna, clara
- **Cuerpo**: [Inter](https://rsms.me/inter/) - Optimizada para legibilidad en pantalla

Ambas fuentes se auto-hospedan vía `@fontsource` para mejor performance y privacidad.

### Escala Tipográfica

Escala modular con ratio 1.250 (Major Third):

| Nivel | Token | Tamaño | Uso |
|-------|-------|--------|-----|
| Display | `--font-size-display` | 3.052rem (48.8px) | Hero principal |
| H1 | `--font-size-h1` | 2.441rem (39px) | Título de página |
| H2 | `--font-size-h2` | 1.953rem (31.2px) | Secciones principales |
| H3 | `--font-size-h3` | 1.563rem (25px) | Subsecciones |
| H4 | `--font-size-h4` | 1.25rem (20px) | Títulos menores |
| Base | `--font-size-base` | 1rem (16px) | Texto de cuerpo |
| Small | `--font-size-small` | 0.875rem (14px) | Metadatos, ayuda |
| XSmall | `--font-size-xsmall` | 0.75rem (12px) | Labels, disclaimer |

### Pesos de Fuente

- Regular: 400 (texto de cuerpo)
- Medium: 500 (énfasis sutil)
- Semibold: 600 (encabezados, botones)
- Bold: 700 (énfasis fuerte)

### Line Height

- Encabezados: 1.2
- Cuerpo: 1.6
- Compacto (tablas): 1.4

## Espaciado

Sistema de espaciado con base 4px:

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` | 0.25rem (4px) | Separación mínima |
| `--space-2` | 0.5rem (8px) | Padding pequeño |
| `--space-3` | 0.75rem (12px) | Padding interno |
| `--space-4` | 1rem (16px) | Espacio estándar |
| `--space-5` | 1.25rem (20px) | Padding medio |
| `--space-6` | 1.5rem (24px) | Secciones pequeñas |
| `--space-8` | 2rem (32px) | Secciones medianas |
| `--space-10` | 2.5rem (40px) | Secciones grandes |
| `--space-12` | 3rem (48px) | Separación de bloques |
| `--space-16` | 4rem (64px) | Separación principal |

## Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-sm` | 0.25rem (4px) | Badges, tags |
| `--radius-md` | 0.5rem (8px) | Botones, inputs, cards |
| `--radius-lg` | 0.75rem (12px) | Cards grandes |
| `--radius-xl` | 1rem (16px) | Elementos destacados |
| `--radius-full` | 9999px | Elementos circulares |

## Sombras

Sombras sutiles para jerarquía visual:

| Token | Valor | Uso |
|-------|-------|-----|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Hover sutil |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Cards, botones elevados |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modales, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Elementos flotantes |

## Layout

### Contenedor Principal

- **Max-width**: 1280px
- **Padding lateral**: 1rem (móvil), 2rem (tablet+)
- **Centrado**: `margin: 0 auto`

### Breakpoints

| Nombre | Token | Valor | Uso |
|--------|-------|-------|-----|
| Mobile | `--bp-sm` | 640px | Teléfonos grandes |
| Tablet | `--bp-md` | 768px | Tablets |
| Desktop | `--bp-lg` | 1024px | Laptops |
| Desktop XL | `--bp-xl` | 1280px | Monitores grandes |

### Grid

- **Sistema**: CSS Grid / Flexbox según necesidad
- **Gaps**: var(--space-4) a var(--space-6)
- **Columnas móvil**: 1
- **Columnas tablet**: 2-3
- **Columnas desktop**: 3-4

## Iconografía

Librería: **Lucide Icons** (vía astro-icon)

- Tamaño estándar: 20px
- Tamaño grande: 24px
- Stroke width: 2px
- Color: Heredado del texto

**Prohibido**: No se usan emojis en ninguna parte del sitio.

## Componentes

### Header

- Fondo: blanco con sombra sutil
- Sticky en scroll
- Logo + navegación + búsqueda
- Menú hamburguesa en móvil

### Footer

- Fondo: var(--color-gray-100)
- Links útiles
- Copyright
- Disclaimer de responsabilidad

### Cards de Líneas

- Border radius: var(--radius-md)
- Sombra: var(--shadow-sm), hover var(--shadow-md)
- Número de línea destacado
- Recorrido resumido
- Link de toda la card

### Tablas

- Bordes sutiles (var(--color-gray-300))
- Zebra striping en filas (var(--color-gray-50))
- Responsive: scroll horizontal en móvil
- Headers sticky opcionales

### Botones

- Padding: var(--space-3) var(--space-5)
- Border radius: var(--radius-md)
- Font weight: 600
- Transiciones suaves (150ms)
- Estados: default, hover, active, disabled, focus

### Badges

- Tamaño pequeño
- Border radius: var(--radius-sm)
- Colores semánticos según estado

### Estados Vacíos/Pendientes

- Icono ilustrativo
- Mensaje claro
- Acción sugerida (si aplica)
- Sin dramatismos

### Slots de Ads

- Claramente separados visualmente
- Espacio reservado con min-height
- No causan layout shift
- Label "Publicidad" cuando corresponda

## Accesibilidad

### Semántica HTML

- Headers jerárquicos (h1 > h2 > h3)
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`
- Listas para navegación (`<ul>`, `<li>`)
- Tablas para datos tabulares

### Focus States

- Outline visible (var(--color-primary))
- Skip to main content
- Tab order lógico

### ARIA

- Labels descriptivos
- aria-current en navegación
- aria-label cuando el texto visual no es suficiente
- Role attributes cuando sea necesario

### Contraste

- Todos los textos: ≥ 4.5:1 (AA)
- Textos grandes (≥18px): ≥ 3:1
- Componentes interactivos: ≥ 3:1

## Performance

### Estrategias

- Fuentes auto-hospedadas con preload
- CSS crítico inline
- Lazy loading de imágenes
- Minificación y compresión
- Cache apropiado

### Core Web Vitals Objetivos

- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Ads Sin Layout Shift

- Espacio reservado con dimensiones fijas
- Contenedor con min-height
- Carga asíncrona
- Placeholder visual opcional

## Tono y Voz

- **Informal pero profesional**: Voseo argentino ("podés", "encontrá")
- **Claro y directo**: Sin jerga innecesaria
- **Útil**: Foco en la información que el usuario necesita
- **Humano**: Sin corporativismo ni robótico

## Mensajes de Error/Estados

### Datos Pendientes

- "Información pendiente"
- "Próximamente disponible"
- "En actualización"

### Sin Resultados

- "No encontramos líneas con ese criterio"
- "Probá con otro número o recorrido"

### 404

- "Esta página no existe"
- "Volvé al inicio o buscá tu línea"

## Notas de Implementación

- Los tokens CSS están definidos en `src/styles/tokens.css`
- Los estilos globales en `src/styles/global.css`
- Componentes Astro reutilizables en `src/components/`
- Mobile-first: escribir estilos base para móvil, luego media queries para desktop
- Evitar !important salvo casos excepcionales
- Preferir CSS moderno (Grid, Flexbox, custom properties)
