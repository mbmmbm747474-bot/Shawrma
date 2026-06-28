# Development image: runs the Vite dev server with hot reload.
# For production, run `npm run build` and serve /dist with any static file
# server (nginx, Caddy, etc.) — that step isn't wired up yet in this milestone.

FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
