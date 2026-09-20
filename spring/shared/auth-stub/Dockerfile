# A single-stage build - unlike the mission service, there's no separate
# "compile" step for Node. npm install still gets its own layer, ordered
# before the app code, for the same caching reason as Module 12's
# COPY pom.xml first.
FROM node:20-alpine
WORKDIR /app

COPY package.json .
RUN npm install --omit=dev

COPY server.js .

EXPOSE 4000
CMD ["node", "server.js"]
