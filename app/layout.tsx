import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Bondi Córdoba - Líneas de Transporte',
  description: 'Información actualizada de las líneas de transporte público de Córdoba Capital',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
