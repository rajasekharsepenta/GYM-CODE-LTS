#step1 - Use Nginx base image
FROM nginx:latest

# Copy your index.html to the default nginx HTML directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 3000
EXPOSE 3000

# Change Nginx default port from 80 → 3000
RUN sed -i 's/80/3000/g' /etc/nginx/conf.d/default.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
