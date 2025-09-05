# Synthetic Data Generation Backend Service - Brainstorming Session

## Executive Summary
- **Topic:** Technical approach for backend service to generate synthetic data based on user-specified domains and features
- **Constraints:** GPT-4o-mini API, 1-hour implementation timeline
- **Session Date:** 2025-09-05
- **Approach:** Analyst-recommended focused ideation techniques

## Session Progress

### Technique 1: Component Breakdown
*Identifying all technical pieces needed for the system*

#### Ideas Generated:

**Input Layer:**
- Natural language description from users
- Example: "Generate customer data with names, emails, purchase amounts"

**Processing Layer:**
- Initially considered LLM-only approach (GPT-4o-mini)
- Open to hybrid or non-LLM approaches for data generation

**Output Layer:**
- CSV file format
- Minimum 1000 rows requirement
- Scalable batch generation

#### Refined Technical Approach:

**Selected Strategy: LLM as Schema Designer Only**
- GPT-4o-mini used ONCE to interpret natural language into data schema
- Traditional libraries (Faker.js/Python Faker) generate the actual 1000+ rows
- Example flow: "I need customer data" → LLM outputs schema → Faker generates data

**Natural Language Processing:**
- Direct to GPT-4o-mini for understanding user intent
- LLM translates requirements into structured schema definition

### Technique 2: Challenge Assumptions & Solutions

#### Schema Format Decision:
**Selected: Simple JSON mapping to Faker methods**
```json
{
  "name": "person.fullName",
  "email": "internet.email", 
  "purchase_amount": "commerce.price",
  "age": {"type": "number.int", "min": 25, "max": 65}
}
```
- Clean, readable format
- Direct mapping to Faker API methods
- Supports parameters for constrained values

### Technique 3: How-Might-We Solutions

#### HMW #1: Handle Custom Domains
**Solution: Composite Generation**
- Combine multiple Faker methods for domain-specific fields
- Example: "diagnosis" → `faker.random.choice(['Hypertension', 'Diabetes', 'Asthma'])`
- GPT-4o-mini can suggest appropriate Faker combinations

#### HMW #2: 1-Hour Implementation Stack
**Decisions:**
- Language: Python
- Framework: FastAPI
- Input: REST endpoint (simpler than CLI for quick implementation)
- Libraries: faker, pandas (for CSV generation)

#### HMW #3: GPT-4o-mini Prompt Instructions
Key instructions for schema generation:
1. "Output only valid JSON schema"
2. "Map to Python Faker methods where possible"
3. "For custom fields, provide array of sample values"

### Technique 4: Complete System Architecture

#### End-to-End Flow Example:
**User Request:** "Generate e-commerce customer data with purchase history"

**Step 1: API Endpoint**
```python
POST /generate
{
  "description": "Generate e-commerce customer data with purchase history",
  "rows": 1000
}
```

**Step 2: GPT-4o-mini Prompt**
```
Convert this request into a Faker schema:
"Generate e-commerce customer data with purchase history"

Rules:
1. Output only valid JSON schema
2. Map to Python Faker methods where possible  
3. For custom fields, provide array of sample values

Output format: {"field_name": "faker.method" or {"type": "method", "params": {...}}}
```

**Step 3: Schema Response & Storage**
- GPT returns JSON schema
- **Store schemas for reuse** (cache by description hash)
- Skip validation, error handling for MVP
- Focus on happy path only

**Step 4: Generate Data**
- Use Faker with stored schema
- Generate 1000 rows
- Export as CSV

#### MVP Scope Decisions:
- Schema caching/storage for reuse (YES)
- Validation (skip for 1-hour timeline)
- Error handling (happy path only)
- Multiple format outputs (CSV only)

### Final Implementation Decisions

#### Technical Specifications:

**1. Schema Storage:** 
- JSON file (`schemas.json`) for persistence between restarts
- Key: hash of description, Value: schema object

**2. Project Structure:**
```
synthetic-data-service/
├── main.py          # FastAPI app + all logic
├── pyproject.toml   # fastapi, faker, pandas, openai (uv managed)
└── schemas.json     # cached schemas
```

**3. Faker Mapping:**
```python
# Simple getattr approach
value = getattr(faker, method_name)()
```

**4. Test Case:**
- Complex: "Generate product inventory with SKUs and stock levels"
- Expected fields: product_id, sku, product_name, category, stock_level, price, warehouse_location

## Implementation Blueprint Summary

### Core Architecture:
1. **Single API call to GPT-4o-mini** to translate natural language to schema
2. **Python Faker library** generates 1000+ rows from schema
3. **JSON file caching** prevents duplicate API calls
4. **FastAPI endpoint** accepts POST requests with description and row count
5. **CSV output** with pandas for easy data consumption

### Quick Start Implementation Path:

#### Phase 1 (0-20 minutes): Core Setup
- Initialize FastAPI project with single main.py
- Set up POST endpoint `/generate`
- Create OpenAI client with GPT-4o-mini

#### Phase 2 (20-40 minutes): Schema Generation
- Write prompt template for GPT-4o-mini
- Implement schema caching with JSON file
- Parse GPT response into usable schema

#### Phase 3 (40-60 minutes): Data Generation
- Map schema to Faker methods using getattr
- Generate specified number of rows
- Convert to pandas DataFrame and export CSV

### Code Skeleton:
```python
# main.py
from fastapi import FastAPI
from faker import Faker
import pandas as pd
import json
import hashlib
from openai import OpenAI

app = FastAPI()
faker = Faker()
client = OpenAI()

@app.post("/generate")
async def generate_data(description: str, rows: int = 1000):
    # 1. Check schema cache
    # 2. If not cached, call GPT-4o-mini
    # 3. Generate data with Faker
    # 4. Return CSV
    pass
```

### Key Advantages:
- **Cost-efficient:** One API call serves unlimited data generation
- **Fast:** Faker generates thousands of rows in seconds
- **Reusable:** Cached schemas eliminate redundant API calls
- **Extensible:** Easy to add new data types or output formats later

### Next Steps:
1. Create project directory and pyproject.toml with uv
2. Implement the FastAPI endpoint
3. Test with product inventory example
4. Iterate based on results
