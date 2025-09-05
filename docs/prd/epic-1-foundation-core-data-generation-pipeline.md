# Epic 1: Foundation & Core Data Generation Pipeline

**Goal:** Create a fully functional REST API service that accepts natural language descriptions and returns synthetic CSV datasets, establishing all necessary infrastructure, integrations, and core functionality to enable data science learners to generate custom datasets for their projects.

## Story 1.1: Project Setup and Infrastructure

As a developer,
I want to set up the Python project with FastAPI and all required dependencies,
so that I have a working foundation for building the data generation service.

### Acceptance Criteria
1. Python project initialized with uv virtual environment (Python 3.12+)
2. pyproject.toml created with FastAPI, uvicorn, pandas, faker, openai, and python-dotenv dependencies
3. Basic FastAPI app structure created in main.py with health check endpoint
4. .env file configured for OpenAI API key storage
5. Server starts successfully with uvicorn and health check returns 200 OK

## Story 1.2: Schema Generation via GPT-4o-mini

As a data science learner,
I want to submit a natural language description of my dataset needs,
so that the system can understand and create an appropriate schema for data generation.

### Acceptance Criteria
1. POST endpoint `/generate` accepts JSON with 'description' and optional 'rows' fields
2. OpenAI client configured and successfully connects to GPT-4o-mini
3. Prompt template created that instructs GPT-4o-mini to output Faker-compatible schema
4. GPT-4o-mini response parsed into valid JSON schema object
5. Error handling returns meaningful message if schema generation fails

## Story 1.3: Schema Caching Implementation

As a service operator,
I want generated schemas to be cached,
so that identical requests don't incur additional API costs.

### Acceptance Criteria
1. Hash function implemented for description text (consistent across requests)
2. schemas.json file created/loaded for persistent cache storage
3. Cache checked before making OpenAI API call
4. New schemas saved to cache after successful generation
5. Cache hit returns stored schema without API call

## Story 1.4: Synthetic Data Generation with Faker

As a data science learner,
I want the service to generate realistic synthetic data based on the schema,
so that I receive high-quality datasets for my projects.

### Acceptance Criteria
1. Faker instance initialized and schema fields mapped to Faker methods
2. 1000+ rows generated based on schema (or user-specified count)
3. Common data types supported: names, emails, dates, numbers, categories, addresses
4. Data variety maintained across rows (no obvious repetition patterns)
5. Custom domain values handled via random.choice when Faker method unavailable

## Story 1.5: CSV Export and Response

As a data science learner,
I want to receive my generated data as a CSV file,
so that I can immediately use it in pandas, Excel, or other data science tools.

### Acceptance Criteria
1. Generated data converted to pandas DataFrame
2. DataFrame exported to CSV format with proper headers
3. CSV returned as response with appropriate content-type headers
4. Response includes suggested filename based on description
5. Complete request-to-CSV process executes within 30 seconds
