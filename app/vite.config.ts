import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    cors: {
      origin: ["http://127.0.0.1:3000/", "http://127.0.0.1:8000/"],
    }
  },
  plugins: [
    vue(),
    tailwindcss(),
  ],
})
