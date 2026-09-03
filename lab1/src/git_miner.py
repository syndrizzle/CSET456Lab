from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Protocol, TypedDict, cast

from pydriller import Repository  # pyright: ignore[reportMissingTypeStubs]


class _Author(Protocol):
    name: str


class _ModifiedFile(Protocol):
    new_path: str | None
    added_lines: int
    deleted_lines: int


class _Commit(Protocol):
    author: _Author
    committer_date: datetime
    modified_files: list[_ModifiedFile]


class _RepositoryTraversal(Protocol):
    def traverse_commits(self) -> Iterable[_Commit]: ...


class _MiningStats(TypedDict):
    total_commits: int
    contributors: defaultdict[str, int]
    files_changed_freq: defaultdict[str, int]
    commits_per_month: defaultdict[str, int]
    files_changed_per_month: defaultdict[str, int]
    total_additions: int
    total_deletions: int


class GitHistoryStats(TypedDict):
    total_commits: int
    total_contributors: int
    most_active_contributor: str
    commits_per_month: dict[str, int]
    average_files_changed_per_month: float
    average_file_addition_per_commit: float
    average_file_deletion_per_commit: float
    most_frequently_changed_files: list[tuple[str, int]]


class GitHistoryMiner:
    def __init__(self, repo_path: str | Path) -> None:
        self.repo_path: Path = Path(repo_path)
        self.stats: _MiningStats = {
            "total_commits": 0,
            "contributors": defaultdict(int),
            "files_changed_freq": defaultdict(int),
            "commits_per_month": defaultdict(int),
            "files_changed_per_month": defaultdict(int),
            "total_additions": 0,
            "total_deletions": 0,
        }

    def mine(self) -> GitHistoryStats:
        print("Mining Git history (this may take a few moments)...")
        repository = cast(
            _RepositoryTraversal,
            cast(object, Repository(str(self.repo_path))),
        )

        for commit in repository.traverse_commits():
            self.stats["total_commits"] += 1

            author_name = commit.author.name
            self.stats["contributors"][author_name] += 1

            month_key = commit.committer_date.strftime("%Y-%m")
            self.stats["commits_per_month"][month_key] += 1

            files_modified_count = len(commit.modified_files)
            self.stats["files_changed_per_month"][month_key] += files_modified_count

            for mod_file in commit.modified_files:
                if mod_file.new_path:
                    self.stats["files_changed_freq"][mod_file.new_path] += 1
                self.stats["total_additions"] += mod_file.added_lines
                self.stats["total_deletions"] += mod_file.deleted_lines

        return self._compute_aggregates()

    def _compute_aggregates(self) -> GitHistoryStats:
        """Calculates averages and identifies top contributors/files."""
        total_commits = self.stats["total_commits"] or 1
        total_months = len(self.stats["commits_per_month"]) or 1

        most_active_contributor = (
            max(
                self.stats["contributors"],
                key=self.stats["contributors"].__getitem__,
            )
            if self.stats["contributors"]
            else "None"
        )

        top_files = sorted(
            self.stats["files_changed_freq"].items(), key=lambda x: x[1], reverse=True
        )[:15]

        return {
            "total_commits": self.stats["total_commits"],
            "total_contributors": len(self.stats["contributors"]),
            "most_active_contributor": most_active_contributor,
            "commits_per_month": self.stats["commits_per_month"],
            "average_files_changed_per_month": sum(
                self.stats["files_changed_per_month"].values()
            )
            / total_months,
            "average_file_addition_per_commit": self.stats["total_additions"]
            / total_commits,
            "average_file_deletion_per_commit": self.stats["total_deletions"]
            / total_commits,
            "most_frequently_changed_files": top_files,
        }
