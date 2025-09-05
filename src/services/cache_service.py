"""Schema caching service for persistent storage of generated schemas."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import asdict

from src.core.config import settings
from src.core.exceptions import CacheError
from src.api.models import GeneratedSchema
from src.utils.file_operations import (
    read_json_file,
    write_json_file,
    ensure_file_exists,
    get_file_size
)
from src.utils.hash_utils import validate_hash


class SchemaCache:
    """File-based cache for generated schemas with atomic operations."""
    
    def __init__(self) -> None:
        """Initialize the schema cache with file paths."""
        self.cache_file = Path(settings.CACHE_FILE_PATH)
        self.backup_file = Path(settings.CACHE_BACKUP_PATH)
        
        # Ensure data directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize cache file if it doesn't exist
        self._initialize_cache()
    
    def _initialize_cache(self) -> None:
        """Initialize the cache file with empty structure if it doesn't exist."""
        default_cache = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "schemas": {},
            "metadata": {
                "total_schemas": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
        
        try:
            ensure_file_exists(self.cache_file, default_cache)
        except OSError as e:
            raise CacheError(f"Failed to initialize cache file: {str(e)}")
    
    def get_cached_schema(self, description_hash: str) -> Optional[GeneratedSchema]:
        """
        Retrieve a cached schema by description hash.
        
        Args:
            description_hash: SHA-256 hash of the description
            
        Returns:
            GeneratedSchema object if found, None otherwise
            
        Raises:
            CacheError: If cache file cannot be read or parsed
        """
        if not validate_hash(description_hash):
            raise ValueError(f"Invalid hash format: {description_hash}")
        
        try:
            cache_data = read_json_file(self.cache_file)
            schemas = cache_data.get("schemas", {})
            
            if description_hash not in schemas:
                return None
            
            schema_data = schemas[description_hash]
            
            # Convert back to GeneratedSchema object
            return GeneratedSchema(
                description_hash=schema_data["description_hash"],
                fields_schema=schema_data["fields_schema"],
                created_at=datetime.fromisoformat(schema_data["created_at"]),
                domain=schema_data["domain"]
            )
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Try to recover from backup if main cache is corrupted
            return self._recover_from_backup(description_hash)
        except (KeyError, ValueError, TypeError) as e:
            raise CacheError(f"Invalid cache data format: {str(e)}")
        except OSError as e:
            raise CacheError(f"Failed to read cache file: {str(e)}")
    
    def save_schema(self, description_hash: str, schema: GeneratedSchema) -> bool:
        """
        Save a schema to the cache.
        
        Args:
            description_hash: SHA-256 hash of the description
            schema: GeneratedSchema object to cache
            
        Returns:
            bool: True if successfully saved
            
        Raises:
            CacheError: If cache cannot be updated
        """
        if not validate_hash(description_hash):
            raise ValueError(f"Invalid hash format: {description_hash}")
        
        try:
            # Read current cache data
            cache_data = read_json_file(self.cache_file)
            
            # Add new schema
            cache_data["schemas"][description_hash] = {
                "description_hash": schema.description_hash,
                "fields_schema": schema.fields_schema,
                "created_at": schema.created_at.isoformat(),
                "domain": schema.domain
            }
            
            # Update metadata
            cache_data["metadata"]["total_schemas"] = len(cache_data["schemas"])
            cache_data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Write updated cache
            write_json_file(self.cache_file, cache_data, create_backup=True)
            return True
            
        except (FileNotFoundError, json.JSONDecodeError):
            # If cache is corrupted, recreate it
            return self._recreate_cache_with_schema(description_hash, schema)
        except OSError as e:
            raise CacheError(f"Failed to save to cache: {str(e)}")
    
    def clear_cache(self) -> bool:
        """
        Clear all cached schemas.
        
        Returns:
            bool: True if cache was cleared successfully
        """
        try:
            self._initialize_cache()
            return True
        except OSError:
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics and metadata.
        
        Returns:
            dict: Cache statistics including total schemas, file size, etc.
        """
        try:
            cache_data = read_json_file(self.cache_file)
            
            return {
                "total_schemas": cache_data.get("metadata", {}).get("total_schemas", 0),
                "last_updated": cache_data.get("metadata", {}).get("last_updated"),
                "cache_file_size": get_file_size(self.cache_file),
                "backup_file_size": get_file_size(self.backup_file),
                "cache_file_path": str(self.cache_file),
                "backup_file_path": str(self.backup_file)
            }
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {
                "total_schemas": 0,
                "last_updated": None,
                "cache_file_size": 0,
                "backup_file_size": 0,
                "cache_file_path": str(self.cache_file),
                "backup_file_path": str(self.backup_file),
                "error": "Cache file not accessible"
            }
    
    def list_cached_hashes(self) -> List[str]:
        """
        Get list of all cached schema hashes.
        
        Returns:
            list: List of description hashes in the cache
        """
        try:
            cache_data = read_json_file(self.cache_file)
            return list(cache_data.get("schemas", {}).keys())
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []
    
    def _recover_from_backup(self, description_hash: str) -> Optional[GeneratedSchema]:
        """
        Attempt to recover a schema from backup cache file.
        
        Args:
            description_hash: Hash of the schema to recover
            
        Returns:
            GeneratedSchema object if found in backup, None otherwise
        """
        try:
            if not self.backup_file.exists():
                return None
            
            backup_data = read_json_file(self.backup_file)
            schemas = backup_data.get("schemas", {})
            
            if description_hash not in schemas:
                return None
            
            schema_data = schemas[description_hash]
            
            return GeneratedSchema(
                description_hash=schema_data["description_hash"],
                fields_schema=schema_data["fields_schema"],
                created_at=datetime.fromisoformat(schema_data["created_at"]),
                domain=schema_data["domain"]
            )
            
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return None
    
    def _recreate_cache_with_schema(self, description_hash: str, schema: GeneratedSchema) -> bool:
        """
        Recreate cache file with a single schema (recovery method).
        
        Args:
            description_hash: Hash of the schema
            schema: GeneratedSchema object
            
        Returns:
            bool: True if cache was recreated successfully
        """
        try:
            new_cache = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "schemas": {
                    description_hash: {
                        "description_hash": schema.description_hash,
                        "fields_schema": schema.fields_schema,
                        "created_at": schema.created_at.isoformat(),
                        "domain": schema.domain
                    }
                },
                "metadata": {
                    "total_schemas": 1,
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            write_json_file(self.cache_file, new_cache, create_backup=False)
            return True
            
        except OSError:
            return False
    
    def is_cache_healthy(self) -> bool:
        """
        Check if cache is accessible and has valid structure.
        
        Returns:
            bool: True if cache is healthy
        """
        try:
            cache_data = read_json_file(self.cache_file)
            
            # Check required keys
            required_keys = ["version", "schemas", "metadata"]
            if not all(key in cache_data for key in required_keys):
                return False
            
            # Check metadata structure
            metadata = cache_data.get("metadata", {})
            if "total_schemas" not in metadata or "last_updated" not in metadata:
                return False
            
            # Validate schema count
            actual_count = len(cache_data.get("schemas", {}))
            reported_count = metadata.get("total_schemas", 0)
            
            return actual_count == reported_count
            
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return False