import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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
    rollupOptions: {
      input: path.resolve(__dirname, "src/web/index.html"),
    },
  },
});