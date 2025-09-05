"""Data generation service using Faker for realistic synthetic datasets."""

import time
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Callable
from decimal import Decimal

from faker import Faker
from faker.providers import BaseProvider

from src.api.models import GeneratedSchema, SyntheticDataset
from src.core.exceptions import ValidationError


class DataGenerator:
    """Service for generating synthetic datasets using Faker library."""
    
    def __init__(self, locale: str = 'en_US') -> None:
        """
        Initialize DataGenerator with Faker instance and method mappings.
        
        Args:
            locale: Faker locale for data generation (default: en_US)
        """
        self.faker = Faker(locale)
        self.faker.seed_instance(random.randint(1, 100000))  # Ensure variety
        
        # Initialize method mapping for schema to Faker conversion
        self._init_faker_method_mapping()
        
        # Domain-specific value sets for fallback scenarios
        self._init_custom_domain_values()
    
    def _init_faker_method_mapping(self) -> None:
        """Initialize mapping from schema field types to Faker methods."""
        self.faker_methods: Dict[str, Callable] = {
            # Names
            'name': self.faker.name,
            'first_name': self.faker.first_name,
            'last_name': self.faker.last_name,
            'full_name': self.faker.name,
            'username': self.faker.user_name,
            
            # Email and Contact
            'email': self.faker.email,
            'free_email': self.faker.free_email,
            'company_email': self.faker.company_email,
            'phone_number': self.faker.phone_number,
            'phone': self.faker.phone_number,
            
            # Dates
            'date': self.faker.date,
            'past_date': lambda: self.faker.date_between(start_date='-2y', end_date='today'),
            'future_date': lambda: self.faker.date_between(start_date='today', end_date='+2y'),
            'date_between': lambda: self.faker.date_between(start_date='-1y', end_date='+1y'),
            'datetime': self.faker.date_time,
            'time': self.faker.time,
            'birth_date': lambda: self.faker.date_between(start_date='-80y', end_date='-18y'),
            
            # Numbers
            'random_int': lambda: self.faker.random_int(min=1, max=1000),
            'random_number': lambda: self.faker.random_int(min=1, max=10000),
            'float': lambda: round(self.faker.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'pyfloat': lambda: round(self.faker.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'pydecimal': lambda: self.faker.pydecimal(left_digits=3, right_digits=2, positive=True),
            'currency': lambda: f"${self.faker.pydecimal(left_digits=3, right_digits=2, positive=True)}",
            'price': lambda: round(self.faker.pyfloat(min_left_digits=1, max_left_digits=4, right_digits=2, positive=True), 2),
            
            # Addresses
            'address': self.faker.address,
            'street_address': self.faker.street_address,
            'city': self.faker.city,
            'state': self.faker.state,
            'country': self.faker.country,
            'postal_code': self.faker.postcode,
            'zipcode': self.faker.postcode,
            'postcode': self.faker.postcode,
            
            # Text
            'text': lambda: self.faker.text(max_nb_chars=200),
            'sentence': self.faker.sentence,
            'paragraph': lambda: self.faker.paragraph(nb_sentences=3),
            'word': self.faker.word,
            'words': lambda: ' '.join(self.faker.words(nb=random.randint(2, 5))),
            'catch_phrase': self.faker.catch_phrase,
            'bs': self.faker.bs,
            
            # Company/Business
            'company': self.faker.company,
            'job': self.faker.job,
            'company_suffix': self.faker.company_suffix,
            'department': lambda: random.choice(['Sales', 'Marketing', 'Engineering', 'HR', 'Finance', 'Operations']),
            
            # Internet
            'url': self.faker.url,
            'domain_name': self.faker.domain_name,
            'ipv4': self.faker.ipv4,
            'mac_address': self.faker.mac_address,
            
            # Identifiers
            'uuid4': self.faker.uuid4,
            'ssn': self.faker.ssn,
            'ein': self.faker.ein,
            'credit_card_number': self.faker.credit_card_number,
            'iban': self.faker.iban,
            
            # Boolean
            'boolean': self.faker.boolean,
            'pybool': self.faker.pybool,
            
            # Colors
            'color_name': self.faker.color_name,
            'hex_color': self.faker.hex_color,
            'rgb_color': self.faker.rgb_color,
        }
    
    def _init_custom_domain_values(self) -> None:
        """Initialize domain-specific value sets for custom field generation."""
        self.domain_values: Dict[str, Dict[str, List[Any]]] = {
            'ecommerce': {
                'category': ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys'],
                'brand': ['Apple', 'Samsung', 'Nike', 'Adidas', 'Sony', 'Microsoft', 'Amazon'],
                'rating': [1, 2, 3, 4, 5],
                'status': ['Active', 'Inactive', 'Discontinued', 'Coming Soon'],
                'product_type': ['Physical', 'Digital', 'Service', 'Subscription'],
                'shipping_method': ['Standard', 'Express', 'Overnight', 'Free Shipping']
            },
            'healthcare': {
                'blood_type': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                'condition': ['Diabetes', 'Hypertension', 'Asthma', 'Arthritis', 'Heart Disease'],
                'treatment': ['Medication', 'Physical Therapy', 'Surgery', 'Monitoring', 'Lifestyle Change'],
                'insurance': ['Medicare', 'Medicaid', 'Private', 'Uninsured', 'VA Benefits'],
                'department': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Emergency'],
                'priority': ['Low', 'Medium', 'High', 'Critical']
            },
            'finance': {
                'account_type': ['Checking', 'Savings', 'Credit', 'Investment', 'Loan'],
                'transaction_type': ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee'],
                'status': ['Pending', 'Completed', 'Failed', 'Cancelled', 'Processing'],
                'merchant_category': ['Gas Station', 'Grocery Store', 'Restaurant', 'Online Purchase', 'ATM'],
                'currency': ['USD', 'EUR', 'GBP', 'CAD', 'JPY'],
                'risk_level': ['Low', 'Medium', 'High', 'Very High']
            },
            'education': {
                'grade_level': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'],
                'subject': ['Mathematics', 'Science', 'English', 'History', 'Art', 'Physical Education'],
                'degree': ['Bachelor', 'Master', 'PhD', 'Associate', 'Certificate'],
                'major': ['Computer Science', 'Business', 'Engineering', 'Psychology', 'Biology'],
                'semester': ['Fall', 'Spring', 'Summer', 'Winter'],
                'grade': ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
            },
            'general': {
                'gender': ['Male', 'Female', 'Non-binary', 'Prefer not to say'],
                'marital_status': ['Single', 'Married', 'Divorced', 'Widowed', 'Separated'],
                'priority': ['Low', 'Medium', 'High', 'Critical'],
                'status': ['Active', 'Inactive', 'Pending', 'Suspended'],
                'language': ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese'],
                'timezone': ['PST', 'EST', 'CST', 'MST', 'UTC']
            }
        }
    
    def map_schema_to_faker(self, schema: Dict[str, Any]) -> Dict[str, Callable]:
        """
        Map schema fields to appropriate Faker methods or fallback functions.
        
        Args:
            schema: Dictionary mapping field names to field specifications
            
        Returns:
            Dictionary mapping field names to callable generation functions
        """
        field_generators: Dict[str, Callable] = {}
        
        for field_name, field_config in schema.items():
            if isinstance(field_config, dict):
                faker_method = field_config.get('faker_method', 'word')
                parameters = field_config.get('parameters', {})
                
                # Get generator function
                generator_func = self._get_field_generator(field_name, faker_method, parameters)
                field_generators[field_name] = generator_func
            else:
                # Simple string specification
                generator_func = self._get_field_generator(field_name, str(field_config), {})
                field_generators[field_name] = generator_func
        
        return field_generators
    
    def _get_field_generator(self, field_name: str, faker_method: str, parameters: Dict[str, Any]) -> Callable:
        """
        Get appropriate generator function for a field.
        
        Args:
            field_name: Name of the field
            faker_method: Faker method name or fallback strategy
            parameters: Parameters for the method
            
        Returns:
            Callable that generates values for this field
        """
        # Try direct Faker method mapping
        if faker_method in self.faker_methods:
            base_method = self.faker_methods[faker_method]
            
            # Apply parameters if provided
            if parameters:
                return lambda: self._call_with_parameters(base_method, parameters)
            else:
                return base_method
        
        # Try Faker method with parameters
        if hasattr(self.faker, faker_method):
            faker_func = getattr(self.faker, faker_method)
            if parameters:
                return lambda: faker_func(**parameters)
            else:
                return faker_func
        
        # Check for custom domain values
        domain_generator = self._get_domain_generator(field_name, faker_method)
        if domain_generator:
            return domain_generator
        
        # Fallback to generic generation based on field name pattern
        return self._get_fallback_generator(field_name)
    
    def _call_with_parameters(self, method: Callable, parameters: Dict[str, Any]) -> Any:
        """
        Call a method with parameters, handling potential errors gracefully.
        
        Args:
            method: Method to call
            parameters: Parameters to pass
            
        Returns:
            Generated value or fallback
        """
        try:
            return method(**parameters)
        except (TypeError, ValueError):
            # Fallback to method without parameters if parameter application fails
            return method()
    
    def _get_domain_generator(self, field_name: str, domain_hint: str) -> Optional[Callable]:
        """
        Get domain-specific generator based on field name and domain hint.
        
        Args:
            field_name: Field name to analyze
            domain_hint: Domain or method hint
            
        Returns:
            Generator function or None
        """
        # First check if domain hint directly matches a category in any domain
        for domain, categories in self.domain_values.items():
            if domain_hint.lower() in categories:
                values = categories[domain_hint.lower()]
                return lambda vals=values: random.choice(vals)
        
        # Check if the domain hint matches a domain name and field has matching category
        if domain_hint.lower() in self.domain_values:
            domain_categories = self.domain_values[domain_hint.lower()]
            field_lower = field_name.lower()
            
            # Look for field name patterns that match categories in this domain
            for category, values in domain_categories.items():
                category_keywords = category.split('_')
                if (category in field_lower or 
                    any(keyword in field_lower for keyword in category_keywords) or
                    field_lower in category):
                    return lambda vals=values: random.choice(vals)
        
        # General field name pattern matching across all domains
        field_lower = field_name.lower()
        for domain, categories in self.domain_values.items():
            for category, values in categories.items():
                category_keywords = category.split('_')
                if (category in field_lower or 
                    any(keyword in field_lower for keyword in category_keywords) or
                    field_lower == category):
                    return lambda vals=values: random.choice(vals)
        
        return None
    
    def _get_fallback_generator(self, field_name: str) -> Callable:
        """
        Generate fallback function based on field name patterns.
        
        Args:
            field_name: Field name to analyze for patterns
            
        Returns:
            Appropriate generator function
        """
        field_lower = field_name.lower()
        
        # Name patterns
        if any(keyword in field_lower for keyword in ['name', 'full_name', 'customer_name']):
            return self.faker.name
        elif any(keyword in field_lower for keyword in ['first', 'fname', 'given']):
            return self.faker.first_name
        elif any(keyword in field_lower for keyword in ['last', 'lname', 'surname', 'family']):
            return self.faker.last_name
        
        # Email patterns
        elif any(keyword in field_lower for keyword in ['email', 'mail']):
            return self.faker.email
        
        # Phone patterns
        elif any(keyword in field_lower for keyword in ['phone', 'tel', 'mobile']):
            return self.faker.phone_number
        
        # Date patterns
        elif any(keyword in field_lower for keyword in ['date', 'birth', 'created', 'updated']):
            return lambda: self.faker.date_between(start_date='-2y', end_date='today')
        
        # Address patterns
        elif any(keyword in field_lower for keyword in ['address', 'street']):
            return self.faker.address
        elif 'city' in field_lower:
            return self.faker.city
        elif any(keyword in field_lower for keyword in ['state', 'province']):
            return self.faker.state
        elif any(keyword in field_lower for keyword in ['country', 'nation']):
            return self.faker.country
        elif any(keyword in field_lower for keyword in ['zip', 'postal']):
            return self.faker.postcode
        
        # Numeric patterns
        elif any(keyword in field_lower for keyword in ['id', 'number', 'num', 'count']):
            return lambda: self.faker.random_int(min=1, max=100000)
        elif any(keyword in field_lower for keyword in ['price', 'cost', 'amount', 'salary']):
            return lambda: round(self.faker.pyfloat(min_left_digits=1, max_left_digits=4, right_digits=2, positive=True), 2)
        elif any(keyword in field_lower for keyword in ['age', 'year']):
            return lambda: self.faker.random_int(min=18, max=80)
        
        # Text patterns
        elif any(keyword in field_lower for keyword in ['description', 'comment', 'note']):
            return lambda: self.faker.text(max_nb_chars=200)
        elif any(keyword in field_lower for keyword in ['title', 'subject']):
            return self.faker.sentence
        
        # Company patterns
        elif any(keyword in field_lower for keyword in ['company', 'employer', 'organization']):
            return self.faker.company
        elif any(keyword in field_lower for keyword in ['job', 'position', 'role']):
            return self.faker.job
        
        # Boolean patterns
        elif any(keyword in field_lower for keyword in ['active', 'enabled', 'valid', 'is_']):
            return self.faker.boolean
        
        # Default fallback
        else:
            return lambda: self.faker.word()
    
    def generate_data(self, schema: GeneratedSchema, row_count: int = 1000) -> SyntheticDataset:
        """
        Generate synthetic dataset based on schema.
        
        Args:
            schema: GeneratedSchema object containing field specifications
            row_count: Number of rows to generate (1-10000)
            
        Returns:
            SyntheticDataset with generated data
            
        Raises:
            ValidationError: If row_count is invalid
        """
        # Validate row count
        if not isinstance(row_count, int) or row_count < 1 or row_count > 10000:
            raise ValidationError("Row count must be an integer between 1 and 10000")
        
        start_time = time.time()
        
        # Get field generators
        field_generators = self.map_schema_to_faker(schema.fields_schema)
        field_names = list(field_generators.keys())
        
        # Generate data
        data: List[Dict[str, Any]] = []
        
        for row_idx in range(row_count):
            # Add some randomization to prevent obvious patterns
            if row_idx > 0 and row_idx % 100 == 0:
                self.faker.seed_instance(random.randint(1, 100000))
            
            row_data: Dict[str, Any] = {}
            
            for field_name, generator in field_generators.items():
                try:
                    value = generator()
                    
                    # Convert certain types for JSON serialization
                    if isinstance(value, (date, datetime)):
                        row_data[field_name] = value.isoformat()
                    elif isinstance(value, Decimal):
                        row_data[field_name] = float(value)
                    else:
                        row_data[field_name] = value
                        
                except Exception:
                    # Fallback to safe default if generation fails
                    row_data[field_name] = f"sample_{field_name}_{row_idx}"
            
            data.append(row_data)
        
        generation_time = time.time() - start_time
        
        return SyntheticDataset(
            data=data,
            row_count=len(data),
            field_names=field_names,
            generation_time=round(generation_time, 3),
            domain=schema.domain
        )