"""Runner layer - execution management with metadata and metrics."""

import time
from datetime import datetime
from typing import Any

from app.application.metrics import PipelineMetrics
from app.application.pipeline import Pipeline
from app.domain.models import BatchMetadata
from app.infrastructure.logging import get_logger
from app.infrastructure.repositories.base import BaseRepository

logger = get_logger(__name__)


class BatchRunner:
    """Manages batch processing execution."""

    def __init__(self, pipeline: Pipeline, repository: BaseRepository, source: str = "default"):
        """
        Initialize batch runner.

        Args:
            pipeline: Pipeline instance
            repository: Data repository
            source: Data source identifier
        """
        self.pipeline = pipeline
        self.repository = repository
        self.source = source

    def run(self) -> PipelineMetrics:
        """
        Execute batch processing with metadata tracking.

        Returns:
            Pipeline execution metrics
        """
        # Generate batch ID
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(
            "batch_started",
            batch_id=batch_id,
            source=self.source,
        )

        start_time = time.time()
        errors = 0

        try:
            # Read bronze data count
            bronze_df = self.repository.read_bronze()
            if hasattr(bronze_df, "__len__"):  # pandas
                records_in = len(bronze_df)
            else:  # Spark
                records_in = bronze_df.count()

            logger.info("bronze_loaded", batch_id=batch_id, record_count=records_in)

            # Run pipeline
            silver_df, gold_df, silver_count, gold_count = self.pipeline.run_batch()

            # Create and save silver metadata
            silver_metadata = BatchMetadata(
                batch_id=batch_id,
                source=self.source,
                ingestion_time=datetime.now(),
                record_count=silver_count,
                layer="silver",
            )

            # Write silver data
            self.repository.write_silver(silver_df, silver_metadata)
            self.repository.save_metadata(silver_metadata)
            
            logger.info(
                "silver_written",
                batch_id=batch_id,
                record_count=silver_count,
            )

            # Create and save gold metadata
            gold_metadata = BatchMetadata(
                batch_id=batch_id,
                source=self.source,
                ingestion_time=datetime.now(),
                record_count=gold_count,
                layer="gold",
            )

            # Write gold data
            self.repository.write_gold(gold_df, gold_metadata)
            self.repository.save_metadata(gold_metadata)
            
            logger.info(
                "gold_written",
                batch_id=batch_id,
                record_count=gold_count,
            )

            records_out = gold_count

        except Exception as e:
            logger.error(
                "batch_failed",
                batch_id=batch_id,
                error=str(e),
                exc_info=True,
            )
            errors = 1
            records_in = 0
            records_out = 0

        # Calculate duration
        duration_seconds = time.time() - start_time

        # Create metrics
        metrics = PipelineMetrics(
            records_in=records_in,
            records_out=records_out,
            duration_seconds=duration_seconds,
            errors=errors,
        )

        logger.info(
            "batch_completed",
            batch_id=batch_id,
            metrics=metrics.to_dict(),
        )

        return metrics


class StreamingRunner:
    """Manages streaming processing execution (scaffold only)."""

    def __init__(self, pipeline: Pipeline, repository: BaseRepository, source: str = "default"):
        """
        Initialize streaming runner.

        Args:
            pipeline: Pipeline instance
            repository: Data repository
            source: Data source identifier
        """
        self.pipeline = pipeline
        self.repository = repository
        self.source = source

    def run(self) -> None:
        """
        Execute streaming processing (placeholder).

        This is a scaffold for future streaming implementation.
        Would integrate with Kafka, Kinesis, or Spark Structured Streaming.
        """
        logger.info(
            "streaming_started",
            source=self.source,
        )

        # Placeholder for streaming logic
        # In a real implementation, this would:
        # 1. Connect to streaming source (Kafka, Kinesis, etc.)
        # 2. Read micro-batches or individual records
        # 3. Apply transformations
        # 4. Write to silver/gold layers
        # 5. Handle checkpointing and exactly-once semantics

        raise NotImplementedError(
            "Streaming processing is scaffolded but not fully implemented. "
            "Extend this class to integrate with your streaming platform."
        )
