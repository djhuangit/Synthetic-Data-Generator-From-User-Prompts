# Database Schema

Since the system uses file-based storage rather than a traditional database, I'll define the JSON schema structure for the schemas.json cache file:

## Schema Cache File Structure (schemas.json)

```json
{
  "cache_metadata": {
    "version": "1.0",
    "created_at": "2025-09-05T10:00:00Z",
    "last_updated": "2025-09-05T10:30:00Z",
    "total_schemas": 15
  },
  "schemas": {
    "a1b2c3d4e5f6...": {
      "description_hash": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
      "original_description": "Generate e-commerce product data including product names, prices, categories, brands, and customer ratings for online store analysis",
      "schema": {
        "product_name": {
          "faker_method": "fake.company() + ' ' + fake.word().title()",
          "data_type": "string",
          "description": "Product name combining company and descriptive word"
        },
        "price": {
          "faker_method": "fake.pydecimal(left_digits=3, right_digits=2, positive=True)",
          "data_type": "decimal",
          "description": "Product price in USD"
        },
        "category": {
          "faker_method": "fake.random_element(['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports'])",
          "data_type": "string",
          "description": "Product category"
        },
        "brand": {
          "faker_method": "fake.company()",
          "data_type": "string",
          "description": "Brand name"
        },
        "rating": {
          "faker_method": "fake.pyfloat(left_digits=1, right_digits=1, min_value=1.0, max_value=5.0)",
          "data_type": "float",
          "description": "Customer rating from 1.0 to 5.0"
        }
      },
      "domain": "e-commerce",
      "created_at": "2025-09-05T10:15:00Z",
      "usage_count": 3,
      "last_used": "2025-09-05T10:30:00Z"
    }
  }
}
```
