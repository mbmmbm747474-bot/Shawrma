import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

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
