import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  plugins: [],
  root: resolve('./'),
  base: '/static/',
  define: {},
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.ts', '.tsx'],
  },
  build: {
    outDir: resolve('./static/js'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'esnext',
    rollupOptions: {
      input: {
        site: resolve('./src/site.ts'),
      },
      output: {
        chunkFileNames: undefined,
      },
      external: ['Typewriter'],
    },
  },
});
