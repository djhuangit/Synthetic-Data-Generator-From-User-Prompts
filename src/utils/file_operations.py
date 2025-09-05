"""File I/O utilities with proper locking for thread-safe operations."""

import json
import fcntl
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any, Optional, Generator, Union
from datetime import datetime


@contextmanager
def file_lock(file_path: Union[str, Path], mode: str = 'r') -> Generator:
    """
    Context manager for file operations with exclusive locking.
    
    Ensures atomic file operations to prevent corruption during concurrent access.
    Uses fcntl.flock for cross-process locking on Unix-like systems.
    
    Args:
        file_path: Path to the file to lock
        mode: File open mode ('r', 'w', 'a', etc.)
        
    Yields:
        file: Opened file object with exclusive lock
        
    Example:
        with file_lock('/path/to/file.json', 'w') as f:
            json.dump(data, f)
    """
    file_path = Path(file_path)
    
    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Open file with specified mode
    file_obj = open(file_path, mode, encoding='utf-8')
    
    try:
        # Acquire exclusive lock (blocks until available)
        fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)
        yield file_obj
    finally:
        # Release lock and close file
        fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)
        file_obj.close()


def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read JSON data from file with proper locking and error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        dict: Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
        PermissionError: If file cannot be accessed
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with file_lock(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e.msg}", e.doc, e.pos)


def write_json_file(file_path: Union[str, Path], data: Dict[str, Any], create_backup: bool = True) -> bool:
    """
    Write JSON data to file with proper locking and backup creation.
    
    Args:
        file_path: Path to JSON file
        data: Dictionary data to write
        create_backup: Whether to create a backup before writing
        
    Returns:
        bool: True if write was successful
        
    Raises:
        PermissionError: If file cannot be written
        OSError: If file system operation fails
    """
    file_path = Path(file_path)
    backup_path = file_path.with_suffix(f'{file_path.suffix}.backup')
    
    try:
        # Create backup if requested and file exists
        if create_backup and file_path.exists():
            shutil.copy2(file_path, backup_path)
        
        # Write new data with atomic operation
        with file_lock(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=_json_serializer, ensure_ascii=False)
            f.flush()  # Ensure data is written to disk
            os.fsync(f.fileno())  # Force OS to write to physical storage
        
        return True
        
    except (OSError, PermissionError) as e:
        # If backup exists and write failed, attempt to restore it
        if create_backup and backup_path.exists():
            try:
                shutil.copy2(backup_path, file_path)
            except (OSError, PermissionError):
                pass  # Best effort restore
        raise e


def ensure_file_exists(file_path: Union[str, Path], default_content: Optional[Dict[str, Any]] = None) -> bool:
    """
    Ensure a JSON file exists, creating it with default content if needed.
    
    Args:
        file_path: Path to JSON file
        default_content: Default content to write if file doesn't exist
        
    Returns:
        bool: True if file exists or was created successfully
    """
    file_path = Path(file_path)
    
    if file_path.exists():
        return True
    
    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use empty dict if no default content provided
    if default_content is None:
        default_content = {}
    
    try:
        write_json_file(file_path, default_content, create_backup=False)
        return True
    except (OSError, PermissionError):
        return False


def _json_serializer(obj: Any) -> str:
    """
    Custom JSON serializer for datetime and other non-JSON types.
    
    Args:
        obj: Object to serialize
        
    Returns:
        str: JSON-serializable representation
        
    Raises:
        TypeError: If object type is not supported
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        # Handle custom objects by converting to dict
        return obj.__dict__
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        int: File size in bytes, 0 if file doesn't exist
    """
    file_path = Path(file_path)
    
    try:
        return file_path.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def safe_delete_file(file_path: Union[str, Path]) -> bool:
    """
    Safely delete a file if it exists.
    
    Args:
        file_path: Path to file to delete
        
    Returns:
        bool: True if file was deleted or didn't exist
    """
    file_path = Path(file_path)
    
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except (OSError, PermissionError):
        return False