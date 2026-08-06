# Task API - FastAPI Authentication System

A CRUD Task API built with FastAPI, PostgreSQL, Docker, and Supabase Authentication.

Docker Compose starts the FastAPI application and PostgreSQL database together with one command. The project also includes user authentication with Supabase, JWT protected routes, and Swagger Bearer authentication.

---

# Features

- FastAPI backend
- PostgreSQL database
- Docker and Docker Compose setup
- Persistent database storage using Docker volume
- Repository pattern architecture
- CRUD task management
- Supabase authentication
- User signup and login
- JWT token verification
- Protected API routes
- Logout functionality
- Swagger Bearer authentication

---

# Why PostgreSQL and Docker?

PostgreSQL provides a dedicated relational database server suitable for applications that need reliable concurrent access and durable data.

Docker keeps the Python and PostgreSQL environments reproducible. Docker Compose connects both services and starts them together.

A named Docker volume stores PostgreSQL data outside the database container, so recreating containers does not remove stored tasks.

---

# Project Architecture

```text
main.py                              creates the FastAPI application
routes/task_routes.py                defines task HTTP endpoints
routes/auth_routes.py                defines public/protected routes
services/task_service.py             contains validation and business logic
repositories/task_repository.py      defines repository interface
repositories/postgres_repository.py  PostgreSQL repository implementation
auth/auth_routes.py                  signup, login and logout routes
config/supabase_client.py            initializes Supabase client
dependencies/auth.py                 JWT verification dependency
dependencies/task.py                 task service dependency
database/init.sql                    creates and seeds database table
docker-compose.yml                   starts FastAPI and PostgreSQL