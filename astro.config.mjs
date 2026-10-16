// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://bondicordoba.com.ar',
  integrations: [],
  build: {
    inlineStylesheets: 'auto',
  },
  compressHTML: true,
});
