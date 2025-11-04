# TaskManager

This is a simple Full Stack task manager application built with React, FastAPI, and PostgreSQL.

## Design

See the design document: [Design Document](Design/DESIGN.md)

## How to run the project

For the fontend:

1. run the dev server

```bash
cd UI
npm install
npm run dev
```

2. Create a .env file to configure the backend URL:

```env
VITE_API_URL=http://localhost:8000
```

### Backend Setup

The backend is built with Python 3.13

1. Set up PostgreSQL with docker or run it as a service.

2. Create a .env file in the BackEnd directory (change the values to you pg instance data)

```env
BACKEND_CORS_ORIGINS=["*"]
ALLOWED_HOSTS=["*"]

DEFAULT_DATABASE_HOSTNAME=localhost
DEFAULT_DATABASE_USER=postgres
DEFAULT_DATABASE_PASSWORD=postgres
DEFAULT_DATABASE_PORT=5432
DEFAULT_DATABASE_DB=taskmanager
```

3. Create and activate a virtual environment:

```powershell
cd BackEnd
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Run the tests:

```bash
python -m pytest tests/test_tasks_service.py -v
```

6. Start the development server:

```
python.exe -m uvicorn app.main:app --reload
```

## API Documentation

Once the backend is running, you can access:

- Swagger UI: http://localhost:8000/docs

## Development

The application is structured as follows:

- `UI/`: React frontend with TypeScript
- `BackEnd/`: FastAPI backend with SQLAlchemy
- `Design/`: Architecture and design documentation
