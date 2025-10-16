import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 3000,
    proxy: {
      '/api': 'http://djangoapp:8000',
      '/search': 'http://djangoapp:8000',
    },
    watch: {
      usePolling: true,
    }
  }
})
