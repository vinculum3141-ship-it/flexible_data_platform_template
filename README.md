# Energy Data Platform

A production-ready, cloud-native data platform implementing medallion architecture with clean architecture principles.

## 🏗️ Architecture Overview

This platform follows **Clean Architecture** principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                    API Layer                        │
│              (FastAPI - thin layer)                 │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│               Application Layer                      │
│        (Pipeline, Runner, Metrics)                  │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                 Domain Layer                        │
│    (Business Logic, Transformers, Models)           │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│             Infrastructure Layer                     │
│   (Repositories, Storage, Logging, Settings)        │
└─────────────────────────────────────────────────────┘
```

### Layer Responsibilities

- **Domain Layer**: Pure business logic, transformations, validations (no I/O)
- **Application Layer**: Orchestrates use cases, manages workflows
- **Infrastructure Layer**: External concerns (storage, logging, monitoring)
- **API Layer**: Thin HTTP interface (no business logic)

## 🥇 Medallion Architecture

The platform implements a three-tier medallion architecture:

### Bronze Layer (Raw)
- Ingests raw data from sources
- Minimal transformation
- Preserves original data

### Silver Layer (Cleaned)
- Data cleaning and validation
- Type enforcement
- Deduplication
- Quality checks

### Gold Layer (Business)
- Aggregated metrics
- Business-level transformations
- Analytics-ready data

## 🔧 Execution Modes

### Local Mode (Pandas)
```bash
export EXECUTION_MODE=local
energy-platform run-batch
```
- Uses pandas for data processing
- Stores data in local filesystem/SQLite
- Ideal for development and testing

### Databricks Mode (Spark)
```bash
export EXECUTION_MODE=databricks
export PROCESSING_MODE=batch
energy-platform run-batch
```
- Uses PySpark for distributed processing
- Integrates with Delta Lake
- Production-ready for large datasets

## 🎯 Processing Modes

### Batch Processing
- Processes complete datasets
- Scheduled execution
- Full historical data
- Currently implemented

### Streaming Processing (Scaffolded)
- Real-time data ingestion
- Continuous processing
- Event-driven architecture
- Ready for implementation

## 📊 Metadata Tracking

Each batch execution tracks:
- `batch_id`: Unique identifier
- `source`: Data source identifier
- `ingestion_time`: Processing timestamp
- `record_count`: Number of records processed
- `checksum`: Optional data integrity hash

Metadata enables:
- Lineage tracking
- Quality monitoring
- Debugging and troubleshooting
- Audit trails

## 📈 Monitoring & Metrics

### Pipeline Metrics
```python
PipelineMetrics(
    records_in=1000,
    records_out=950,
    duration_seconds=12.5,
    errors=0
)
```

### Structured Logging
All operations emit structured JSON logs:
```json
{
  "event": "batch_started",
  "batch_id": "20260220_143022",
  "execution_mode": "local",
  "timestamp": "2026-02-20T14:30:22Z"
}
```

### Health Endpoint
```bash
curl http://localhost:8000/health
```

Returns system health status including database connectivity.

## 🚀 Getting Started

### Local Development

1. **Install dependencies**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run batch processing**:
```bash
energy-platform run-batch
```

4. **Start API server**:
```bash
uvicorn app.main:app --reload
```

### Docker Deployment

```bash
# Build and run
docker-compose up -d

# Run batch job
docker-compose exec app energy-platform run-batch

# View logs
docker-compose logs -f app
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_transformers.py
```

## 🏢 Databricks Integration

### Setup
1. Install PySpark dependencies: `pip install -e ".[spark]"`
2. Configure Databricks settings in `.env`
3. Deploy via Databricks Jobs or CLI

### Configuration
```python
EXECUTION_MODE=databricks
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
STORAGE_PATH=/mnt/data
```

### Running on Databricks
```bash
# Via Databricks Job
databricks jobs create --json-file databricks-job.json

# Via CLI
dbfs cp -r app dbfs:/FileStore/energy-platform/
databricks jobs run-now --job-id YOUR_JOB_ID
```

## 📁 Project Structure

```
energy_platform/
├── app/
│   ├── cli.py                    # CLI entrypoint
│   ├── main.py                   # FastAPI app
│   ├── api/                      # API layer
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── dependencies.py
│   ├── domain/                   # Business logic
│   │   ├── models.py
│   │   ├── transformers.py
│   │   └── validation.py
│   ├── application/              # Use case orchestration
│   │   ├── pipeline.py
│   │   ├── runner.py
│   │   └── metrics.py
│   └── infrastructure/           # External concerns
│       ├── settings.py
│       ├── logging.py
│       ├── monitoring.py
│       └── repositories/
│           ├── base.py
│           ├── pandas_repository.py
│           └── spark_repository.py
├── tests/                        # Test suite
├── terraform/                    # Infrastructure as Code
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## 🔮 Future Improvements

### Streaming Implementation
- Kafka/Kinesis integration
- Real-time transformations
- Windowing and aggregations
- Exactly-once semantics

### Data Management
- Partitioning strategies (date, entity)
- Data retention policies
- Compaction and optimization
- Time travel queries

### Reliability
- Idempotency guarantees
- Retry mechanisms
- Dead letter queues
- Circuit breakers

### Observability
- Distributed tracing (OpenTelemetry)
- Metrics dashboards (Grafana)
- Alerting (PagerDuty, Slack)
- Data quality dashboards

### Performance
- Caching layer (Redis)
- Incremental processing
- Query optimization
- Parallel execution

### Security
- Authentication/Authorization (OAuth2)
- Data encryption at rest
- PII masking
- Audit logging

## 🤝 Contributing

1. Follow clean architecture principles
2. Keep transformers pure and stateless
3. No business logic in API or repositories
4. Add tests for new features
5. Use type hints everywhere

## 📝 License

MIT License
