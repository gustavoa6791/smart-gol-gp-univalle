# Smart Gol

Sistema de gestión de torneos deportivos. Monorepo con **backend** (FastAPI + MySQL en Docker) y **frontend** (Next.js, fuera del contenedor con hot-reload).

Este repositorio es la **base del proyecto (HU-000)**: entorno, base de datos, migraciones, autenticación base y CI listos para que cada quien construya su HU encima. Ver [docs/HU-000.md](docs/HU-000.md).

## Stack

| Capa          | Tecnología |
|---------------|------------|
| Frontend      | Next.js 16, React 19, TypeScript 5, Tailwind CSS 4 |
| Backend       | FastAPI 0.115, SQLAlchemy 2.0, Pydantic 2.10 |
| Base de datos | MySQL 8 (PyMySQL) |
| Auth          | JWT (HS256, bcrypt) — helpers listos, login en HU-001 |
| Infra         | Docker Compose (db + backend) |

## Arquitectura de ejecución

- **Backend + base de datos → Docker.** Se levantan juntos con un solo comando.
- **Frontend → fuera del contenedor**, con `npm run dev` para aprovechar el hot-reload del servidor de desarrollo.

```
┌─────────── Docker Compose ───────────┐      Host (npm run dev)
│  smart_gol_db (MySQL :3307→3306)      │      ┌─────────────────────┐
│  smart_gol_backend (FastAPI :8000) ◄──┼──────┤ frontend Next.js     │
└───────────────────────────────────────┘      │ :3000  /api → :8000  │
                                                └─────────────────────┘
```

## Requisitos

- Docker + Docker Compose
- Node.js 20+

## 1) Levantar backend + base de datos (Docker)

```bash
DOCKER_BUILDKIT=0 docker compose -p smart_gol up --build -d
```

Esto crea la base de datos, aplica las migraciones de Alembic (`entrypoint.sh`) y deja la API en pie.

| Servicio | URL |
|----------|-----|
| Backend  | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health   | http://localhost:8000/api/health |

Datos de prueba (un usuario por rol):

```bash
docker exec smart_gol_backend python seed.py
# admin@smartgol.com / admin123  ·  organizer@smartgol.com / organizer123  ·  viewer@smartgol.com / viewer123
```

## 2) Levantar frontend (local, hot-reload)

```bash
cd frontend
cp .env.example .env.local   # opcional, valores por defecto ya apuntan a :8000
npm install
npm run dev
```

Frontend en http://localhost:3000 (la home muestra el estado del backend).

## Ritual de cambios en la base de datos (Alembic)

1. Edita `backend/models.py` (y `schemas.py` / `frontend/lib/types.ts` si aplica).
2. Genera la migración:
   ```bash
   docker exec smart_gol_backend alembic revision --autogenerate -m "descripcion"
   ```
3. Revisa el archivo nuevo en `backend/migrations/versions/` (`upgrade` / `downgrade`).
4. Aplica:
   ```bash
   docker exec smart_gol_backend alembic upgrade head
   ```
   (Reiniciar el contenedor también la aplica vía `entrypoint.sh`.)

## Estructura

```
smart_gol/
├── docker-compose.yml          # db + backend
├── .github/workflows/ci.yml    # CI: lint backend + lint/build frontend
├── docs/HU-000.md              # alcance y guía de la base
├── backend/
│   ├── main.py                 # FastAPI: CORS, routers, startup DB
│   ├── database.py             # engine + SessionLocal + get_db
│   ├── models.py               # Base + modelo User (+ UserRole)
│   ├── schemas.py              # schemas Pydantic base
│   ├── auth.py                 # JWT, bcrypt, get_current_user, require_roles
│   ├── seed.py                 # usuario por rol
│   ├── routers/health.py       # /api/health (patrón de router)
│   └── migrations/             # Alembic (0001_initial_users)
└── frontend/
    ├── app/                    # App Router (layout, home con health-check)
    ├── lib/api.ts              # cliente axios con interceptors
    └── lib/types.ts            # tipos compartidos
```

## CI

Cada push/PR corre [.github/workflows/ci.yml](.github/workflows/ci.yml): lint del backend (ruff) + verificación de import, y lint + build del frontend.
