# Tech Stack

## Cloud Infrastructure

- **Provider:** None for MVP (local deployment)
- **Key Services:** N/A (file system only)
- **Deployment Regions:** Local development environment

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
|----------|------------|---------|---------|-----------|
| **Language** | Python | 3.12.0 | Primary development language | PRD requirement, modern features, excellent AI/ML ecosystem |
| **Framework** | FastAPI | 0.104.1 | REST API framework | PRD specified, rapid development, auto documentation |
| **ASGI Server** | Uvicorn | 0.24.0 | Application server | Standard FastAPI deployment, development server |
| **AI Integration** | OpenAI | 1.3.7 | GPT-4o-mini integration | PRD specified, official SDK, cost-effective model |
| **Data Generation** | Faker | 19.12.0 | Synthetic data creation | PRD specified, comprehensive data types, domain support |
| **Data Processing** | Pandas | 2.1.3 | CSV generation and manipulation | PRD specified, standard for data science workflows |
| **Configuration** | python-dotenv | 1.0.0 | Environment variable management | PRD specified, secure API key handling |
| **Development** | pyproject.toml | - | Dependency management with uv | Modern Python packaging, uv-based virtual env management |
