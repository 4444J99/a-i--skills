---
name: configuration-management
description: Manage application configuration across environments with layered config loading, environment variables, secrets management, and validation. Covers 12-factor app patterns and config file formats. Triggers on configuration management, environment variables, or settings architecture requests.
license: MIT
complexity: intermediate
time_to_learn: 30min
tags:
  - configuration
  - environment-variables
  - secrets
  - twelve-factor
  - settings
governance_phases: [shape, build]
organ_affinity: [all]
triggers: [user-asks-about-config, context:environment-variables, context:settings, project-has-dotenv, file-type:.env*]
complements: [python-packaging-patterns, cli-tool-design, docker-containerization]
---

# Configuration Management

Load, validate, and manage application configuration across environments.

## Configuration Hierarchy

Priority order (highest wins):

```
1. Command-line arguments
2. Environment variables
3. .env.local (git-ignored, per-developer)
4. .env.{environment} (e.g., .env.production)
5. .env (shared defaults)
6. Config file (config.yaml, settings.toml)
7. Application defaults
```

## Python: Pydantic Settings

```python
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    model_config = {"env_prefix": "APP_", "env_file": ".env"}

    # Required
    database_url: str
    redis_url: str = "redis://localhost:6379"

    # Secrets (masked in logs)
    api_key: SecretStr  # allow-secret
    db_password: SecretStr

    # Typed with defaults
    debug: bool = False
    log_level: str = "INFO"
    workers: int = Field(default=4, ge=1, le=32)
    allowed_origins: list[str] = ["http://localhost:3000"]

settings = Settings()  # Loads from env + .env file
```

### Environment-Specific Overrides

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {
        "env_prefix": "APP_",
        "env_file": [".env", f".env.{os.getenv('APP_ENV', 'development')}"],
    }
```

## Environment Variable Conventions

### Naming

```bash
# Prefix with app name to avoid collisions
APP_DATABASE_URL=postgresql://...
APP_REDIS_URL=redis://...
APP_LOG_LEVEL=DEBUG

# Nested config uses double underscore
APP_AUTH__SECRET_KEY=...
APP_AUTH__TOKEN_TTL=3600
```

### .env Files

```bash
# .env (committed, shared defaults)
APP_LOG_LEVEL=INFO
APP_WORKERS=4
APP_REDIS_URL=redis://localhost:6379

# .env.local (git-ignored, developer overrides)
APP_DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp
APP_DEBUG=true

# .env.production (committed, production defaults)
APP_LOG_LEVEL=WARNING
APP_WORKERS=8
APP_DEBUG=false
```

### .gitignore Rules

```gitignore
.env.local
.env.*.local
*.secret
```

## Configuration Validation

### Fail Fast on Startup

```python
def validate_config(settings: Settings) -> None:
    errors = []

    if settings.debug and settings.log_level == "WARNING":
        errors.append("Debug mode with WARNING log level — probably unintended")

    if "localhost" in settings.database_url and not settings.debug:
        errors.append("Localhost database URL in non-debug mode")

    if errors:
        for e in errors:
            print(f"CONFIG ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
```

### Schema Validation for Config Files

```python
import yaml
import jsonschema

def load_config(path: str, schema_path: str) -> dict:
    config = yaml.safe_load(Path(path).read_text())
    schema = json.loads(Path(schema_path).read_text())
    jsonschema.validate(config, schema)
    return config
```

## YAML/TOML Configuration

### YAML with Anchors

```yaml
defaults: &defaults
  log_level: INFO
  workers: 4
  timeout: 30

development:
  <<: *defaults
  debug: true
  database_url: postgresql://localhost/dev

production:
  <<: *defaults
  log_level: WARNING
  workers: 16
  database_url: ${DATABASE_URL}  # Resolved at runtime
```

### TOML (pyproject.toml compatible)

```toml
[tool.myapp]
log_level = "INFO"
workers = 4

[tool.myapp.database]
pool_size = 10
timeout = 30
```

## Secrets Management

### Runtime Resolution

```python
import os

def resolve_secret(value: str) -> str:
    if value.startswith("op://"):
        # 1Password reference
        return subprocess.check_output(["op", "read", value]).decode().strip()
    elif value.startswith("file://"):
        # File reference (Docker secrets)
        return Path(value[7:]).read_text().strip()
    elif value.startswith("env://"):
        # Explicit env var reference
        return os.environ[value[6:]]
    return value
```

### Docker Secrets

```python
def load_docker_secret(name: str) -> str:
    secret_path = Path(f"/run/secrets/{name}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    return os.environ.get(name.upper(), "")
```

## Feature Flags

```python
from dataclasses import dataclass

@dataclass
class FeatureFlags:
    new_dashboard: bool = False
    v2_api: bool = False
    experimental_search: bool = False

    @classmethod
    def from_env(cls) -> "FeatureFlags":
        return cls(**{
            field: os.getenv(f"FF_{field.upper()}", "false").lower() == "true"
            for field in cls.__dataclass_fields__
        })
```

## 12-Factor Config Principles

1. **Store config in the environment** — Not in code
2. **Strict separation** — Config varies between deploys; code doesn't
3. **No config groups** (dev/staging/prod) — Each deploy is independently configured
4. **Secrets are config** — Treat them as environment variables, never commit them

## Anti-Patterns

- **Hardcoded configuration** — Always externalize into env vars or config files
- **Secrets in code or git** — Use secret managers or environment variables
- **No validation** — Fail fast on startup if config is invalid
- **Environment-specific code branches** — Config should change behavior, not if/else on env name
- **Overly complex config** — If a value rarely changes, a sensible default beats configurability
- **Missing .env.example** — Always provide a template showing required variables
