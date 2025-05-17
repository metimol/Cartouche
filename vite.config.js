import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  root: "src/web",
  publicDir: "../../public",
  build: {
    outDir: "../../web-build",
    emptyOutDir: true,
  },
  server: {
    port: 8000,
    open: true,
    host: '0.0.0.0',
    allowedHosts: ['.'],
  },
});
