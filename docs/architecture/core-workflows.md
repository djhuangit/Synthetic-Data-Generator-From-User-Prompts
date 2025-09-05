# Core Workflows

I'll illustrate the key system workflows using sequence diagrams to show component interactions and data flow:

## Primary Dataset Generation Workflow

```mermaid
sequenceDiagram
    participant Client as Data Science Learner
    participant API as APIController
    participant Cache as SchemaCache
    participant SchemaGen as SchemaGenerator
    participant OpenAI as OpenAI API
    participant DataGen as DataGenerator
    participant Faker as Faker Library
    participant CSV as CSVExporter
    
    Client->>API: POST /generate {"description": "e-commerce product data", "rows": 1000}
    API->>API: Validate request parameters
    
    Note over API,Cache: Schema Retrieval Phase
    API->>Cache: get_cached_schema(hash("e-commerce product data"))
    
    alt Schema Cache Miss
        Cache-->>API: None (not cached)
        API->>SchemaGen: generate_schema("e-commerce product data")
        SchemaGen->>OpenAI: POST /chat/completions with prompt
        OpenAI-->>SchemaGen: JSON schema mapping fields to Faker methods
        SchemaGen->>SchemaGen: Validate and parse JSON response
        SchemaGen->>Cache: save_schema(hash, GeneratedSchema)
        Cache-->>SchemaGen: Success
        SchemaGen-->>API: GeneratedSchema object
    else Schema Cache Hit
        Cache-->>API: Cached GeneratedSchema object
    end
    
    Note over API,CSV: Data Generation Phase
    API->>DataGen: generate_data(schema, 1000)
    DataGen->>DataGen: Map schema fields to Faker methods
    
    loop For each of 1000 rows
        DataGen->>Faker: Call mapped Faker methods
        Faker-->>DataGen: Generated field values
    end
    
    DataGen-->>API: SyntheticDataset object
    
    Note over API,Client: CSV Export Phase
    API->>CSV: export_to_csv(SyntheticDataset)
    CSV->>CSV: Convert to DataFrame and generate CSV
    CSV-->>API: DatasetResponse with CSV content
    
    API-->>Client: HTTP 200 with CSV file and headers
```

## Error Handling Workflow

```mermaid
sequenceDiagram
    participant Client as Data Science Learner
    participant API as APIController
    participant SchemaGen as SchemaGenerator
    participant OpenAI as OpenAI API
    
    Client->>API: POST /generate with invalid description
    
    alt OpenAI API Failure
        API->>SchemaGen: generate_schema(description)
        SchemaGen->>OpenAI: POST /chat/completions
        OpenAI-->>SchemaGen: 429 Rate Limit Error
        SchemaGen->>SchemaGen: Exponential backoff retry (3 attempts)
        OpenAI-->>SchemaGen: 500 Server Error
        SchemaGen->>SchemaGen: Fall back to basic schema template
        SchemaGen-->>API: Basic GeneratedSchema
        Note right of SchemaGen: Logs error but continues with fallback
    else Invalid JSON Response
        SchemaGen->>OpenAI: POST /chat/completions
        OpenAI-->>SchemaGen: Malformed JSON response
        SchemaGen->>SchemaGen: JSON parsing fails
        SchemaGen->>SchemaGen: Retry with refined prompt
        OpenAI-->>SchemaGen: Valid JSON schema
        SchemaGen-->>API: GeneratedSchema
    else Request Validation Error
        API->>API: Validate request (empty description)
        API-->>Client: HTTP 400 {"error_type": "validation", "message": "Description required"}
    end
```

## Concurrent Request Handling

```mermaid
sequenceDiagram
    participant Client1 as Learner A
    participant Client2 as Learner B
    participant API as APIController
    participant Cache as SchemaCache
    participant FileSystem as schemas.json
    
    Note over Client1,FileSystem: Concurrent identical requests
    
    Client1->>API: POST /generate {"description": "healthcare patient data"}
    Client2->>API: POST /generate {"description": "healthcare patient data"}
    
    par Request A Processing
        API->>Cache: get_cached_schema(hash("healthcare patient data"))
        Cache->>FileSystem: Read schemas.json with file lock
        FileSystem-->>Cache: Schema not found
        Cache-->>API: None
        Note right of API: Proceeds to OpenAI API call
    and Request B Processing  
        API->>Cache: get_cached_schema(hash("healthcare patient data"))
        Cache->>FileSystem: Wait for file lock release
        FileSystem-->>Cache: Schema found (saved by Request A)
        Cache-->>API: Cached GeneratedSchema
        Note right of API: Skips OpenAI API call
    end
    
    Note over Client1,Client2: Both receive consistent results
    API-->>Client1: CSV dataset
    API-->>Client2: CSV dataset (from cache)
```
