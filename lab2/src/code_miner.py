import os
from pathlib import Path

import config
import pandas as pd


class SourceCodeMiner:
    def __init__(self, repo_path, repo_name):
        self.repo_path = Path(repo_path)
        self.repo_name = repo_name
        self.dataset = []

    def count_loc(self, file_path):
        """Safely counts LOC, ignoring binary or encoding errors."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def mine(self):
        print(f"[{self.repo_name}] Mining source code files...")

        for root, dirs, files in os.walk(self.repo_path):
            # Filter out irrelevant hidden directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".") and d not in ["node_modules", "venv", "env"]
            ]

            for file in files:
                file_path = Path(root) / file
                extension = file_path.suffix.lower()

                # Filter out irrelevant files (docs, configs, binaries)
                if extension not in config.RELEVANT_EXTENSIONS:
                    continue

                relative_path = file_path.relative_to(self.repo_path).as_posix()

                self.dataset.append(
                    {
                        "repo_name": self.repo_name,
                        "file_path": relative_path,
                        "extension": extension,
                        "loc": self.count_loc(file_path),
                        "size_bytes": file_path.stat().st_size,
                    }
                )

        return self.dataset


def append_to_csv(data, output_path):
    """Appends data to CSV, writing headers only if the file is new."""
    df = pd.DataFrame(data)
    if not df.empty:
        file_exists = output_path.is_file()
        df.to_csv(output_path, mode="a", index=False, header=not file_exists)
