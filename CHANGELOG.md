# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-20

### Added
- Clean architecture codebase with API, application, domain, and infrastructure layers.
- Medallion pipeline (bronze, silver, gold) with batch orchestration and metrics.
- Local pandas and Databricks/PySpark repositories and transformers.
- FastAPI endpoints (health, metrics, gold data) with dependency injection.
- Typer CLI commands for batch/stream runs, health checks, and sample data generation.
- Structured logging, monitoring hooks, and configuration via Pydantic settings.
- Test suite for transformers, pipeline integration, and API endpoints.
- Dockerfile and docker-compose stack for local deployment.
- Terraform scaffold for cloud infrastructure.
- Documentation set including README, Quickstart, Architecture, Deployment, and Features.
