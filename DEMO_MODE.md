# Demo Mode - Testing Without OpenAI API Key

This guide explains how to test the entire application stack (Gradio frontend, FastAPI backend, and all services) **without needing an OpenAI API key**.

## What is Demo Mode?

Demo Mode allows you to:
- ✅ Test the complete application flow (Gradio UI → FastAPI → Backend → CSV export)
- ✅ Verify Gradio and FastAPI integration
- ✅ Test deployment configurations before production
- ✅ Develop and debug without incurring API costs
- ✅ Demo the application to stakeholders without API access

**How it works**: Instead of calling OpenAI's API to generate schemas, Demo Mode uses a `MockSchemaGenerator` with predefined templates for common data domains.

## Quick Start

### 1. Enable Demo Mode

Set the `DEMO_MODE` environment variable to `true`:

```bash
# Linux/Mac
export DEMO_MODE=true

# Windows (PowerShell)
$env:DEMO_MODE="true"

# Windows (CMD)
set DEMO_MODE=true
```

### 2. Run the Application

```bash
# Start the server
DEMO_MODE=true uv run python main.py

# Or with hot reload for development
DEMO_MODE=true uv run uvicorn main:app --reload
```

### 3. Access the Application

- **Gradio Interface**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

The health check will show `"demo_mode": true` when enabled.

## Supported Data Domains

Demo Mode includes pre-configured templates for:

### 1. E-commerce
**Keywords**: ecommerce, product, shop, store, catalog

**Fields**:
- product_name (catch phrase)
- category (word)
- brand (company name)
- price (decimal 10-1000)
- rating (integer 1-5)
- in_stock (boolean)
- sku (product code)

**Example prompt**: *"E-commerce product catalog with names, prices, and categories"*

### 2. Healthcare
**Keywords**: healthcare, patient, medical, hospital, health

**Fields**:
- patient_name
- age (1-100)
- gender (Male/Female/Other)
- blood_type (A+, A-, B+, B-, AB+, AB-, O+, O-)
- condition (common conditions)
- department (hospital departments)

**Example prompt**: *"Healthcare patient records with medical conditions"*

### 3. Finance
**Keywords**: finance, account, bank, transaction, payment

**Fields**:
- account_holder
- account_number
- account_type (Checking/Savings/Credit/Loan)
- balance (100-100000)
- transaction_date
- merchant

**Example prompt**: *"Financial transactions with account details"*

### 4. Business/Employee
**Keywords**: employee, staff, worker, job, salary

**Fields**:
- employee_name
- job_title
- department (Engineering/Sales/Marketing/HR/Finance)
- salary (40000-200000)
- hire_date
- email

**Example prompt**: *"Employee database with job titles and salaries"*

### 5. Social Media
**Keywords**: social, user, profile, follower, post

**Fields**:
- username
- bio
- followers (0-1000000)
- posts (0-10000)
- registration_date
- verified (boolean)

**Example prompt**: *"Social media user profiles with followers"*

### 6. Education
**Keywords**: student, education, school, grade, university

**Fields**:
- student_name
- student_id
- grade (1-12)
- gpa (0.00-4.00)
- major (various subjects)
- enrollment_date

**Example prompt**: *"Student records with grades and GPAs"*

### 7. General (Default)
If no keywords match, uses a general template:

**Fields**:
- id (UUID)
- name
- email
- phone
- address
- created_at

## Running the Test Suite

We've included a comprehensive test script that validates the entire stack:

```bash
# Run the full test suite
uv run python test_demo_mode.py
```

### What Gets Tested:

1. **Configuration** - DEMO_MODE enabled, no API key required
2. **Mock Schema Generator** - All 7 domain templates
3. **Data Generation** - Faker integration and data quality
4. **CSV Export** - CSV formatting and download
5. **FastAPI Routes** - Health check, generate endpoint, cache stats
6. **Gradio Integration** - UI mounting and interface creation

**Expected output**:
```
============================================================
🎉 All tests passed! Demo mode is working perfectly!
============================================================

You can now run the application without an API key:
  DEMO_MODE=true uv run python main.py
```

## Using Demo Mode

### Via Gradio UI

1. Start the application with `DEMO_MODE=true`
2. Navigate to http://localhost:8000/
3. Enter a description (use keywords from supported domains)
4. Set the number of rows
5. Click "Generate Dataset"
6. Preview and download your CSV

### Via API

```bash
# Test the generate endpoint
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "E-commerce products with prices and ratings",
    "rows": 50,
    "format": "csv"
  }'

# Check health (shows demo_mode status)
curl http://localhost:8000/health
```

**Response headers in Demo Mode:**
- `X-Demo-Mode: true` - Indicates demo mode is active
- `X-Domain: ecommerce` - Detected domain
- `X-Generation-Time: 0.123` - Processing time

## Limitations

### What Demo Mode Does NOT Do:

- ❌ Call OpenAI API (uses predefined templates)
- ❌ Generate custom schemas (limited to 7 domains)
- ❌ Learn from descriptions (keyword-based matching)
- ❌ Cache schemas (since they're predefined)

### When to Use Production Mode:

Use production mode (with OpenAI API key) when you need:
- Custom field definitions
- Complex schema generation
- Domain-specific terminology
- Flexible field types and validations

## Environment Variables

| Variable | Demo Mode | Production Mode |
|----------|-----------|-----------------|
| `DEMO_MODE` | `true` | `false` (default) |
| `OPENAI_API_KEY` | Not required | **Required** |
| `CACHE_ENABLED` | Optional | Recommended |

## Deployment on Heroku

Demo Mode works on Heroku too! Great for testing your deployment:

```bash
# Set demo mode on Heroku
heroku config:set DEMO_MODE=true

# Test the deployment
heroku open

# When ready for production, disable demo mode and add API key
heroku config:set DEMO_MODE=false
heroku config:set OPENAI_API_KEY=your_key_here
```

## Troubleshooting

### Demo Mode Not Working

**Check environment variable:**
```bash
# Linux/Mac
echo $DEMO_MODE

# Python
python -c "import os; print(os.getenv('DEMO_MODE'))"
```

**Verify in health check:**
```bash
curl http://localhost:8000/health | jq '.demo_mode'
# Should return: true
```

### Template Not Matching

If you're not getting the expected domain:

1. **Check your keywords**: Use exact keywords from the supported domains
2. **Be specific**: "ecommerce products" works better than "products"
3. **View detected domain**: Check the `X-Domain` response header

### Need Custom Fields?

Demo Mode uses fixed templates. For custom schemas:
- Switch to production mode with an OpenAI API key
- Or modify the templates in `src/services/mock_schema_generator.py`

## Development

### Adding New Templates

Edit `src/services/mock_schema_generator.py`:

```python
self.templates["your_domain"] = {
    "domain": "your_domain",
    "schema": {
        "field_name": {"faker_method": "method_name"},
        # ... more fields
    }
}
```

Then add keyword matching:
```python
elif any(word in description_lower for word in ["keyword1", "keyword2"]):
    template_key = "your_domain"
```

## Summary

Demo Mode enables full-stack testing without OpenAI API costs:

✅ **Perfect for**:
- Initial development and testing
- Deployment verification
- Demonstrations and POCs
- CI/CD pipelines

❌ **Not suitable for**:
- Production data generation
- Custom schema requirements
- Complex domain modeling

**Remember**: Set `DEMO_MODE=false` and add your `OPENAI_API_KEY` for production use!
