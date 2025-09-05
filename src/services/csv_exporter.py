"""CSV export service for converting synthetic datasets to CSV format."""

import re
import time
from datetime import datetime
from typing import Dict, Any, Optional
from io import StringIO

import pandas as pd

from src.api.models import SyntheticDataset, DatasetResponse
from src.core.exceptions import ValidationError


class CSVExporter:
    """Service for exporting synthetic datasets to CSV format."""
    
    def __init__(self) -> None:
        """Initialize CSVExporter with default configurations."""
        self.csv_options = {
            'index': False,  # Don't include row indices
            'encoding': 'utf-8',  # Unicode support
            'quoting': 1,  # Quote all fields (csv.QUOTE_ALL equivalent)
            'lineterminator': '\n'  # Cross-platform line endings
        }
    
    def export_to_csv(self, dataset: SyntheticDataset, description: str = "") -> DatasetResponse:
        """
        Convert SyntheticDataset to CSV format.
        
        Args:
            dataset: Generated synthetic dataset to export
            description: Original description for filename generation
            
        Returns:
            DatasetResponse with CSV content and metadata
            
        Raises:
            ValidationError: If dataset conversion fails
        """
        try:
            # Convert dataset to pandas DataFrame
            df = self._create_dataframe(dataset)
            
            # Generate CSV content
            csv_content = self._dataframe_to_csv(df)
            
            # Generate filename
            filename = self.generate_filename(description, dataset.domain)
            
            return DatasetResponse(
                csv_content=csv_content,
                filename=filename,
                row_count=dataset.row_count,
                content_type="text/csv"
            )
            
        except Exception as e:
            raise ValidationError(f"Failed to export dataset to CSV: {str(e)}")
    
    def _create_dataframe(self, dataset: SyntheticDataset) -> pd.DataFrame:
        """
        Create pandas DataFrame from SyntheticDataset.
        
        Args:
            dataset: Synthetic dataset to convert
            
        Returns:
            Pandas DataFrame with proper column ordering
            
        Raises:
            ValidationError: If DataFrame creation fails
        """
        try:
            # Validate dataset structure
            if not dataset.data:
                raise ValidationError("Dataset contains no data records")
            
            if not dataset.field_names:
                raise ValidationError("Dataset contains no field names")
            
            # Create DataFrame from data records
            df = pd.DataFrame(dataset.data)
            
            # Ensure column ordering matches field_names
            if set(df.columns) != set(dataset.field_names):
                missing_cols = set(dataset.field_names) - set(df.columns)
                extra_cols = set(df.columns) - set(dataset.field_names)
                
                error_msg = []
                if missing_cols:
                    error_msg.append(f"Missing columns: {missing_cols}")
                if extra_cols:
                    error_msg.append(f"Extra columns: {extra_cols}")
                
                raise ValidationError(f"Column mismatch: {'; '.join(error_msg)}")
            
            # Reorder columns to match field_names order
            df = df[dataset.field_names]
            
            # Validate row count
            if len(df) != dataset.row_count:
                raise ValidationError(f"Row count mismatch: DataFrame has {len(df)} rows, expected {dataset.row_count}")
            
            return df
            
        except pd.errors.EmptyDataError:
            raise ValidationError("Cannot create DataFrame from empty dataset")
        except pd.errors.ParserError as e:
            raise ValidationError(f"DataFrame parsing error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"DataFrame creation failed: {str(e)}")
    
    def _dataframe_to_csv(self, df: pd.DataFrame) -> str:
        """
        Convert pandas DataFrame to CSV string.
        
        Args:
            df: DataFrame to convert
            
        Returns:
            CSV content as string
            
        Raises:
            ValidationError: If CSV conversion fails
        """
        try:
            # Use StringIO to capture CSV output
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, **self.csv_options)
            
            # Get CSV content and clean up
            csv_content = csv_buffer.getvalue()
            csv_buffer.close()
            
            # Validate CSV content
            if not csv_content.strip():
                raise ValidationError("Generated CSV content is empty")
            
            return csv_content
            
        except Exception as e:
            raise ValidationError(f"CSV conversion failed: {str(e)}")
    
    def generate_filename(self, description: str, domain: str = "") -> str:
        """
        Generate descriptive filename from description text.
        
        Args:
            description: Natural language description
            domain: Domain category for prefix
            
        Returns:
            Sanitized filename with .csv extension
        """
        # Start with description or fallback
        base_name = description.strip() if description else "synthetic_dataset"
        
        # Add domain prefix if available
        if domain and domain.lower() != "general":
            base_name = f"{domain}_{base_name}"
        
        # Clean and sanitize filename
        filename = self._sanitize_filename(base_name)
        
        # Ensure reasonable length (max 100 characters before extension)
        if len(filename) > 100:
            filename = filename[:100]
        
        # Add timestamp if filename is generic
        if filename in ["dataset", "data", "synthetic_dataset"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}"
        
        # Add .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        return filename
    
    def _sanitize_filename(self, text: str) -> str:
        """
        Sanitize text for use as filename.
        
        Args:
            text: Input text to sanitize
            
        Returns:
            Sanitized filename string
        """
        # Convert to lowercase
        filename = text.lower()
        
        # Replace common words and phrases
        filename = re.sub(r'\b(generate|create|dataset|data|for|the|a|an|with|and|or)\b', '', filename)
        
        # Replace whitespace and special characters with underscores
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        
        # Replace multiple underscores with single underscore
        filename = re.sub(r'_{2,}', '_', filename)
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        # Ensure we have something meaningful
        if not filename or len(filename) < 3:
            filename = "synthetic_dataset"
        
        return filename
    
    def get_csv_headers(self, dataset_response: DatasetResponse) -> Dict[str, str]:
        """
        Generate HTTP headers for CSV response.
        
        Args:
            dataset_response: DatasetResponse with CSV content
            
        Returns:
            Dictionary of HTTP headers for CSV download
        """
        return {
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": f'attachment; filename="{dataset_response.filename}"',
            "X-Row-Count": str(dataset_response.row_count),
            "X-Content-Length": str(len(dataset_response.csv_content.encode('utf-8')))
        }
    
    def validate_csv_compatibility(self, csv_content: str) -> bool:
        """
        Validate CSV content can be read by common tools.
        
        Args:
            csv_content: CSV content to validate
            
        Returns:
            True if CSV is valid and compatible
        """
        try:
            # Test with pandas read_csv
            test_df = pd.read_csv(StringIO(csv_content))
            
            # Basic validation
            if test_df.empty:
                return False
            
            if len(test_df.columns) == 0:
                return False
            
            return True
            
        except Exception:
            return False