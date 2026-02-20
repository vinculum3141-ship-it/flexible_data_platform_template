"""Pandas-based repository for local execution."""

import json
from pathlib import Path
from typing import Any

import pandas as pd

from app.domain.models import BatchMetadata
from app.infrastructure.repositories.base import BaseRepository
from app.infrastructure.settings import Settings


class PandasRepository(BaseRepository):
    """Repository implementation using pandas for local storage."""

    def __init__(self, settings: Settings):
        """
        Initialize pandas repository.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create storage directories if they don't exist."""
        Path(self.settings.bronze_full_path).mkdir(parents=True, exist_ok=True)
        Path(self.settings.silver_full_path).mkdir(parents=True, exist_ok=True)
        Path(self.settings.gold_full_path).mkdir(parents=True, exist_ok=True)
        Path(self.settings.metadata_full_path).mkdir(parents=True, exist_ok=True)

    def read_bronze(self) -> pd.DataFrame:
        """Read bronze data from parquet files."""
        bronze_path = Path(self.settings.bronze_full_path)
        parquet_files = list(bronze_path.glob("*.parquet"))

        if not parquet_files:
            # Return empty DataFrame with expected schema if no files exist
            return pd.DataFrame(columns=["timestamp", "entity_id", "value"])

        # Read all parquet files and concatenate
        dfs = [pd.read_parquet(f) for f in parquet_files]
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    def write_silver(self, df: pd.DataFrame, metadata: BatchMetadata) -> None:
        """Write silver data to parquet."""
        output_path = Path(self.settings.silver_full_path) / f"{metadata.batch_id}.parquet"
        df.to_parquet(output_path, index=False)

    def read_silver(self) -> pd.DataFrame:
        """Read silver data from parquet files."""
        silver_path = Path(self.settings.silver_full_path)
        parquet_files = list(silver_path.glob("*.parquet"))

        if not parquet_files:
            return pd.DataFrame()

        dfs = [pd.read_parquet(f) for f in parquet_files]
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    def write_gold(self, df: pd.DataFrame, metadata: BatchMetadata) -> None:
        """Write gold data to parquet."""
        output_path = Path(self.settings.gold_full_path) / f"{metadata.batch_id}.parquet"
        df.to_parquet(output_path, index=False)

    def read_gold(self) -> pd.DataFrame:
        """Read gold data from parquet files."""
        gold_path = Path(self.settings.gold_full_path)
        parquet_files = list(gold_path.glob("*.parquet"))

        if not parquet_files:
            return pd.DataFrame()

        dfs = [pd.read_parquet(f) for f in parquet_files]
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    def save_metadata(self, metadata: BatchMetadata) -> None:
        """Save metadata to JSON file."""
        metadata_path = (
            Path(self.settings.metadata_full_path) / f"{metadata.batch_id}_metadata.json"
        )
        with open(metadata_path, "w") as f:
            json.dump(metadata.to_dict(), f, indent=2)

    def health_check(self) -> bool:
        """Check if storage is accessible."""
        try:
            self._ensure_directories()
            # Try to write and read a test file
            test_path = Path(self.settings.storage_path) / ".health_check"
            test_path.write_text("ok")
            content = test_path.read_text()
            test_path.unlink()
            return content == "ok"
        except Exception:
            return False
