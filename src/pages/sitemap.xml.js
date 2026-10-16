export async function GET() {
  const pages = [
    '',
    'lineas',
    'lineas/1',
    'lineas/5',
    'lineas/10',
    'como-llegar/aeropuerto',
    'como-llegar/terminal',
    'como-llegar/ciudad-universitaria',
    'guias/red-bus',
    'guias/tarifas',
    'novedades',
    'sobre-nosotros',
    'contacto',
    'privacidad',
    'terminos'
  ];

  const siteUrl = 'https://bondicordoba.com.ar';

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(page => `  <url>
    <loc>${siteUrl}/${page}</loc>
    <changefreq>${page.includes('lineas/') ? 'weekly' : page === '' ? 'daily' : 'monthly'}</changefreq>
    <priority>${page === '' ? '1.0' : page.includes('lineas/') ? '0.8' : '0.6'}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(sitemap.trim(), {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}
