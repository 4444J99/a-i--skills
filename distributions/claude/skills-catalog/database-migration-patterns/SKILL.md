---
name: database-migration-patterns
description: Manage database schema changes safely with migration tools, zero-downtime strategies, and rollback procedures. Covers Alembic, SQL migrations, data migrations, and testing strategies. Triggers on database migration, schema changes, or Alembic configuration requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - database
  - migrations
  - alembic
  - schema
  - zero-downtime
governance_phases: [build, prove]
organ_affinity: [organ-iii, organ-vi, meta]
triggers: [user-asks-about-migrations, context:database-schema, context:alembic, project-has-alembic-ini]
complements: [python-packaging-patterns, postgres-advanced-patterns, fastapi-patterns]
---

# Database Migration Patterns

Evolve database schemas safely with versioned, reversible, tested migrations.

## Alembic Setup

```bash
# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "add skills table"

# Run migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Show current state
alembic current
alembic history
```

### Configuration

```python
# alembic/env.py
from app.models import Base
from app.config import settings

target_metadata = Base.metadata

def run_migrations_online():
    connectable = create_async_engine(settings.database_url)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
```

## Migration Structure

```python
"""add skills table

Revision ID: abc123
Revises: def456
Create Date: 2026-03-20 10:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "abc123"
down_revision = "def456"

def upgrade():
    op.create_table(
        "skills",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(64), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_skills_category", "skills", ["category"])

def downgrade():
    op.drop_index("ix_skills_category")
    op.drop_table("skills")
```

## Zero-Downtime Migration Strategies

### Adding a Column

```python
# Safe: add nullable column first
def upgrade():
    op.add_column("skills", sa.Column("tier", sa.String(20), nullable=True))

# Later migration: backfill then add constraint
def upgrade():
    op.execute("UPDATE skills SET tier = 'community' WHERE tier IS NULL")
    op.alter_column("skills", "tier", nullable=False, server_default="community")
```

### Renaming a Column

```python
# Phase 1: Add new column
def upgrade():
    op.add_column("skills", sa.Column("skill_category", sa.String(32)))
    op.execute("UPDATE skills SET skill_category = category")

# Phase 2: (after app updated to use new column)
def upgrade():
    op.drop_column("skills", "category")
```

### Removing a Column

```python
# Phase 1: Stop writing to column (app change)
# Phase 2: Remove column
def upgrade():
    op.drop_column("skills", "deprecated_field")
```

### Adding an Index

```python
# Use CONCURRENTLY for zero-downtime
def upgrade():
    op.execute("CREATE INDEX CONCURRENTLY ix_skills_name ON skills (name)")

def downgrade():
    op.drop_index("ix_skills_name")
```

## Data Migrations

```python
"""backfill governance metadata

Revision ID: ghi789
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Use raw SQL for large table updates
    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE skills
        SET governance_phases = ARRAY['build']
        WHERE governance_phases IS NULL
        AND category IN ('development', 'data')
    """))
    conn.execute(sa.text("""
        UPDATE skills
        SET governance_phases = ARRAY['prove']
        WHERE governance_phases IS NULL
        AND category IN ('security', 'documentation')
    """))

def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE skills SET governance_phases = NULL"))
```

## Testing Migrations

```python
import pytest
from alembic.config import Config
from alembic import command

@pytest.fixture
def alembic_config():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", test_database_url)
    return config

def test_upgrade_downgrade(alembic_config):
    # Full upgrade
    command.upgrade(alembic_config, "head")
    # Full downgrade
    command.downgrade(alembic_config, "base")
    # Back to head
    command.upgrade(alembic_config, "head")

def test_migration_data_integrity(alembic_config, db_session):
    command.upgrade(alembic_config, "head")
    # Insert test data
    db_session.execute(sa.text("INSERT INTO skills (id, name, description, category) VALUES ('t1', 'test', 'Test skill', 'dev')"))
    db_session.commit()
    # Verify data survives next migration
    command.upgrade(alembic_config, "head")
    result = db_session.execute(sa.text("SELECT name FROM skills WHERE id = 't1'"))
    assert result.scalar() == "test"
```

## Migration Checklist

### Before Creating

- [ ] Schema change designed for zero-downtime
- [ ] Both upgrade and downgrade paths defined
- [ ] Large table changes use batching/CONCURRENTLY

### Before Deploying

- [ ] Migration tested against staging database
- [ ] Rollback tested (downgrade works)
- [ ] Data backup taken
- [ ] Estimated execution time for large tables
- [ ] Application compatible with both old and new schema

### After Deploying

- [ ] Migration completed successfully
- [ ] Application functioning correctly
- [ ] No performance regressions
- [ ] Cleanup migration scheduled (if multi-phase)

## Anti-Patterns

- **No downgrade** — Every migration must be reversible
- **Destructive changes in one step** — Use multi-phase for column renames/removals
- **Mixing schema and data migrations** — Separate into distinct revisions
- **Manual SQL in production** — All changes through versioned migrations
- **Testing only upgrade** — Test downgrade paths too
- **Large table ALTER without CONCURRENTLY** — Locks the table for the duration
