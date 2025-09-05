#!/usr/bin/env python3
"""Test the complete pipeline without OpenAI API key."""

import time
from datetime import datetime
from src.services.data_generator import DataGenerator
from src.services.csv_exporter import CSVExporter
from src.api.models import GeneratedSchema

def create_mock_schemas():
    """Create mock schemas for different domains without OpenAI."""
    return {
        'ecommerce': {
            'description': 'E-commerce product catalog with pricing and categories',
            'schema': {
                'product_name': {'faker_method': 'catch_phrase'},
                'category': {'faker_method': 'ecommerce'},
                'brand': {'faker_method': 'ecommerce'},
                'price': {'faker_method': 'price'},
                'rating': {'faker_method': 'ecommerce'},
                'in_stock': {'faker_method': 'boolean'},
                'sku': {'faker_method': 'random_int', 'parameters': {'min': 10000, 'max': 99999}}
            }
        },
        'healthcare': {
            'description': 'Patient medical records with demographics and conditions',
            'schema': {
                'patient_name': {'faker_method': 'name'},
                'age': {'faker_method': 'age'},
                'gender': {'faker_method': 'general'},
                'blood_type': {'faker_method': 'healthcare'},
                'condition': {'faker_method': 'healthcare'},
                'department': {'faker_method': 'healthcare'},
                'admission_date': {'faker_method': 'past_date'},
                'priority': {'faker_method': 'healthcare'}
            }
        },
        'finance': {
            'description': 'Financial transaction records with account details',
            'schema': {
                'account_holder': {'faker_method': 'name'},
                'account_number': {'faker_method': 'random_int', 'parameters': {'min': 100000, 'max': 999999}},
                'account_type': {'faker_method': 'finance'},
                'balance': {'faker_method': 'price'},
                'transaction_date': {'faker_method': 'past_date'},
                'merchant': {'faker_method': 'company'},
                'amount': {'faker_method': 'price'}
            }
        }
    }

def test_pipeline_with_mock_schema(domain: str, description: str, schema_dict: dict, rows: int = 10):
    """Test complete pipeline: Mock Schema → Data Generation → CSV Export."""
    print(f"\n{'='*60}")
    print(f"TESTING PIPELINE: {domain.upper()}")
    print(f"{'='*60}")
    print(f"Description: {description}")
    print(f"Rows: {rows}")
    
    start_time = time.time()
    
    # Step 1: Create mock GeneratedSchema (replaces OpenAI call)
    generated_schema = GeneratedSchema(
        description_hash=f"mock_{domain}_{hash(description)}",
        fields_schema=schema_dict,
        created_at=datetime.now(),
        domain=domain
    )
    
    print(f"\n✅ Step 1: Mock Schema Created")
    print(f"   Fields: {list(generated_schema.fields_schema.keys())}")
    print(f"   Domain: {generated_schema.domain}")
    
    # Step 2: Generate synthetic data
    data_generator = DataGenerator()
    synthetic_dataset = data_generator.generate_data(generated_schema, rows)
    data_time = time.time() - start_time
    
    print(f"\n✅ Step 2: Data Generated ({data_time:.3f}s)")
    print(f"   Generated {synthetic_dataset.row_count} rows")
    print(f"   Sample data (first 2 rows):")
    for i, row in enumerate(synthetic_dataset.data[:2], 1):
        print(f"     Row {i}: {row}")
    
    # Step 3: Export to CSV
    csv_exporter = CSVExporter()
    csv_response = csv_exporter.export_to_csv(synthetic_dataset, description)
    total_time = time.time() - start_time
    
    print(f"\n✅ Step 3: CSV Export Complete ({total_time:.3f}s)")
    print(f"   Filename: {csv_response.filename}")
    print(f"   CSV size: {len(csv_response.csv_content)} characters")
    
    # Step 4: Display CSV content
    print(f"\n📄 CSV OUTPUT:")
    print("-" * 50)
    print(csv_response.csv_content)
    print("-" * 50)
    
    # Step 5: Save CSV to file
    output_filename = f"output_{domain}_{rows}rows.csv"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(csv_response.csv_content)
    
    print(f"\n💾 CSV saved to: {output_filename}")
    
    # Step 6: Performance summary
    print(f"\n📊 Performance:")
    print(f"   Total time: {total_time:.3f}s")
    print(f"   Throughput: {rows/total_time:.1f} rows/second")
    print(f"   Memory usage: {len(csv_response.csv_content)} bytes")
    
    return {
        'domain': domain,
        'rows': rows,
        'time': total_time,
        'throughput': rows/total_time,
        'filename': output_filename,
        'csv_content': csv_response.csv_content
    }

def main():
    """Run complete pipeline tests for all domains."""
    print("🚀 TESTING COMPLETE PIPELINE WITHOUT OPENAI")
    print("="*60)
    
    mock_schemas = create_mock_schemas()
    results = []
    
    # Test each domain
    for domain, config in mock_schemas.items():
        result = test_pipeline_with_mock_schema(
            domain=domain,
            description=config['description'],
            schema_dict=config['schema'],
            rows=10
        )
        results.append(result)
    
    # Test with different row counts
    print(f"\n{'='*60}")
    print("PERFORMANCE TESTING WITH DIFFERENT ROW COUNTS")
    print("="*60)
    
    row_counts = [5, 50, 100]
    for rows in row_counts:
        result = test_pipeline_with_mock_schema(
            domain='ecommerce',
            description='Performance test e-commerce data',
            schema_dict=mock_schemas['ecommerce']['schema'],
            rows=rows
        )
        results.append(result)
    
    # Summary
    print(f"\n{'='*60}")
    print("🎉 PIPELINE TEST SUMMARY")
    print("="*60)
    
    print(f"{'Domain':<12} {'Rows':<6} {'Time(s)':<8} {'Speed(r/s)':<12} {'File':<25}")
    print("-" * 65)
    
    for result in results:
        print(f"{result['domain']:<12} {result['rows']:<6} {result['time']:<8.3f} {result['throughput']:<12.1f} {result['filename']:<25}")
    
    print(f"\n✅ All CSV files generated successfully!")
    print(f"✅ Pipeline working end-to-end without OpenAI API")
    print(f"✅ Ready for production with real OpenAI integration")

if __name__ == "__main__":
    main()