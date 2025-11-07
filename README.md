# Synthetic Data Generator From User Prompt

A FastAPI-based service that generates realistic synthetic datasets from natural language descriptions. Built with the assistance of **BMAD (Breakthrough Method of Agile AI-Driven Development)** methodology and **Claude Code**.

## Features

- **Gradio Web Interface**: User-friendly web UI for generating datasets without code
- **Natural Language Input**: Describe your dataset needs in plain English
- **Intelligent Schema Generation**: Powered by OpenAI GPT-4o-mini for Faker-compatible schemas
- **High-Quality Synthetic Data**: Uses Faker library with 80+ field types and domain-specific values
- **Multiple Domains**: E-commerce, healthcare, finance, education, and general datasets
- **CSV Export**: Ready-to-use CSV files compatible with pandas, Excel, and data science tools
- **Performance Optimized**: Generate 1,000+ rows/second with sub-30-second response times
- **Schema Caching**: Intelligent caching reduces API costs and improves performance
- **REST API**: Full-featured API for programmatic access
- **Heroku Ready**: Single-dyno deployment for cost-effective hosting

## API Endpoints

### Generate Dataset
```
POST /api/v1/generate
```

**Request Body:**
```json
{
  "description": "E-commerce product catalog with names, prices, and categories",
  "rows": 1000,
  "format": "csv"
}
```

**Response:** CSV file download with appropriate headers

### Health Check
```
GET /health
```

### Cache Statistics
```
GET /api/v1/cache/stats
```

## Installation

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd data_generator_from_user_prompt

# Install dependencies
uv sync

# Create environment configuration
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Environment Variables
```bash
# API Provider (openai or anthropic)
API_PROVIDER=openai  # or anthropic

# API Keys (set one based on your provider)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Demo Mode (true = no API key needed, false = uses API)
DEMO_MODE=false

# Optional settings
CACHE_ENABLED=true
LOG_LEVEL=INFO
```

## BMAD Setup

This project uses the **BMAD** methodology for systematic development. To set up BMAD for this project, refer to [this official repository](https://github.com/bmad-code-org/BMAD-METHOD) for more information.

## Running the Service

### Start the Server (with Gradio Frontend)
```bash
# Install dependencies (including Gradio)
uv sync

# Set your OpenAI API key
export OPENAI_API_KEY=your_key_here

# Run the integrated application
uv run python main.py
```

### Access the Application
- **Gradio Web Interface**: http://localhost:8000/gradio (or http://localhost:8000/)
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Cache Stats**: http://localhost:8000/api/v1/cache/stats

### Using the Gradio Interface

The Gradio interface provides an intuitive way to generate datasets:

1. **Enter Description**: Describe your dataset in natural language
2. **Set Row Count**: Choose how many rows to generate (1-10,000)
3. **Generate**: Click the generate button
4. **Preview**: View the first 100 rows in your browser
5. **Download**: Download the complete dataset as CSV

**Example Prompts:**
- "E-commerce product catalog with product names, categories, prices, ratings, and stock status"
- "Healthcare patient records with names, ages, blood types, medical conditions, and departments"
- "Financial transactions with account holders, account numbers, transaction amounts, dates, and merchants"

## Architecture

### Services
- **SchemaGenerator**: Converts natural language to Faker-compatible schemas using OpenAI
- **DataGenerator**: Generates realistic synthetic data using Faker library
- **CSVExporter**: Converts generated data to CSV format with proper headers
- **SchemaCache**: Caches generated schemas to reduce API costs

### Data Flow
```
Natural Language → Schema Generation → Data Generation → CSV Export → HTTP Response
```

### Performance
- **Throughput**: 500-18,000+ rows/second depending on dataset size
- **Response Time**: Complete pipeline typically under 1 second for 1,000 rows
- **Scalability**: Supports 1-10,000 rows per request

## Sample Output

The service generates realistic data across multiple domains:

### E-commerce
```csv
"product_name","category","brand","price","rating","in_stock","sku"
"Balanced web-enabled alliance","Clothing","Apple","sample_price_0","5","True","693"
"Robust background productivity","Clothing","Amazon","sample_price_1","3","True","781"
```

### Healthcare
```csv
"patient_name","age","gender","blood_type","condition","department"
"Roy Livingston","22","Male","O+","Heart Disease","Emergency"
"Aaron Rich","78","Male","B-","Arthritis","Neurology"
```

### Finance
```csv
"account_holder","account_number","account_type","balance","transaction_date","merchant"
"Anna Berger","194","Loan","sample_balance_0","2024-10-24","Stafford, Kennedy and Young"
"Elizabeth Esparza","76","Credit","sample_balance_1","2024-04-11","Fox Inc"
```

## Development

This project was developed using modern software engineering practices:

### Methodology
- **BMAD Framework**: Breakthrough Method of Agile AI-Driven Development approach for systematic development
- **Story-Driven Development**: Feature implementation based on user stories and acceptance criteria

### Tools Used
- **Claude Code**: AI-powered development assistant for code generation and architecture design
- **FastAPI**: Modern, high-performance web framework for APIs
- **Pydantic**: Data validation and settings management
- **Faker**: Library for generating fake data
- **Pandas**: Data manipulation and CSV export
- **uv**: Fast Python package manager and project manager

### Code Quality
- **Type Hints**: Full type annotation throughout the codebase
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Performance**: Optimized for high throughput and low latency
- **Testing**: Manual testing framework with comprehensive test scenarios

## Project Structure

```
data_generator_from_user_prompt/
├── src/
│   ├── api/
│   │   ├── models.py          # Pydantic models
│   │   └── routes.py          # FastAPI routes
│   ├── frontend/
│   │   └── gradio_app.py      # Gradio web interface
│   ├── services/
│   │   ├── schema_generator.py # OpenAI integration
│   │   ├── data_generator.py   # Faker-based data generation
│   │   ├── csv_exporter.py     # CSV export functionality
│   │   └── cache_service.py    # Schema caching
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── exceptions.py      # Custom exceptions
│   └── utils/
│       ├── hash_utils.py      # Hashing utilities
│       └── file_operations.py # File I/O utilities
├── data/                      # Cache storage (git-ignored)
├── docs/stories/              # User stories and documentation
├── main.py                    # Application entry point
├── test_full_pipeline.py      # Complete pipeline testing
├── Procfile                   # Heroku deployment config
├── runtime.txt                # Python version for Heroku
├── requirements.txt           # Python dependencies
├── DEPLOYMENT.md              # Deployment guide
└── README.md
```

## Deployment

### Heroku Deployment

This application is configured for easy deployment to Heroku with a single Basic dyno ($7/month):

#### Initial Setup

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name
```

#### Configure Environment Variables

**Choose Your API Provider:**

```bash
# For Anthropic Claude
heroku config:set API_PROVIDER=anthropic
heroku config:set ANTHROPIC_API_KEY=your_anthropic_api_key_here

# OR for OpenAI
heroku config:set API_PROVIDER=openai
heroku config:set OPENAI_API_KEY=your_openai_api_key_here

# Optional: Enable caching
heroku config:set CACHE_ENABLED=true
```

**Switch Between Demo Mode and Production Mode:**

```bash
# Enable Demo Mode (No API Key Required)
heroku config:set DEMO_MODE=true
heroku restart

# Enable Production Mode (Uses API)
heroku config:set DEMO_MODE=false
heroku restart
```

**Verify Configuration:**

```bash
# View all environment variables
heroku config
```

#### Deploy Application

```bash
# Deploy from your feature branch to Heroku's main branch
git push heroku your-branch-name:main

# Note: Heroku always deploys from the main branch.
# The command above pushes your feature branch to Heroku's main branch.

# OR deploy from main branch
git push heroku main
```

#### Scale Dynos

```bash
# Scale to 1 Basic dyno (starts the app)
heroku ps:scale web=1

# Scale down to 0 (stops the app to save costs)
heroku ps:scale web=0

# View current dyno status
heroku ps
```

#### Access Your Application

```bash
# Open application in browser
heroku open

# Get application URL
heroku info | grep "Web URL"
```

#### Monitor and Debug

```bash
# View real-time logs
heroku logs --tail

# View recent logs
heroku logs

# View app information
heroku info

# Restart application
heroku restart
```

#### Managing Your Heroku App

```bash
# View app info (includes dyno type, region, URL, etc.)
heroku info

# Restart app (useful after config changes)
heroku restart

# View current dyno type and status
heroku ps

# View all environment variables
heroku config

# Remove an environment variable
heroku config:unset VARIABLE_NAME
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Local Development

```bash
# Install dependencies
uv sync

# Set environment variables
export OPENAI_API_KEY=your_key_here
export CACHE_ENABLED=true

# Run application
uv run python main.py

# Access at http://localhost:8000
```

## Contributing

This project demonstrates modern AI-assisted development practices:

1. **User Story Development**: Each feature implemented based on detailed acceptance criteria
2. **Test-Driven Approach**: Comprehensive testing without external API dependencies
3. **Performance Focus**: Built with scalability and speed requirements in mind
4. **Documentation**: Clear documentation and examples for easy adoption