# External APIs

Based on the PRD requirements and component design, the system requires integration with one external service:

## OpenAI API

- **Purpose:** Generate JSON schemas from natural language descriptions using GPT-4o-mini model for cost-effective synthetic data schema creation
- **Documentation:** https://platform.openai.com/docs/api-reference
- **Base URL(s):** https://api.openai.com/v1
- **Authentication:** Bearer token via OpenAI API key stored in environment variables
- **Rate Limits:** 3 requests per minute, 200 requests per day (free tier), up to 10,000 tokens per minute

**Key Endpoints Used:**
- `POST /chat/completions` - Submit natural language descriptions and receive structured JSON schemas compatible with Faker library methods

**Integration Notes:** 
- **Cost optimization:** Implement aggressive caching via SHA-256 hash of descriptions to minimize API calls for identical requests
- **Model specification:** Use "gpt-4o-mini" model specifically for cost efficiency while maintaining schema generation quality
- **Token management:** Keep prompts under 4000 tokens per PRD constraint, implement truncation if descriptions exceed limits
- **Error handling:** Implement retry logic with exponential backoff for rate limit errors, fallback to basic schema templates for API failures
- **Prompt engineering:** Use structured prompts that consistently return JSON objects mapping field names to Faker method calls
- **Response parsing:** Validate all responses contain valid JSON before processing, handle malformed responses gracefully
