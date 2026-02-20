"""Spark-based repository for Databricks execution."""

from typing import Any

from app.domain.models import BatchMetadata
from app.infrastructure.repositories.base import BaseRepository
from app.infrastructure.settings import Settings


class SparkRepository(BaseRepository):
    """Repository implementation using PySpark for Databricks."""

    def __init__(self, settings: Settings):
        """
        Initialize Spark repository.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._spark = None

    @property
    def spark(self) -> Any:
        """Get or create Spark session."""
        if self._spark is None:
            from pyspark.sql import SparkSession

            builder = SparkSession.builder.appName("EnergyPlatform")

            # Configure for Databricks if credentials provided
            if self.settings.databricks_host and self.settings.databricks_token:
                builder = builder.config("spark.databricks.service.address", self.settings.databricks_host)
                builder = builder.config("spark.databricks.service.token", self.settings.databricks_token)

            self._spark = builder.getOrCreate()

        return self._spark

    def read_bronze(self) -> Any:
        """Read bronze data from Delta Lake."""
        bronze_path = f"{self.settings.bronze_full_path}"
        try:
            return self.spark.read.format("delta").load(bronze_path)
        except Exception:
            # Return empty DataFrame with schema if table doesn't exist
            from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType

            schema = StructType(
                [
                    StructField("timestamp", TimestampType(), True),
                    StructField("entity_id", StringType(), True),
                    StructField("value", DoubleType(), True),
                ]
            )
            return self.spark.createDataFrame([], schema)

    def write_silver(self, df: Any, metadata: BatchMetadata) -> None:
        """Write silver data to Delta Lake."""
        silver_path = f"{self.settings.silver_full_path}"
        df.write.format("delta").mode("append").save(silver_path)

    def read_silver(self) -> Any:
        """Read silver data from Delta Lake."""
        silver_path = f"{self.settings.silver_full_path}"
        try:
            return self.spark.read.format("delta").load(silver_path)
        except Exception:
            # Return empty DataFrame if table doesn't exist
            return self.spark.createDataFrame([], schema="timestamp timestamp, entity_id string, value double")

    def write_gold(self, df: Any, metadata: BatchMetadata) -> None:
        """Write gold data to Delta Lake."""
        gold_path = f"{self.settings.gold_full_path}"
        df.write.format("delta").mode("append").save(gold_path)

    def read_gold(self) -> Any:
        """Read gold data from Delta Lake."""
        gold_path = f"{self.settings.gold_full_path}"
        try:
            return self.spark.read.format("delta").load(gold_path)
        except Exception:
            # Return empty DataFrame if table doesn't exist
            return self.spark.createDataFrame([], schema="entity_id string, date date")

    def save_metadata(self, metadata: BatchMetadata) -> None:
        """Save metadata to Delta Lake metadata table."""
        metadata_path = f"{self.settings.metadata_full_path}"
        
        # Convert metadata to DataFrame
        metadata_df = self.spark.createDataFrame([metadata.to_dict()])
        
        # Write to Delta Lake
        metadata_df.write.format("delta").mode("append").save(metadata_path)

    def health_check(self) -> bool:
        """Check if Spark session is accessible."""
        try:
            # Try to perform a simple operation
            self.spark.range(1).count()
            return True
        except Exception:
            return False
