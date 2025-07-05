import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
  server: {
    watch: {
      // incluye también tu carpeta components
      include: ['components/**', 'src/**']
    }
  }
});
