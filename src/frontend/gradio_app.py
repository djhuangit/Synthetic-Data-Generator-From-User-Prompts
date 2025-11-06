"""
Gradio frontend for the Synthetic Data Generator.
This module provides a user-friendly web interface for generating synthetic datasets.
"""

import gradio as gr
import pandas as pd
from io import StringIO
from typing import Tuple, Optional
import time
from datetime import datetime

from src.services.data_generator import DataGenerator
from src.services.csv_exporter import CSVExporter
from src.core.exceptions import (
    SchemaGenerationError,
    RateLimitError,
    APIConnectionError,
    ValidationError
)


class GradioInterface:
    """Gradio interface for synthetic data generation."""

    def __init__(self):
        """Initialize the Gradio interface with service instances."""
        self.schema_generator = None
        self.data_generator = None
        self.csv_exporter = None

    def _initialize_services(self):
        """Lazily initialize services when needed."""
        from src.core.config import settings

        if self.schema_generator is None:
            # Use mock or real generator based on DEMO_MODE and API_PROVIDER
            if settings.DEMO_MODE:
                from src.services.mock_schema_generator import MockSchemaGenerator
                self.schema_generator = MockSchemaGenerator()
            elif settings.API_PROVIDER == "anthropic":
                from src.services.anthropic_schema_generator import AnthropicSchemaGenerator
                self.schema_generator = AnthropicSchemaGenerator()
            else:  # default to openai
                from src.services.schema_generator import SchemaGenerator
                self.schema_generator = SchemaGenerator()

        if self.data_generator is None:
            self.data_generator = DataGenerator()
        if self.csv_exporter is None:
            self.csv_exporter = CSVExporter()

    async def generate_dataset(
        self,
        description: str,
        num_rows: int,
        progress=gr.Progress()
    ) -> Tuple[Optional[str], Optional[str], str]:
        """
        Generate synthetic dataset based on user input.

        Args:
            description: Natural language description of the dataset
            num_rows: Number of rows to generate
            progress: Gradio progress tracker

        Returns:
            Tuple of (csv_preview, csv_download_path, status_message)
        """
        start_time = time.time()

        # Validate inputs
        if not description or len(description.strip()) < 10:
            return None, None, "❌ Error: Description must be at least 10 characters long."

        if num_rows < 1 or num_rows > 10000:
            return None, None, "❌ Error: Number of rows must be between 1 and 10,000."

        try:
            # Initialize services
            self._initialize_services()

            # Step 1: Generate schema
            progress(0.2, desc="Generating schema with AI...")
            generated_schema = await self.schema_generator.generate_schema(description)

            # Step 2: Generate data
            progress(0.5, desc="Generating synthetic data...")
            synthetic_dataset = self.data_generator.generate_data(generated_schema, num_rows)

            # Step 3: Export to CSV
            progress(0.8, desc="Exporting to CSV...")
            csv_response = self.csv_exporter.export_to_csv(synthetic_dataset, description)

            # Calculate metrics
            total_time = time.time() - start_time
            rows_per_second = num_rows / total_time if total_time > 0 else 0

            # Create preview (first 100 rows)
            csv_data = StringIO(csv_response.csv_content)
            df = pd.read_csv(csv_data)
            preview_df = df.head(100) if len(df) > 100 else df

            # Create success message
            status_msg = (
                f"✅ Successfully generated {num_rows:,} rows in {total_time:.2f}s\n"
                f"📊 Domain: {generated_schema.domain}\n"
                f"⚡ Performance: {rows_per_second:,.0f} rows/second\n"
                f"📁 Fields: {', '.join(synthetic_dataset.field_names)}\n"
                f"⏰ Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            progress(1.0, desc="Complete!")

            # Return preview as HTML table and CSV content for download
            return preview_df.to_html(index=False, max_rows=100), csv_response.csv_content, status_msg

        except ValidationError as e:
            return None, None, f"❌ Validation Error: {str(e)}"

        except RateLimitError as e:
            return None, None, f"⏸️ Rate Limit Error: {str(e)}\nPlease wait a moment and try again."

        except APIConnectionError as e:
            return None, None, f"🔌 API Connection Error: {str(e)}\nPlease check your internet connection and API key."

        except SchemaGenerationError as e:
            return None, None, f"⚠️ Schema Generation Error: {str(e)}"

        except ValueError as e:
            if "OPENAI_API_KEY" in str(e):
                return None, None, "❌ Configuration Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
            else:
                return None, None, f"❌ Configuration Error: {str(e)}"

        except Exception as e:
            return None, None, f"❌ Unexpected Error: {str(e)}\nPlease try again or contact support."


def create_gradio_interface() -> gr.Blocks:
    """
    Create and configure the Gradio interface.

    Returns:
        Configured Gradio Blocks interface
    """
    interface = GradioInterface()

    # Define example prompts
    examples = [
        ["E-commerce product catalog with product names, categories, prices, ratings, and stock status", 100],
        ["Healthcare patient records with names, ages, blood types, medical conditions, and departments", 50],
        ["Financial transactions with account holders, account numbers, transaction amounts, dates, and merchants", 200],
        ["Employee database with names, job titles, departments, salaries, hire dates, and email addresses", 150],
        ["Social media user profiles with usernames, bio, follower count, posts, and registration dates", 75],
    ]

    with gr.Blocks(
        title="Synthetic Data Generator",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        gr.Markdown(
            """
            # 🎲 Synthetic Data Generator

            Generate realistic synthetic datasets from natural language descriptions using AI and Faker library.

            ### How it works:
            1. **Describe** your dataset needs in plain English
            2. **Specify** how many rows you want (1-10,000)
            3. **Generate** high-quality synthetic data instantly
            4. **Download** your dataset as a CSV file

            ---
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                description_input = gr.Textbox(
                    label="Dataset Description",
                    placeholder="Describe the dataset you want to generate (e.g., 'E-commerce orders with customer names, products, prices, and dates')",
                    lines=4,
                    info="Minimum 10 characters, maximum 4000 characters"
                )

                num_rows_input = gr.Slider(
                    minimum=1,
                    maximum=10000,
                    value=100,
                    step=1,
                    label="Number of Rows",
                    info="More rows = longer generation time"
                )

                generate_btn = gr.Button("🚀 Generate Dataset", variant="primary", size="lg")

            with gr.Column(scale=1):
                gr.Markdown(
                    """
                    ### 💡 Tips:
                    - Be specific about field names and types
                    - Mention the domain (e.g., healthcare, finance)
                    - Include desired data characteristics
                    - Start with fewer rows to test

                    ### ⚡ Performance:
                    - **Small** (1-100 rows): < 1 second
                    - **Medium** (100-1000 rows): 1-3 seconds
                    - **Large** (1000-10000 rows): 3-30 seconds
                    """
                )

        status_output = gr.Textbox(
            label="Status",
            lines=5,
            interactive=False,
            show_label=True
        )

        gr.Markdown("### 📊 Data Preview (first 100 rows)")

        preview_output = gr.HTML(label="Preview")

        csv_download = gr.File(
            label="📥 Download Complete Dataset (CSV)",
            visible=True
        )

        # Example datasets
        gr.Markdown("### 📝 Example Prompts")
        gr.Examples(
            examples=examples,
            inputs=[description_input, num_rows_input],
            label="Click an example to load it"
        )

        # Add footer
        gr.Markdown(
            """
            ---

            **Powered by:** Claude Sonnet 4.5 • Faker Library • FastAPI • Gradio

            **Note:** This service generates *synthetic* (fake) data for testing and development purposes only.
            """
        )

        # Event handler
        async def generate_and_update(description: str, num_rows: int, progress=gr.Progress()):
            """Handle generate button click with progress tracking."""
            preview, csv_content, status = await interface.generate_dataset(description, num_rows, progress)

            # Create temporary file for download if generation was successful
            if csv_content:
                # Create filename from description
                filename = description[:50].replace(' ', '_').replace(',', '').replace('.', '')
                filename = f"synthetic_data_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                # Save to temporary file for Gradio download
                temp_path = f"/tmp/{filename}"
                with open(temp_path, 'w') as f:
                    f.write(csv_content)

                return preview, status, temp_path
            else:
                return preview, status, None

        generate_btn.click(
            fn=generate_and_update,
            inputs=[description_input, num_rows_input],
            outputs=[preview_output, status_output, csv_download],
            api_name="generate"
        )

    return demo


# Create the Gradio app instance
app = create_gradio_interface()

if __name__ == "__main__":
    # Launch the Gradio app standalone
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
