# Source Tree

Based on the chosen repository structure (monorepo), service architecture (monolith), and tech stack (Python/FastAPI), here's the project folder structure:

```
synthetic-data-service/
├── pyproject.toml                 # uv dependency management and project config
├── uv.lock                        # uv lock file for reproducible builds
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore patterns
├── README.md                      # Project documentation
├── main.py                        # FastAPI application entry point
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # FastAPI route definitions
│   │   └── models.py              # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── schema_generator.py    # OpenAI integration for schema generation
│   │   ├── data_generator.py      # Faker integration for data generation
│   │   ├── csv_exporter.py        # CSV export functionality
│   │   └── cache_service.py       # File-based schema caching
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── exceptions.py          # Custom exception classes
│   │   └── logging.py             # Logging configuration
│   └── utils/
│       ├── __init__.py
│       ├── file_operations.py     # File I/O utilities with locking
│       └── hash_utils.py          # SHA-256 hashing for cache keys
├── data/
│   ├── schemas.json               # Schema cache file (git-ignored)
│   └── schemas.json.backup        # Backup cache file (git-ignored)
├── tests/                         # Future test organization (manual testing for MVP)
│   ├── __init__.py
│   ├── test_api.py               # API endpoint tests
│   ├── test_services.py          # Service layer tests
│   └── fixtures/
│       └── sample_schemas.json   # Test data fixtures
├── docs/
│   ├── api.md                    # API documentation
│   └── examples/                 # Usage examples
│       ├── ecommerce_request.json
│       ├── healthcare_request.json
│       └── finance_request.json
└── scripts/
    ├── dev_setup.sh              # Development environment setup
    ├── run_local.sh              # Local development server script
    └── cache_cleanup.py          # Cache maintenance utilities
```
