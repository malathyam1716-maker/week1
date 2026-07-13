# Internship Report

## Abstract

This report describes the `week1` project folder, which contains a Python-based ETL pipeline for integrating external services such as Stripe and Salesforce. The project uses configuration management, Pydantic data validation, and a reusable pipeline architecture to extract, validate, transform, and load data.

## Certificate

Certificate details are not included in the repository. Add the internship certificate information or a scanned copy here when available.

## Acknowledgement

I would like to acknowledge the support of my mentors and team members who helped me understand API integration, Python package structure, and ETL design.

## Table of Contents

1. Abstract
2. Certificate
3. Acknowledgement
4. Introduction
5. Company Profile
6. Overview of the Organization
7. Objectives of the Internship
8. Role and Responsibilities
9. Tools and Technologies Used
10. Project Work / Tasks Performed
11. Methodology / Working Process
12. Implementation Details
13. Results and Output
14. Learning Outcomes
15. Skills Gained
16. Challenges Faced
17. Conclusion
18. Future Scope
19. References / Bibliography

## Introduction

The `week1` folder contains an internship project focused on building data extraction pipelines with Python. The goal is to connect to external APIs, validate the returned data, and implement a basic ETL workflow in a modular project layout.

## Company Profile

This project appears to be part of an internship in a software development or data engineering environment. The repository demonstrates work on data integration services, likely for a company that manages API-driven reporting and analytics.

## Overview of the Organization

The project is organized into several key packages:

- `config/`: application settings and environment-based configuration.
- `integrations/`: service-specific extraction and modeling logic for Stripe, Salesforce, and Zendesk.
- `pipelines/`: pipeline definitions for each service using a shared `BasePipeline` design.
- `utils/`: validation utilities to enforce data model consistency.
- `logs/` and `loaders/`: placeholders for logging and loading components.

## Objectives of the Internship

- Build a reusable ETL pipeline structure.
- Integrate with external APIs using Stripe and Salesforce clients.
- Define data models with Pydantic for robust validation.
- Implement configuration using environment variables.

## Role and Responsibilities

As an intern, the responsibilities included:

- Designing the folder and package structure.
- Implementing extractors for external APIs.
- Defining Pydantic models for Stripe and Salesforce data.
- Building and running pipelines from `main.py`.
- Validating and transforming incoming data.

## Tools and Technologies Used

- Python
- requests
- pydantic
- pydantic-settings
- Stripe SDK (`stripe` package)
- Salesforce REST API via HTTP requests
- Git and `.env` configuration

## Project Work / Tasks Performed

- Created `BasePipeline` in `pipelines/base_pipeline.py`.
- Built Stripe integration in `integrations/stripe/` including extractor and data models.
- Built Salesforce integration in `integrations/salesforce/` including extractor, models, and query definitions.
- Implemented a dummy JSON extractor example in `sample_extarctor.py`.
- Configured application settings in `config/settings.py`.
- Added a validator utility in `utils/validator.py`.
- Created a driver script in `main.py` to run selected pipelines.

## Methodology / Working Process

The project follows an ETL methodology:

1. Extract: Call external APIs to retrieve raw data.
2. Validate: Use Pydantic models to validate and normalize the extracted records.
3. Transform: Pass data through transformation steps (currently identity transform).
4. Load: Print loaded record counts and prepare for downstream loading logic.

## Implementation Details

- `config/settings.py`: Uses `BaseSettings` and `.env` to load API keys and endpoints.
- `pipelines/base_pipeline.py`: Defines abstract `extract`, `transform`, and `load` methods.
- `pipelines/stripe/pipelines.py`: Implements Stripe account and charge pipelines.
- `pipelines/salesforce/pipelines.py`: Implements Salesforce account and billing pipelines.
- `integrations/stripe/extractor.py`: Calls Stripe client services based on `ServiceEnum`.
- `integrations/salesforce/extractor.py`: Handles Salesforce query pagination and API requests.
- `integrations/stripe/models.py` and `integrations/salesforce/models.py`: Define Pydantic models for API responses.
- `sample_extarctor.py`: Demonstrates a simple API extraction loop for dummy JSON data.

## Results and Output

The main driver script `week1/main.py` currently runs the `StripeAccountPipeline`. Expected runtime behavior:

- Extract customer records from Stripe.
- Validate each record against `StripeCustomerModel`.
- Print the number of loaded records.

Salesforce pipelines are available but commented out. The repository prints debug information for validation and extraction progress.

## Learning Outcomes

- Understood how to structure a Python ETL project.
- Learned service-specific extraction patterns for Stripe and Salesforce.
- Applied Pydantic models for data validation and normalization.
- Gained experience with environment-based configuration.

## Skills Gained

- Python package organization
- API integration with `requests` and Stripe SDK
- Data modeling with Pydantic
- ETL pipeline design
- Configuration management with `.env`

## Challenges Faced

- Integrating multiple external API clients in a reusable pipeline.
- Handling API pagination and authentication flows.
- Maintaining consistent data models across services.
- Completing transformers for some service paths (e.g. Zendesk transformer is currently empty).

## Conclusion

The `week1` folder is a solid foundation for a data integration internship project. It demonstrates an ETL pattern with reusable pipelines, validated data models, and a clear separation between configuration, integration, and pipeline logic.

## Future Scope

- Complete Zendesk integration and pipelines.
- Add actual loader implementations to persist data to a database.
- Implement transformation steps beyond identity transforms.
- Add unit tests and error handling for production readiness.
- Improve logging inside `logs/` and loading logic inside `loaders/`.

## References / Bibliography

- Stripe API documentation
- Salesforce REST API documentation
- Pydantic documentation
- Python `requests` library documentation
