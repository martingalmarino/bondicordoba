import { MetadataRoute } from 'next'
import indexData from '@/src/data/lineas/index.json'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://bondicordoba.com'
  
  const lineasUrls = indexData.lineas.map((linea) => ({
    url: `${baseUrl}/lineas/${linea.numero}`,
    lastModified: new Date(indexData.ultimaActualizacion),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...lineasUrls,
  ]
}
