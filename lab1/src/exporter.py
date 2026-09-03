import json
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, TypedDict, cast

import pandas as pd  # pyright: ignore[reportMissingTypeStubs]

from . import config
from .file_analyser import FileData, RepositoryStats
from .git_miner import GitHistoryStats


class _CsvExportable(Protocol):
    def to_csv(self, path: Path, *, index: bool) -> None: ...


class _CombinedStats(TypedDict):
    repository_inventory: RepositoryStats
    git_history_metrics: GitHistoryStats


def export_to_csv(file_data: Sequence[FileData]) -> None:
    """Exports file-level metrics to a CSV dataset."""
    # Set the column order to match the lab manual specification.
    columns = ["file_path", "language", "extension", "loc", "size_bytes"]
    dataframe = cast(
        _CsvExportable,
        cast(object, pd.DataFrame(file_data, columns=columns)),
    )

    dataframe.to_csv(config.CSV_OUTPUT_PATH, index=False)
    print(f"File-level dataset saved to {config.CSV_OUTPUT_PATH}")


def export_to_json(
    repo_stats: RepositoryStats, git_stats: GitHistoryStats
) -> None:
    """Combines repository and git statistics into a single JSON output."""
    combined_stats: _CombinedStats = {
        "repository_inventory": repo_stats,
        "git_history_metrics": git_stats,
    }

    with config.JSON_OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(combined_stats, file, indent=4)
    print(f"Repository statistics saved to {config.JSON_OUTPUT_PATH}")
