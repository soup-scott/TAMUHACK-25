import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  
  server: {
    // morgan add on so my stuff will ACTUALLY UPDATE without me re-running
    hmr: true,
    watch: {
      usePolling: true,
    },
  },
})
