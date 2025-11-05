"""
Mock schema generator for demo/test mode.
This allows testing the full stack without an OpenAI API key.
"""

from datetime import datetime
from typing import Dict, Any
from src.api.models import GeneratedSchema
from src.utils.hash_utils import generate_cache_key


class MockSchemaGenerator:
    """Generates mock schemas based on keywords in the description."""

    def __init__(self):
        """Initialize mock schema generator with predefined templates."""
        self.templates = {
            "ecommerce": {
                "domain": "ecommerce",
                "schema": {
                    "product_name": {"faker_method": "catch_phrase"},
                    "category": {"faker_method": "word"},
                    "brand": {"faker_method": "company"},
                    "price": {"faker_method": "pydecimal", "min_value": 10, "max_value": 1000, "right_digits": 2},
                    "rating": {"faker_method": "random_int", "min": 1, "max": 5},
                    "in_stock": {"faker_method": "boolean"},
                    "sku": {"faker_method": "bothify", "text": "###-???-###"},
                }
            },
            "healthcare": {
                "domain": "healthcare",
                "schema": {
                    "patient_name": {"faker_method": "name"},
                    "age": {"faker_method": "random_int", "min": 1, "max": 100},
                    "gender": {"faker_method": "random_element", "elements": ["Male", "Female", "Other"]},
                    "blood_type": {"faker_method": "random_element", "elements": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},
                    "condition": {"faker_method": "random_element", "elements": ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Arthritis"]},
                    "department": {"faker_method": "random_element", "elements": ["Emergency", "Surgery", "Pediatrics", "Cardiology", "Neurology"]},
                }
            },
            "finance": {
                "domain": "finance",
                "schema": {
                    "account_holder": {"faker_method": "name"},
                    "account_number": {"faker_method": "bban"},
                    "account_type": {"faker_method": "random_element", "elements": ["Checking", "Savings", "Credit", "Loan"]},
                    "balance": {"faker_method": "pydecimal", "min_value": 100, "max_value": 100000, "right_digits": 2},
                    "transaction_date": {"faker_method": "date_this_year"},
                    "merchant": {"faker_method": "company"},
                }
            },
            "employee": {
                "domain": "business",
                "schema": {
                    "employee_name": {"faker_method": "name"},
                    "job_title": {"faker_method": "job"},
                    "department": {"faker_method": "random_element", "elements": ["Engineering", "Sales", "Marketing", "HR", "Finance"]},
                    "salary": {"faker_method": "random_int", "min": 40000, "max": 200000},
                    "hire_date": {"faker_method": "date_between", "start_date": "-10y", "end_date": "today"},
                    "email": {"faker_method": "company_email"},
                }
            },
            "social": {
                "domain": "social_media",
                "schema": {
                    "username": {"faker_method": "user_name"},
                    "bio": {"faker_method": "sentence"},
                    "followers": {"faker_method": "random_int", "min": 0, "max": 1000000},
                    "posts": {"faker_method": "random_int", "min": 0, "max": 10000},
                    "registration_date": {"faker_method": "date_between", "start_date": "-5y", "end_date": "today"},
                    "verified": {"faker_method": "boolean", "chance_of_getting_true": 20},
                }
            },
            "education": {
                "domain": "education",
                "schema": {
                    "student_name": {"faker_method": "name"},
                    "student_id": {"faker_method": "bothify", "text": "STU-####"},
                    "grade": {"faker_method": "random_int", "min": 1, "max": 12},
                    "gpa": {"faker_method": "pydecimal", "min_value": 0, "max_value": 4, "right_digits": 2},
                    "major": {"faker_method": "random_element", "elements": ["Computer Science", "Mathematics", "Physics", "Biology", "Literature"]},
                    "enrollment_date": {"faker_method": "date_this_decade"},
                }
            },
            "default": {
                "domain": "general",
                "schema": {
                    "id": {"faker_method": "uuid4"},
                    "name": {"faker_method": "name"},
                    "email": {"faker_method": "email"},
                    "phone": {"faker_method": "phone_number"},
                    "address": {"faker_method": "address"},
                    "created_at": {"faker_method": "date_time_this_year"},
                }
            }
        }

    async def generate_schema(self, description: str) -> GeneratedSchema:
        """
        Generate a mock schema based on keywords in the description.

        Args:
            description: Natural language description of the dataset

        Returns:
            GeneratedSchema with mock data
        """
        description_lower = description.lower()

        # Determine domain based on keywords
        template_key = "default"
        if any(word in description_lower for word in ["ecommerce", "product", "shop", "store", "catalog"]):
            template_key = "ecommerce"
        elif any(word in description_lower for word in ["healthcare", "patient", "medical", "hospital", "health"]):
            template_key = "healthcare"
        elif any(word in description_lower for word in ["finance", "account", "bank", "transaction", "payment"]):
            template_key = "finance"
        elif any(word in description_lower for word in ["employee", "staff", "worker", "job", "salary"]):
            template_key = "employee"
        elif any(word in description_lower for word in ["social", "user", "profile", "follower", "post"]):
            template_key = "social"
        elif any(word in description_lower for word in ["student", "education", "school", "grade", "university"]):
            template_key = "education"

        template = self.templates[template_key]

        # Create GeneratedSchema
        return GeneratedSchema(
            description_hash=generate_cache_key(description),
            fields_schema=template["schema"],
            created_at=datetime.now(),
            domain=template["domain"]
        )
