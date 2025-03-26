# Use an official Node.js runtime as a parent image
FROM node:22

# Set the working directory in the container
WORKDIR /app

# Get build Args
ARG VITE_BACKEND
ARG VITE_WEBSOCKET_BACKEND
ARG VITE_DIFY_EMBED
ARG VITE_EMAIL
ARG VITE_PASSWORD

# Set environment variables for build
ENV VITE_BACKEND=${VITE_BACKEND}
ENV VITE_WEBSOCKET_BACKEND=${VITE_WEBSOCKET_BACKEND}
ENV VITE_DIFY_EMBED=${VITE_DIFY_EMBED}
ENV VITE_EMAIL=${VITE_EMAIL}
ENV VITE_PASSWORD=${VITE_PASSWORD}

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages specified in package.json or package-lock.json
RUN npm install

# Bundle app source inside Docker image
COPY . .

# Build the application
RUN npm run build

# Specify the port the app runs on
EXPOSE 5000

# Command to run the app
CMD ["npm", "run", "start:prod"]