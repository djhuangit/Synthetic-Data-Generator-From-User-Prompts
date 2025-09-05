"""Hash utilities for cache key generation."""

import hashlib
import re


def generate_cache_key(description: str) -> str:
    """
    Generate a consistent SHA-256 hash for cache key from description text.
    
    Handles input sanitization to ensure consistent hashing across requests:
    - Normalizes whitespace (multiple spaces/tabs/newlines to single space)
    - Strips leading/trailing whitespace
    - Converts to lowercase for case-insensitive caching
    - Removes extra punctuation spacing
    
    Args:
        description: Raw description text from user input
        
    Returns:
        str: SHA-256 hash (64-character hexadecimal string)
        
    Example:
        >>> generate_cache_key("  Generate customer DATA   for e-commerce  ")
        'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456'
    """
    if not description:
        raise ValueError("Description cannot be empty for hash generation")
    
    # Normalize the description for consistent hashing
    normalized = _normalize_description(description)
    
    # Generate SHA-256 hash
    hash_object = hashlib.sha256(normalized.encode('utf-8'))
    return hash_object.hexdigest()


def _normalize_description(description: str) -> str:
    """
    Normalize description text for consistent hashing.
    
    Args:
        description: Raw description text
        
    Returns:
        str: Normalized description text
    """
    # Convert to lowercase for case-insensitive comparison
    normalized = description.lower()
    
    # Replace multiple whitespace characters (spaces, tabs, newlines) with single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Strip leading and trailing whitespace
    normalized = normalized.strip()
    
    # Normalize punctuation spacing (remove extra spaces around punctuation)
    normalized = re.sub(r'\s*([,.!?;:])\s*', r'\1 ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)  # Clean up any double spaces
    normalized = normalized.strip()
    
    return normalized


def validate_hash(hash_string: str) -> bool:
    """
    Validate that a string is a proper SHA-256 hash.
    
    Args:
        hash_string: String to validate
        
    Returns:
        bool: True if valid SHA-256 hash format
    """
    if not hash_string:
        return False
    
    # SHA-256 produces 64-character hexadecimal string
    if len(hash_string) != 64:
        return False
    
    # Check if all characters are hexadecimal
    try:
        int(hash_string, 16)
        return True
    except ValueError:
        return False


def hash_matches_description(hash_string: str, description: str) -> bool:
    """
    Verify that a hash matches a given description.
    
    Args:
        hash_string: SHA-256 hash to verify
        description: Description text to check against
        
    Returns:
        bool: True if hash matches description
    """
    try:
        expected_hash = generate_cache_key(description)
        return hash_string == expected_hash
    except (ValueError, TypeError):
        return False