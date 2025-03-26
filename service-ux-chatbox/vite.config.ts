/// <reference types="vitest" />
import path from 'node:path';
// import path from 'path'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0',
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },

  resolve: {
    alias: {
      '@/src': path.resolve(__dirname, './src'),
    },
  },

  plugins: [TanStackRouterVite(), react()],

  build: {
    minify: true,
    emptyOutDir: true,
  },

  clearScreen: false,
});
