import os
import subprocess
from pathlib import Path
from typing import TypedDict

from . import config


class FileData(TypedDict):
    file_path: str
    language: str
    extension: str
    loc: int
    size_bytes: int


class RepositoryStats(TypedDict):
    repository_name: str
    total_files: int
    source_code_files: int
    total_directories: int
    total_loc: int
    programming_languages: list[str]
    file_type_distribution: dict[str, int]


class RepoAnalyser:
    def __init__(self, repo_url: str, data_dir: str | Path) -> None:
        self.repo_url: str = repo_url
        self.repo_name: str = repo_url.rstrip("/").split("/")[-1]
        self.repo_path: Path = Path(data_dir) / self.repo_name
        self.file_data: list[FileData] = []
        self._programming_languages: set[str] = set()
        self.repo_stats: RepositoryStats = {
            "repository_name": self.repo_name,
            "total_files": 0,
            "source_code_files": 0,
            "total_directories": 0,
            "total_loc": 0,
            "programming_languages": [],
            "file_type_distribution": {},
        }

    def clone_repo(self) -> None:
        """Clones the repository if it doesn't already exist."""
        if not self.repo_path.exists():
            print(f"Cloning {self.repo_url} into {self.repo_path}...")
            _ = subprocess.run(
                ["git", "clone", self.repo_url, str(self.repo_path)], check=True
            )
        else:
            print(f"Repository already exists at {self.repo_path}. Skipping clone.")

    def count_loc(self, file_path: Path) -> int:
        """Safely counts the lines of code in a file."""
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as file:
                return sum(1 for _ in file)
        except OSError:
            return 0

    def analyze(self) -> tuple[list[FileData], RepositoryStats]:
        """Traverses the repository to gather file-level and repo-level metrics."""
        self.clone_repo()

        for root, dirs, files in os.walk(self.repo_path):
            # Ignore hidden directories like .git
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            self.repo_stats["total_directories"] += len(dirs)

            for file in files:
                if file.startswith("."):
                    continue

                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.repo_path)
                extension = file_path.suffix.lower()

                # File metrics
                size_bytes = file_path.stat().st_size
                loc = self.count_loc(file_path)
                language = config.LANGUAGE_MAP.get(extension, "Unknown")

                # Update repository-level statistics
                self.repo_stats["total_files"] += 1
                self.repo_stats["total_loc"] += loc
                self.repo_stats["file_type_distribution"][extension] = (
                    self.repo_stats["file_type_distribution"].get(extension, 0) + 1
                )

                is_source_code = language != "Unknown"
                if is_source_code:
                    self.repo_stats["source_code_files"] += 1
                    self._programming_languages.add(language)

                # Store file-level data for the CSV output
                self.file_data.append(
                    {
                        "file_path": str(relative_path),
                        "language": language,
                        "extension": extension,
                        "loc": loc,
                        "size_bytes": size_bytes,
                    }
                )

        # Convert set to list for JSON serialization later
        self.repo_stats["programming_languages"] = list(
            self._programming_languages
        )
        return self.file_data, self.repo_stats
