import { defineConfig } from 'astro/config';
import icon from 'astro-icon';

export default defineConfig({
  site: 'https://bondicordoba.com.ar',
  integrations: [
    icon()
  ],
  build: {
    inlineStylesheets: 'auto'
  }
});
