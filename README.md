# Task API with PostgreSQL and Docker

A CRUD task API built with FastAPI and PostgreSQL. Docker Compose starts the API and database together with one command.

## Why PostgreSQL and Docker?

PostgreSQL provides a dedicated relational database server suitable for applications that need reliable concurrent access and durable data. Docker keeps the Python and PostgreSQL environments reproducible, while Docker Compose connects both services and starts them together. A named Docker volume stores PostgreSQL data outside the database container so recreating containers does not erase tasks.

## Project Architecture

```text
main.py                              creates the FastAPI application
routes/task_routes.py                defines the HTTP endpoints
services/task_service.py             contains validation and business logic
repositories/task_repository.py      defines the repository interface
repositories/postgres_repository.py  implements that interface for PostgreSQL
repositories/sqlite_repository.py    preserves the previous SQLite implementation
dependencies.py                      selects PostgresTaskRepository
database/init.sql                    creates and seeds the tasks table
docker-compose.yml                   starts FastAPI and PostgreSQL
```

Only the repository selection in `dependencies.py` was switched from SQLite to PostgreSQL. The existing routes and service were left unchanged because the PostgreSQL repository implements the same interface and no blocking bug was found in either layer. This preserves the existing endpoints, status codes, validation messages, and response shapes.

## Environment Setup

Docker Desktop (or Docker Engine with the Compose plugin) is required.

1. Copy `.env.example` to `.env`.
2. Replace the example password in `.env` with a private password.
3. Keep all four values consistent: the username, password, and database name inside `DATABASE_URL` must match the three `POSTGRES_*` values.

Example structure:

```dotenv
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=your_private_password
POSTGRES_DB=tasksdb
DATABASE_URL=postgresql://taskuser:your_private_password@db:5432/tasksdb
```

The hostname is `db` because that is the PostgreSQL service name in Docker Compose. The real `.env` file is ignored by both Git and the Docker build context. `.env.example` is safe to commit because it contains placeholder credentials only.

## Start the Application

From the project directory, run:

```bash
docker compose up
```

To build and run in the background:

```bash
docker compose up --build -d
```

The API is available at `http://localhost:8000`, and Swagger UI is at `http://localhost:8000/docs`.

Check the services with:

```bash
docker compose ps
```

Stop the services without deleting stored data:

```bash
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the PostgreSQL volume and all stored tasks.

## Database Initialization and Persistence

On the first start of a new volume, PostgreSQL runs `database/init.sql`. It creates the `tasks` table and inserts the same three starter tasks used by the previous SQLite implementation. The named volume `postgres_data` is mounted at `/var/lib/postgresql/data`.

The persistence test performed for this assignment is documented in the verification section below.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Show API information |
| GET | `/health` | Check API health |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get one task |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

Create request example:

```json
{
  "title": "Learn PostgreSQL"
}
```

Update request example:

```json
{
  "title": "Learn PostgreSQL and Docker",
  "done": true
}
```

## Verification Performed

The final verified commands, HTTP results, created task ID, and persistence restart result will be recorded here after the Docker test run.

## Author

Asma Hussain
