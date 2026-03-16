READ BEFORE EXECUTING OR COMPILING

------------------------------------------------------------

Create a `.env` file in the project root with:

```
ENVIRONMENT=dev
RATE_LIMIT_DEV=100/minute
RATE_LIMIT_PROD=30/minute
```

------------------------------------------------------------

This README will be updated with additional variables and API key requirements as they are added.

Run with Docker

1. Build the image:
`docker build -t cr-backoffice .`

2. Run the container:
`docker run --rm -p ${HOST_PORT:-8080}:8080 --env-file .env cr-backoffice`

The API will be available at `http://localhost:${HOST_PORT:-8080}/docs`.

If port 8080 is already in use, override `HOST_PORT` (export it or update the `.env` file)
before running the container so that Docker publishes the service on a different host port.

-----------------------------------------------------------

Run locally (without Docker)

1. Activate the virtual environment:
`.\.venv\Scripts\activate`

2. Start the app:
`python -m uvicorn main:app --host 127.0.0.1 --port 8000`

The API will be available at `http://127.0.0.1:8000/docs`.

