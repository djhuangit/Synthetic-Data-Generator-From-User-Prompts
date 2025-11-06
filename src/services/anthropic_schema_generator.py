"""Schema generation service using Anthropic Claude API."""

import json
import asyncio
from datetime import datetime
from typing import Dict, Any
import time
from anthropic import AsyncAnthropic

from src.core.config import settings
from src.core.exceptions import (
    SchemaGenerationError,
    RateLimitError,
    APIConnectionError,
    ParsingError,
    ValidationError
)
from src.api.models import GeneratedSchema
from src.utils.hash_utils import generate_cache_key
from src.services.cache_service import SchemaCache


class AnthropicSchemaGenerator:
    """Service for generating Faker-compatible schemas using Anthropic Claude."""

    def __init__(self) -> None:
        """Initialize the schema generator with Anthropic client."""
        settings.validate_settings()
        self.client = AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            timeout=settings.API_REQUEST_TIMEOUT
        )
        self.model = settings.ANTHROPIC_MODEL
        self.max_tokens = settings.ANTHROPIC_MAX_TOKENS
        self.temperature = settings.ANTHROPIC_TEMPERATURE

        # Initialize cache service
        if settings.CACHE_ENABLED:
            try:
                self.cache = SchemaCache()
            except Exception:
                # Cache initialization failed, disable caching
                self.cache = None
        else:
            self.cache = None

        # Rate limiting tracking
        self._request_times: list = []
        self._daily_request_count = 0
        self._last_reset_date = datetime.now().date()

    def _check_rate_limits(self) -> None:
        """
        Check if rate limits would be exceeded by this request.

        Raises:
            RateLimitError: If rate limits would be exceeded
        """
        now = datetime.now()

        # Reset daily counter if new day
        if now.date() > self._last_reset_date:
            self._daily_request_count = 0
            self._last_reset_date = now.date()

        # Check daily limit
        if self._daily_request_count >= settings.RATE_LIMIT_REQUESTS_PER_DAY:
            raise RateLimitError(
                f"Daily request limit of {settings.RATE_LIMIT_REQUESTS_PER_DAY} exceeded. "
                "Try again tomorrow."
            )

        # Clean old request times (older than 1 minute)
        cutoff_time = now.timestamp() - 60
        self._request_times = [t for t in self._request_times if t > cutoff_time]

        # Check per-minute limit
        if len(self._request_times) >= settings.RATE_LIMIT_REQUESTS_PER_MINUTE:
            raise RateLimitError(
                f"Rate limit exceeded: {settings.RATE_LIMIT_REQUESTS_PER_MINUTE} "
                "requests per minute. Please wait before trying again."
            )

    def _record_request(self) -> None:
        """Record a successful request for rate limiting."""
        self._request_times.append(time.time())
        self._daily_request_count += 1

    def _create_prompt(self, description: str) -> str:
        """
        Create a structured prompt for schema generation.

        Args:
            description: User's dataset description

        Returns:
            str: Formatted prompt for Claude
        """
        prompt = f"""You are a data schema generator. Create a JSON schema for synthetic data generation using Python Faker library.

User Request: "{description}"

Generate a JSON object with the following structure:
{{
    "domain": "category_name",
    "fields": {{
        "field_name_1": {{
            "faker_method": "method_name",
            "parameters": {{}},
            "description": "field description"
        }},
        "field_name_2": {{
            "faker_method": "method_name",
            "parameters": {{}},
            "description": "field description"
        }}
    }}
}}

Requirements:
1. Use only valid Faker methods (e.g., "name", "email", "address", "phone_number", "date", "text", "random_int", etc.)
2. Include 3-15 relevant fields based on the description
3. Set appropriate parameters for each Faker method
4. Infer the domain category (e.g., "ecommerce", "healthcare", "finance", "education", "social_media")
5. Ensure field names are descriptive and snake_case
6. Return ONLY the JSON object, no additional text

Example:
{{
    "domain": "ecommerce",
    "fields": {{
        "customer_name": {{
            "faker_method": "name",
            "parameters": {{}},
            "description": "Customer full name"
        }},
        "email": {{
            "faker_method": "email",
            "parameters": {{}},
            "description": "Customer email address"
        }},
        "order_total": {{
            "faker_method": "pydecimal",
            "parameters": {{"left_digits": 3, "right_digits": 2, "positive": true}},
            "description": "Order total amount"
        }}
    }}
}}"""

        return prompt

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Claude response into schema dictionary.

        Args:
            response_text: Raw response from Claude

        Returns:
            Dict containing parsed schema

        Raises:
            ParsingError: If response cannot be parsed
        """
        try:
            # Clean response text
            cleaned_text = response_text.strip()

            # Remove markdown code blocks if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text.replace("```", "").strip()

            # Parse JSON
            schema_data = json.loads(cleaned_text)

            # Validate required fields
            if not isinstance(schema_data, dict):
                raise ParsingError("Response is not a valid JSON object")

            if "domain" not in schema_data or "fields" not in schema_data:
                raise ParsingError("Response missing required 'domain' or 'fields'")

            if not isinstance(schema_data["fields"], dict):
                raise ParsingError("'fields' must be a dictionary")

            return schema_data

        except json.JSONDecodeError as e:
            raise ParsingError(f"Invalid JSON in Claude response: {str(e)}")
        except Exception as e:
            raise ParsingError(f"Failed to parse Claude response: {str(e)}")

    def _validate_schema(self, schema: Dict[str, Any]) -> bool:
        """
        Validate that the generated schema is well-formed.

        Args:
            schema: Schema dictionary to validate

        Returns:
            bool: True if schema is valid

        Raises:
            ValidationError: If schema is invalid
        """
        required_faker_methods = {
            "name", "first_name", "last_name", "email", "phone_number", "address",
            "city", "country", "date", "date_between", "text", "sentence", "paragraph",
            "random_int", "random_element", "boolean", "pydecimal", "uuid4", "url",
            "company", "job", "ssn", "credit_card_number", "iban"
        }

        for field_name, field_config in schema["fields"].items():
            if not isinstance(field_config, dict):
                raise ValidationError(f"Field '{field_name}' configuration must be a dictionary")

            if "faker_method" not in field_config:
                raise ValidationError(f"Field '{field_name}' missing 'faker_method'")

            faker_method = field_config["faker_method"]
            if faker_method not in required_faker_methods:
                # Allow method but warn it might not work
                continue

            # Validate parameters is a dict
            if "parameters" in field_config and not isinstance(field_config["parameters"], dict):
                raise ValidationError(f"Field '{field_name}' parameters must be a dictionary")

        return True

    def _generate_hash(self, description: str) -> str:
        """Generate SHA-256 hash of description for caching."""
        return generate_cache_key(description)

    async def generate_schema(self, description: str) -> GeneratedSchema:
        """
        Generate a Faker-compatible schema from natural language description.

        Args:
            description: Natural language description of dataset needs

        Returns:
            GeneratedSchema object with generated schema and metadata

        Raises:
            Various exceptions on failure (ValidationError, RateLimitError, etc.)
        """
        # Validate input
        if len(description) < settings.MIN_DESCRIPTION_LENGTH:
            raise ValidationError(f"Description must be at least {settings.MIN_DESCRIPTION_LENGTH} characters")

        if len(description) > settings.MAX_DESCRIPTION_LENGTH:
            raise ValidationError(f"Description must be less than {settings.MAX_DESCRIPTION_LENGTH} characters")

        # Generate description hash for caching
        description_hash = self._generate_hash(description)

        # Check cache first if caching is enabled
        if self.cache:
            try:
                cached_schema = self.cache.get_cached_schema(description_hash)
                if cached_schema:
                    # Cache hit! Return cached schema
                    return cached_schema
            except Exception:
                # Cache error shouldn't block schema generation
                pass

        # Cache miss or caching disabled - proceed with Claude generation
        # Check rate limits
        self._check_rate_limits()

        try:
            # Create prompt
            prompt = self._create_prompt(description)

            # Make Claude API call with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = await self.client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )
                    break

                except Exception as e:
                    if "rate limit" in str(e).lower() or "429" in str(e):
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        else:
                            raise RateLimitError(f"Rate limit exceeded: {str(e)}")
                    elif "timeout" in str(e).lower():
                        raise APIConnectionError(f"Request timeout: {str(e)}")
                    else:
                        raise APIConnectionError(f"Anthropic API error: {str(e)}")

            # Record successful request
            self._record_request()

            # Parse response
            response_text = response.content[0].text
            if not response_text:
                raise SchemaGenerationError("Claude returned empty response")

            schema_data = self._parse_response(response_text)

            # Validate schema
            self._validate_schema(schema_data)

            # Create GeneratedSchema object
            domain = schema_data.get("domain", "unknown")

            generated_schema = GeneratedSchema(
                description_hash=description_hash,
                fields_schema=schema_data["fields"],
                created_at=datetime.now(),
                domain=domain
            )

            # Save to cache if caching is enabled
            if self.cache:
                try:
                    self.cache.save_schema(description_hash, generated_schema)
                except Exception:
                    # Cache save error shouldn't block response
                    pass

            return generated_schema

        except (ValidationError, RateLimitError, APIConnectionError, ParsingError):
            # Re-raise specific exceptions
            raise
        except Exception as e:
            # Never log the API key or sensitive information
            raise SchemaGenerationError(f"Schema generation failed: {str(e)}")
