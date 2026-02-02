FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy Vite build output to nginx
COPY dist /usr/share/nginx/html

# Expose port 3000
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]

