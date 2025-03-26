# Template Vite MobX ReactQuery

This template provides a modern setup for building scalable React applications with efficient state management, data fetching, and routing.


## React Query + MobX: The Best of Both Worlds

This template leverages the powerful combination of React Query and MobX to handle both data fetching and state management effectively.

React Query excels at managing server-side state, including fetching, caching, and syncing data with your backend, ensuring your app stays performant and up-to-date.

On the other hand, MobX provides a simple yet powerful way to manage client-side state, offering reactivity and seamless integration with your React components. Together, these tools create a highly scalable architecture where React Query handles transient, server-driven data, and MobX manages persistent, client-driven state, enabling you to build robust, maintainable applications effortlessly.


## Features

- **Vite**: Fast development and build tooling.
- **MobX**: Reactive state management.
- **React Query**: Optimized data fetching and caching.
- **TanStack Router**: Flexible routing system with powerful features.
- **fp-ts**: Functional programming utilities.
- **zod**: Type-safe schema validation.
- **Biome**: Unified linter and formatter.


## Scripts

- `start:dev`: Start the development server.
- `start:prod`: Serve the production build using http-server on http://localhost:5000.
- `build`: Build the application for production.
- `check:code`: Type-check the project.
- `format:code`: Format the codebase using Biome.
- `lint:code`: Lint and fix issues in the codebase.
- `precommit`: Runs type-checking, formatting, and linting before commits.



## Folder Structure

```plaintext
src/
├── assets/       # Static assets (images, fonts, etc.)
├── components/   # Reusable and page-specific components
├── contextes/    # React Contexts for shared state
├── hooks/        # Custom React hooks
├── init/         # Application initialization logic
├── libs/         # Shared libraries and utilities
├── schemas/      # zod schemas for validation
├── stores/       # MobX stores for state management
├── main.tsx      # Application entry point
└── vite-env.d.ts # Vite environment type declarations
```

## Development Environment Setup

1. Ensure you are in the service-ux-chatbox directory
   ```bash
   ~/ pwd
   /dify-poc/service-ux-chatbox
   ```

2. Install dependencies:
   ```bash
   npm ci
   ```

3. Setup .env file
   ```bash
   cp .env.example .env.development
   ```
   This creates an env file that Vite uses for the development environment. See below for current env variables.
   
   **Note:** Email and Password are used for communication with Dify. Once we have an authentication system, these will be removed. 
   ```bash
   VITE_BACKEND=http://localhost:8000
   VITE_WEBSOCKET_BACKEND=ws://localhost:8000
   VITE_DIFY_EMBED=http://localhost/
   VITE_EMAIL=danny@danny.com
   VITE_PASSWORD=Password1234
   ```

4. Run the server
   ```bash
   npm run start:dev
   ```

5. Access application at http://localhost:5173/

**Reminder:** Ensure code quality with `check:code`, `format:code`, and `lint:code`.

## Production Environment Setup

1. Ensure you are in the service-ux-chatbox directory
   ```bash
   ~/ pwd
   /dify-poc/service-ux-chatbox
   ```

2. Install dependencies:
   ```bash
   npm ci
   ```

3. Setup .env file
   ```bash
   cp .env.example .env
   ```
   This creates an env file that Vite uses for the production environment. See below for current env variables.
   
   **Note:** Email and Password are used for communication with Dify. Once we have an authentication system, these will be removed. 
   ```bash
   VITE_BACKEND=http://localhost:8000
   VITE_WEBSOCKET_BACKEND=ws://localhost:8000
   VITE_DIFY_EMBED=http://localhost/
   VITE_EMAIL=danny@danny.com
   VITE_PASSWORD=Password1234
   ```

4. Build the application
   ```bash
   npm run build
   ```
   **Note:** If you are already using port 5000 for something else, you can change it to a desired port in package.json in the line ```"start:prod": "http-server dist -p 5000 -o"```. Simply change the 5000 to something else.

5. Run the server
   ```bash
   npm run start:prod
   ```

6. Access application at http://localhost:5000/


## Docker Deployment
We have introduced environment variables to our application. When the application is being built, React takes the environment variables and uses them in the build process. With that being said, we need to pass in those variables when we build the Docker image. 

1. Ensure you are in the service-ux-chatbox directory
   ```bash
   ~/ pwd
   /dify-poc/service-ux-chatbox
   ```
2. Build the docker image
   We pass in the environment variables we need using the --build-arg flag as seen below. 
   ```bash
   docker build \
   --build-arg VITE_BACKEND=http://127.0.0.1:8000 \
   --build-arg VITE_WEBSOCKET_BACKEND=ws://127.0.0.1:8000 \
   --build-arg VITE_DIFY_EMBED=http://127.0.0.1/ \
   --build-arg VITE_EMAIL=danny@danny.com \
   --build-arg VITE_PASSWORD=Password1234 \
   -t service-ux-chatbox .
   ```
3. Deploy the application 
   ```bash
   docker run -d -p 5050:5000 --name service-ux-chatbox --restart always service-ux-chatbox
   ```
4. Access the application at http://localhost:5050

**Things to Note:** `-p 5050:5000` maps external port `5050` to internal `5000`. You can change the left port to a different port if it conflicts with a service you are running.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
