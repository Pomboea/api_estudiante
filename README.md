# API de Estudiantes

API REST con FastAPI y PostgreSQL (Neon) para guardar y consultar estudiantes.

## Endpoints

- `GET /` — estado de la API
- `GET /estudiantes/` — listar
- `POST /estudiantes/` — crear
- `GET /estudiantes/{id}` — obtener uno
- `PUT /estudiantes/{id}` — actualizar
- `DELETE /estudiantes/{id}` — eliminar

## Tabla SQL

```sql
CREATE TABLE estudiantes (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  grado INTEGER NOT NULL,
  promedio NUMERIC(3,2) NOT NULL
);
```

## Variables de entorno

Copia `.env.example` a `.env` y completa:

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT` (por defecto `5432`)

## Local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## Render

- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
