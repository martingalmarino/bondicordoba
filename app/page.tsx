import Link from 'next/link'
import indexData from '@/src/data/lineas/index.json'

export default function Home() {
  const lineas = indexData.lineas.sort((a, b) => {
    const aNum = parseInt(a.numero.replace(/\D/g, '')) || 0
    const bNum = parseInt(b.numero.replace(/\D/g, '')) || 0
    return aNum - bNum
  })

  const empresas = Array.from(new Set(lineas.map(l => l.empresa)))

  return (
    <>
      <header>
        <div className="container">
          <h1>🚌 Bondi Córdoba</h1>
          <p style={{ textAlign: 'center', margin: '10px 0 0 0' }}>
            Líneas de transporte público de Córdoba Capital
          </p>
        </div>
      </header>

      <main className="container">
        <div className="info-card">
          <h2>Información General</h2>
          <p>
            <strong>Total de líneas:</strong> {indexData.totalLineas} líneas
          </p>
          <p>
            <strong>Empresas operadoras:</strong> {empresas.join(', ')}
          </p>
          <p>
            <strong>Última actualización de datos:</strong> {indexData.ultimaActualizacion}
          </p>
          <p>
            <strong>Fuente:</strong> {indexData.fuente}
          </p>
        </div>

        <div className="disclaimer">
          ⚠️ <strong>Importante:</strong> Los datos provienen del GTFS oficial de la Municipalidad 
          de Córdoba (marzo 2023). Los recorridos y horarios pueden haber cambiado. 
          Verificá la información actualizada en la app Tu Bondi.
        </div>

        <h2 style={{ marginTop: '30px' }}>Todas las Líneas</h2>
        <div className="lineas-grid">
          {lineas.map((linea) => (
            <Link 
              href={`/lineas/${linea.numero}`} 
              key={linea.archivo}
              className="linea-card"
            >
              <div className="linea-numero">Línea {linea.numero}</div>
              <div className="linea-nombre">{linea.nombre}</div>
              <div className="linea-empresa">{linea.empresa}</div>
            </Link>
          ))}
        </div>
      </main>

      <footer>
        <p>Datos abiertos de la Municipalidad de Córdoba</p>
        <p>Sitio no oficial - Solo con fines informativos</p>
      </footer>
    </>
  )
}
