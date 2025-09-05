# Goals and Background Context

## Goals
- Enable data science learners to generate custom synthetic datasets through natural language descriptions in under 2 minutes
- Eliminate the technical barrier to synthetic data creation by abstracting schema definition complexity
- Provide 1000+ row CSV datasets that support meaningful ML/data science exercises (train/test splitting, pattern detection)
- Reduce data acquisition time from hours to minutes for learning projects
- Support diverse domain-specific data generation (e-commerce, healthcare, finance, education, social media)
- Minimize API costs through intelligent schema caching while maintaining generation quality

## Background Context

Data science and ML learners currently face a significant bottleneck in their educational journey: acquiring appropriate datasets for their projects. The overreliance on common public datasets (Titanic, Iris) limits portfolio differentiation, while the complexity of existing data generation tools creates unnecessary barriers to learning. This service addresses the gap by combining GPT-4o-mini's natural language understanding with Faker's efficient data generation capabilities, creating a hybrid solution that makes synthetic data as accessible as describing what you need in plain English.

The 1-hour MVP implementation constraint drives a focused approach: a single FastAPI endpoint that processes natural language requests, generates schemas via AI, and produces CSV files with realistic data. By targeting learners specifically, we can optimize for educational value over enterprise features, prioritizing ease of use and domain variety over complex relational structures or authentication systems.

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|---------|
| 2025-09-05 | 1.0 | Initial PRD creation | John (PM) |
