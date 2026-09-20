# VectorShift Integrations - Docker Setup

## Expected project structure

Move/copy the Docker files so your project looks like:

    project/
    ├── docker-compose.yml
    ├── backend/
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   ├── .dockerignore
    │   ├── .env
    │   └── integrations/
    │       ├── __init__.py
    │       ├── hubspot.py
    │       ├── notion.py
    │       └── airtable.py
    └── frontend/
        ├── package.json
        ├── package-lock.json
        ├── src/
        ├── Dockerfile
        ├── nginx.conf
        └── .dockerignore

Do NOT put .env into the Docker image. docker-compose passes it to the backend container.

## Build and run

From the project root:

    docker compose up --build

Then open:

    Frontend: http://localhost:3000
    Backend:  http://localhost:8000

To stop:

    docker compose down

To rebuild after code/dependency changes:

    docker compose up --build

## Important

The current frontend integration files use http://localhost:8000 as the API base URL, so publishing backend port 8000 on the host is intentional for this local Docker setup.

For production deployment, make the API URL configurable instead of hardcoding localhost.

Do not commit backend/.env to Git.
