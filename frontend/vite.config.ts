import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { fileURLToPath } from "node:url";

// package.json has "type": "module", so this file runs as an ES module -
// __dirname doesn't exist here. We also deliberately do NOT name this
// variable __dirname: Vite's own docs warn that it specially substitutes
// __filename/__dirname/import.meta.url as string literals inside config
// files, and assigning to a variable with one of those exact names breaks.
const configDir = path.dirname(fileURLToPath(import.meta.url));

// VITE_API_PROXY_TARGET lets the dev server proxy reach the backend whether
// running directly on the host (http://localhost:8000, the default) or
// inside the docker-compose network (http://backend:8000, set as a real
// container env var in docker-compose.yml). loadEnv also picks it up from
// a local .env file for the `npm run dev` (non-Docker) case.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || "http://localhost:8000";

  return {
    plugins: [react()],
    resolve: {
      alias: {
        // Must match tsconfig.json's "paths": { "@/*": ["src/*"] } -
        // that file only affects the editor/type-checker, not the actual
        // bundler, so the alias has to be declared here too or every
        // "@/..." import fails at build time (though it works fine in dev
        // mode, where esbuild is more lenient - that's why this wasn't
        // caught until a production build was attempted).
        "@": path.resolve(configDir, "./src"),
      },
    },
    server: {
      host: true,
      port: 5173,
      proxy: {
        "/api": {
          target: apiProxyTarget,
          changeOrigin: true,
        },
      },
    },
  };
});
