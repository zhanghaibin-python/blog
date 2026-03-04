import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') // The backend expects /api/v1/..., so we don't rewrite if the backend root handles /api
        // The API doc says Base URL: /api/v1/
        // If backend URLs are defined as /api/v1/..., then we keep /api.
        // Assuming Django urls.py includes path('api/v1/', include(...))
      }
    }
  }
})
