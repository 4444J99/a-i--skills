---
name: fastapi-patterns
description: Build production FastAPI applications with dependency injection, middleware, background tasks, and structured project layouts. Covers async patterns, Pydantic models, OpenAPI customization, and testing strategies. Triggers on FastAPI development, Python API, or async web framework requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - fastapi
  - python
  - async
  - api
  - pydantic
governance_phases: [build]
organ_affinity: [organ-iv, organ-vi, meta]
triggers: [user-asks-about-fastapi, project-has-fastapi, context:python-api, file-type:*app.py]
complements: [python-packaging-patterns, api-design-patterns, backend-implementation-patterns, redis-patterns]
---

# FastAPI Patterns

Build production-ready async APIs with FastAPI's dependency injection and type system.

## Project Layout

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app factory
│   ├── config.py          # Pydantic Settings
│   ├── dependencies.py    # Shared DI providers
│   ├── middleware.py       # Custom middleware
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── skills.py
│   │   └── registry.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── skill.py       # Pydantic models
│   │   └── registry.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── skill_service.py
│   │   └── registry_service.py
│   └── db/
│       ├── __init__.py
│       └── session.py
└── tests/
    ├── conftest.py
    └── test_skills.py
```

## App Factory

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_cache()
    yield
    # Shutdown
    await close_db()
    await close_cache()

def create_app() -> FastAPI:
    app = FastAPI(
        title="ORGANVM Skills API",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(skills_router, prefix="/api/skills", tags=["skills"])
    app.include_router(registry_router, prefix="/api/registry", tags=["registry"])
    app.add_middleware(CorrelationMiddleware)
    return app

app = create_app()
```

## Dependency Injection

```python
from fastapi import Depends
from typing import Annotated

async def get_db():
    async with async_session() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:  # allow-secret
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Type aliases for clean signatures
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/skills/{skill_id}")
async def get_skill(skill_id: str, db: DB, user: CurrentUser) -> SkillResponse:
    skill = await db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return SkillResponse.model_validate(skill)
```

## Pydantic Models

```python
from pydantic import BaseModel, Field
from datetime import datetime

class SkillBase(BaseModel):
    name: str = Field(pattern=r"^[a-z][a-z0-9-]*$", min_length=2, max_length=64)
    description: str = Field(min_length=20, max_length=600)
    category: str
    tags: list[str] = []

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class SkillList(BaseModel):
    items: list[SkillResponse]
    total: int
    page: int
    per_page: int
```

## Router Patterns

```python
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/", response_model=SkillList)
async def list_skills(
    db: DB,
    category: str | None = None,
    tag: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> SkillList:
    query = select(Skill)
    if category:
        query = query.where(Skill.category == category)
    if tag:
        query = query.where(Skill.tags.contains([tag]))
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    skills = await db.scalars(query.offset((page - 1) * per_page).limit(per_page))
    return SkillList(items=skills.all(), total=total, page=page, per_page=per_page)

@router.post("/", response_model=SkillResponse, status_code=201)
async def create_skill(data: SkillCreate, db: DB, user: CurrentUser) -> SkillResponse:
    skill = Skill(**data.model_dump())
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return SkillResponse.model_validate(skill)
```

## Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/skills/{skill_id}/validate")
async def validate_skill(
    skill_id: str,
    background_tasks: BackgroundTasks,
    db: DB,
):
    skill = await db.get(Skill, skill_id)
    background_tasks.add_task(run_validation, skill_id)
    return {"status": "validation_queued", "skill_id": skill_id}

async def run_validation(skill_id: str):
    # Long-running validation logic
    async with async_session() as db:
        skill = await db.get(Skill, skill_id)
        result = await validate_frontmatter(skill)
        skill.validation_status = result.status
        await db.commit()
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, code: str, status: int):
        self.message = message
        self.code = code
        self.status = status

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
```

## Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_list_skills(client: AsyncClient):
    response = await client.get("/api/skills/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

@pytest.mark.asyncio
async def test_create_skill(client: AsyncClient):
    response = await client.post("/api/skills/", json={
        "name": "test-skill",
        "description": "A test skill for unit testing purposes",
        "category": "development",
    })
    assert response.status_code == 201
    assert response.json()["name"] == "test-skill"
```

## Anti-Patterns

- **Sync database calls** — Always use async drivers (asyncpg, aiosqlite)
- **Business logic in routes** — Extract to service layer for testability
- **No response models** — Always define response_model for API documentation
- **Global state** — Use dependency injection, not module-level singletons
- **Missing validation** — Pydantic models should validate all inputs
- **No lifespan management** — Use the lifespan context manager for startup/shutdown
