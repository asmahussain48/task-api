# Task API with SQLite

A CRUD Task API built using FastAPI and SQLite.

The API allows users to:

- View all tasks
- View one task
- Create a task
- Update a task
- Delete a task

All tasks are stored permanently in a SQLite database.

## Technologies Used

- Python
- FastAPI
- SQLite
- Uvicorn

## Why SQLite Was Chosen

SQLite was chosen because it is lightweight, simple to use, and does not require a separate database server.

The complete database is stored in one file, which makes SQLite suitable for small projects and learning backend database concepts.

## Database Location

The SQLite database file is named:

```text
tasks.db
```

It is automatically created in the same directory as `main.py` when the application starts.

The application also automatically:

- Creates the `tasks` table if it does not exist
- Inserts three example tasks if the table is empty

## Database Structure

The `tasks` table contains the following columns:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Unique task ID |
| title | TEXT | Task title |
| done | BOOLEAN | Task completion status |

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

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/asmahussain48/task-api.git
```

### 2. Enter the project directory

```bash
cd task-api
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS or Linux:

```bash
source venv/bin/activate
```

### 5. Install the dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 7. Open Swagger documentation

Open this address in your browser:

```text
http://127.0.0.1:8000/docs
```

## Example Request

Create a task using:

```json
{
  "title": "Learn SQLite"
}
```

Example response:

```json
{
  "id": 4,
  "title": "Learn SQLite",
  "done": false
}
```

## Example SQL Query

The following query returns all completed tasks:

```sql
SELECT *
FROM tasks
WHERE done = 1;
```

## Database Screenshot

![SQLite database screenshot](screenshots/database-view.png)

## Persistence

Tasks are stored inside SQLite instead of an in-memory Python list.

This means that tasks remain available after the application server is stopped and restarted.

## Author

Your Asma Hussain