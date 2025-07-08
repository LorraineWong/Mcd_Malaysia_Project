import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/ask': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/outlets': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
