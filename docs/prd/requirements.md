# Requirements

## Functional

- **FR1:** The service SHALL accept natural language descriptions via REST API POST endpoint with a 'description' field containing the dataset requirements in plain English
- **FR2:** The service SHALL process natural language input through GPT-4o-mini to generate a JSON schema mapping field names to Faker library methods
- **FR3:** The service SHALL cache generated schemas using a hash of the description to avoid redundant API calls for identical requests
- **FR4:** The service SHALL generate a minimum of 1000 rows of synthetic data using the Faker library based on the generated schema
- **FR5:** The service SHALL return data in CSV format with appropriate headers matching the schema field names
- **FR6:** The service SHALL complete the entire generation process (request to CSV delivery) within 30 seconds for standard requests
- **FR7:** The service SHALL support common data types including names, emails, dates, numbers, categories, and addresses without additional configuration
- **FR8:** The service SHALL handle at least 5 domain types: e-commerce, healthcare, finance, education, and social media
- **FR9:** The service SHALL provide meaningful error messages when unable to interpret a natural language request

## Non Functional

- **NFR1:** The service MUST operate within GPT-4o-mini token limits (approximately 4000 tokens per request)
- **NFR2:** The service MUST minimize OpenAI API costs by caching schemas and making single API calls per unique request
- **NFR3:** The service MUST be implementable by a single developer within a 1-hour timeframe
- **NFR4:** The service MUST run on Python 3.12+ across Linux, Mac, and Windows platforms
- **NFR5:** The service MUST handle concurrent requests without file corruption in the schema cache
- **NFR6:** The service MUST protect the OpenAI API key through environment variable configuration
- **NFR7:** The service MUST generate data with sufficient variety to avoid obvious repetition patterns in 1000+ row datasets
- **NFR8:** The service MUST operate as a stateless REST API requiring no user authentication for MVP
