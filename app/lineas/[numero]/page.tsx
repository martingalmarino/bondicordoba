import Link from 'next/link'
import { notFound } from 'next/navigation'
import indexData from '@/src/data/lineas/index.json'
import fs from 'fs'
import path from 'path'

interface LineaData {
  numero: string
  nombre: string
  empresa: string
  descripcionCorta: string
  recorrido: {
    ida: {
      descripcion: string
      calles: string[]
    }
    vuelta: {
      descripcion: string
      calles: string[]
    }
  }
  paradasPrincipales: string[]
  horarios: any[]
  tarifas: any[]
  mapsEmbedUrl: string
  ultimaActualizacion: string
  fuente: string
  notas: string
  esEjemplo: boolean
}

export async function generateStaticParams() {
  return indexData.lineas.map((linea) => ({
    numero: linea.numero,
  }))
}

export async function generateMetadata({ params }: { params: { numero: string } }) {
  const linea = indexData.lineas.find(l => l.numero === params.numero)
  
  if (!linea) {
    return {
      title: 'Línea no encontrada',
    }
  }

  return {
    title: `Línea ${linea.numero} - Bondi Córdoba`,
    description: `Información sobre la línea ${linea.numero} de ${linea.empresa} en Córdoba Capital`,
  }
}

function getLineaData(numero: string): LineaData | null {
  try {
    const filePath = path.join(process.cwd(), 'src', 'data', 'lineas', `linea-${numero}.json`)
    const fileContents = fs.readFileSync(filePath, 'utf8')
    return JSON.parse(fileContents)
  } catch {
    return null
  }
}

export default function LineaPage({ params }: { params: { numero: string } }) {
  const lineaData = getLineaData(params.numero)

  if (!lineaData) {
    notFound()
  }

  return (
    <>
      <header>
        <div className="container">
          <h1>🚌 Línea {lineaData.numero}</h1>
          <p style={{ textAlign: 'center', margin: '10px 0 0 0' }}>
            {lineaData.empresa}
          </p>
        </div>
      </header>

      <main className="container">
        <div className="linea-detail">
          <Link href="/" className="back-link">
            ← Volver al listado
          </Link>

          <div className="info-card">
            <h2>Información General</h2>
            <p><strong>Número:</strong> {lineaData.numero}</p>
            <p><strong>Nombre:</strong> {lineaData.nombre}</p>
            <p><strong>Empresa:</strong> {lineaData.empresa}</p>
            <p><strong>Descripción:</strong> {lineaData.descripcionCorta}</p>
          </div>

          <div className="info-card">
            <h2>Recorridos</h2>
            
            {lineaData.recorrido.ida.descripcion && (
              <div className="recorrido-section">
                <h3>📍 Recorrido de Ida</h3>
                <p><strong>{lineaData.recorrido.ida.descripcion}</strong></p>
                {lineaData.recorrido.ida.calles.length > 0 && (
                  <>
                    <p style={{ marginTop: '10px', marginBottom: '8px' }}>
                      <strong>Principales puntos del recorrido:</strong>
                    </p>
                    <ul className="calles-list">
                      {lineaData.recorrido.ida.calles.map((calle, idx) => (
                        <li key={idx}>{calle}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            )}

            {lineaData.recorrido.vuelta.descripcion && (
              <div className="recorrido-section">
                <h3>📍 Recorrido de Vuelta</h3>
                <p><strong>{lineaData.recorrido.vuelta.descripcion}</strong></p>
                {lineaData.recorrido.vuelta.calles.length > 0 && (
                  <>
                    <p style={{ marginTop: '10px', marginBottom: '8px' }}>
                      <strong>Principales puntos del recorrido:</strong>
                    </p>
                    <ul className="calles-list">
                      {lineaData.recorrido.vuelta.calles.map((calle, idx) => (
                        <li key={idx}>{calle}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            )}
          </div>

          {lineaData.paradasPrincipales.length > 0 && (
            <div className="info-card">
              <h2>Paradas Principales</h2>
              <ul className="paradas-list">
                {lineaData.paradasPrincipales.map((parada, idx) => (
                  <li key={idx}>
                    {idx + 1}. {parada}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="info-card">
            <h2>Horarios</h2>
            {lineaData.horarios.length > 0 ? (
              <div>
                {lineaData.horarios.map((horario: any, idx: number) => (
                  <div key={idx}>
                    <p><strong>{horario.dia}:</strong> {horario.horario}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">
                Información de horarios pendiente de confirmación. 
                Consultá los horarios en la app Tu Bondi o en las paradas.
              </p>
            )}
          </div>

          <div className="info-card">
            <h2>Tarifas</h2>
            {lineaData.tarifas.length > 0 ? (
              <div>
                {lineaData.tarifas.map((tarifa: any, idx: number) => (
                  <div key={idx}>
                    <p><strong>{tarifa.tipo}:</strong> ${tarifa.precio}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">
                Información de tarifas no disponible. Consultá las tarifas vigentes 
                con tu tarjeta SUBE o en las boleterías.
              </p>
            )}
          </div>

          <div className="disclaimer">
            ℹ️ {lineaData.notas}
          </div>

          <div className="info-card" style={{ marginTop: '20px', fontSize: '0.9rem', color: '#666' }}>
            <p><strong>Última actualización:</strong> {lineaData.ultimaActualizacion}</p>
            <p><strong>Fuente:</strong> <a href={lineaData.fuente} target="_blank" rel="noopener noreferrer">GTFS oficial Municipalidad de Córdoba</a></p>
          </div>
        </div>
      </main>

      <footer>
        <p>Datos abiertos de la Municipalidad de Córdoba</p>
        <p>Sitio no oficial - Solo con fines informativos</p>
      </footer>
    </>
  )
}
