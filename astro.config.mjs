// @ts-check
import { defineConfig } from 'astro/config';
import icon from 'astro-icon';

// https://astro.build/config
export default defineConfig({
  site: 'https://bondicordoba.com.ar',
  integrations: [icon()],
  build: {
    inlineStylesheets: 'auto',
  },
  compressHTML: true,
  redirects: {
    '/lineas/A1': '/lineas/36A',
    '/lineas/B1': '/lineas/81B',
    '/lineas/C1': '/lineas/10C',
    '/lineas/C2': '/lineas/B10',
  },
});
