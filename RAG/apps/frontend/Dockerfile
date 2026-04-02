# Stage 1: Build the React Application
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the build via Nginx
FROM nginx:alpine
# Copy the built assets to the default nginx public folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the standard web port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
