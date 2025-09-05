# REST API Spec

Since the project includes a REST API, I'll create an OpenAPI 3.0 specification based on the PRD requirements and data models:

```yaml
openapi: 3.0.0
info:
  title: Synthetic Data Generation Service API
  version: 1.0.0
  description: |
    REST API for generating custom synthetic datasets from natural language descriptions.
    Supports educational use cases with cost-optimized schema caching and CSV export.
    
    **Key Features:**
    - Natural language to synthetic data generation
    - GPT-4o-mini powered schema generation
    - Faker library integration for realistic data
    - Intelligent caching to minimize API costs
    - CSV export optimized for data science workflows

servers:
  - url: http://localhost:8000
    description: Local development server

paths:
  /generate:
    post:
      summary: Generate synthetic dataset from natural language description
      description: |
        Accepts a natural language description of desired dataset characteristics
        and returns a CSV file containing synthetic data matching the description.
        
        **Process:**
        1. Validates input description and parameters
        2. Checks cache for existing schema (SHA-256 hash of description)
        3. Generates schema via GPT-4o-mini if cache miss
        4. Generates synthetic data using Faker library
        5. Returns CSV file with appropriate headers
        
        **Performance:** Target response time <30 seconds per request.
      operationId: generateDataset
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DatasetRequest'
            examples:
              ecommerce:
                summary: E-commerce product dataset
                value:
                  description: "Generate e-commerce product data including product names, prices, categories, brands, and customer ratings for online store analysis"
                  rows: 1000
              healthcare:
                summary: Healthcare patient dataset
                value:
                  description: "Create healthcare patient records with demographics, medical conditions, treatment dates, and billing information for analysis"
                  rows: 500
              finance:
                summary: Financial transaction dataset
                value:
                  description: "Generate financial transaction data with account numbers, transaction types, amounts, dates, and merchant information"
                  rows: 2000
      responses:
        '200':
          description: Successfully generated CSV dataset
          headers:
            Content-Disposition:
              description: Suggested filename for the dataset
              schema:
                type: string
                example: 'attachment; filename="ecommerce_product_data.csv"'
            X-Row-Count:
              description: Number of rows in the generated dataset
              schema:
                type: integer
                example: 1000
            X-Generation-Time:
              description: Time taken to generate the dataset in seconds
              schema:
                type: number
                format: float
                example: 12.5
          content:
            text/csv:
              schema:
                type: string
                format: binary
                description: CSV file containing synthetic dataset with headers
              example: |
                product_name,price,category,brand,rating
                Wireless Bluetooth Headphones,89.99,Electronics,AudioTech,4.2
                Organic Cotton T-Shirt,24.95,Clothing,EcoWear,4.5
                Smart Home Security Camera,159.99,Electronics,SecureView,3.8
        '400':
          description: Invalid request parameters
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              examples:
                empty_description:
                  summary: Missing description
                  value:
                    error_type: "validation"
                    message: "Description field is required and cannot be empty"
                    details:
                      field: "description"
                      provided_value: ""
                    timestamp: "2025-09-05T10:30:00Z"
                invalid_rows:
                  summary: Invalid row count
                  value:
                    error_type: "validation"
                    message: "Row count must be between 1 and 10000"
                    details:
                      field: "rows"
                      provided_value: 15000
                    timestamp: "2025-09-05T10:30:00Z"
        '429':
          description: Rate limit exceeded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error_type: "rate_limit"
                message: "OpenAI API rate limit exceeded. Please try again in 60 seconds"
                details:
                  retry_after: 60
                  limit: "3 requests per minute"
                timestamp: "2025-09-05T10:30:00Z"
        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error_type: "generation_failure"
                message: "Failed to generate synthetic data after multiple attempts"
                details:
                  last_error: "OpenAI API timeout"
                  fallback_used: true
                timestamp: "2025-09-05T10:30:00Z"

  /health:
    get:
      summary: Service health check
      description: Returns service status and basic system information
      operationId: healthCheck
      responses:
        '200':
          description: Service is healthy and operational
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'
              example:
                status: "healthy"
                version: "1.0.0"
                timestamp: "2025-09-05T10:30:00Z"
                dependencies:
                  openai_api: "available"
                  schema_cache: "accessible"
        '503':
          description: Service is temporarily unavailable
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'
              example:
                status: "unhealthy"
                version: "1.0.0"
                timestamp: "2025-09-05T10:30:00Z"
                dependencies:
                  openai_api: "unavailable"
                  schema_cache: "accessible"

components:
  schemas:
    DatasetRequest:
      type: object
      required:
        - description
      properties:
        description:
          type: string
          minLength: 10
          maxLength: 4000
          description: |
            Natural language description of the desired synthetic dataset.
            Should include domain context, field types, and any specific requirements.
          example: "Generate e-commerce product data with names, prices, categories, and ratings"
        rows:
          type: integer
          minimum: 1
          maximum: 10000
          default: 1000
          description: Number of data rows to generate
          example: 1500
        format:
          type: string
          enum: [csv]
          default: csv
          description: Output format (currently only CSV supported)

    ErrorResponse:
      type: object
      required:
        - error_type
        - message
        - timestamp
      properties:
        error_type:
          type: string
          enum: [validation, generation_failure, rate_limit, api_failure]
          description: Category of error that occurred
        message:
          type: string
          description: Human-readable error message
        details:
          type: object
          description: Additional context about the error
          additionalProperties: true
        timestamp:
          type: string
          format: date-time
          description: When the error occurred (ISO 8601 format)

    HealthResponse:
      type: object
      required:
        - status
        - version
        - timestamp
      properties:
        status:
          type: string
          enum: [healthy, unhealthy]
          description: Overall service health status
        version:
          type: string
          description: Service version identifier
        timestamp:
          type: string
          format: date-time
          description: Health check timestamp (ISO 8601 format)
        dependencies:
          type: object
          description: Status of external dependencies
          properties:
            openai_api:
              type: string
              enum: [available, unavailable, degraded]
            schema_cache:
              type: string
              enum: [accessible, inaccessible]
```
