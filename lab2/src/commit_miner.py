from pathlib import Path

import config
import pandas as pd
from pydriller import Repository


class CommitHistoryMiner:
    def __init__(self, repo_path, repo_name):
        self.repo_path = str(repo_path)
        self.repo_name = repo_name
        self.dataset = []

    def mine(self):
        print(f"[{self.repo_name}] Mining commit history (this will take a moment)...")

        # Traverse commits using PyDriller
        for commit in Repository(self.repo_path).traverse_commits():
            # Skip merge commits to avoid double-counting churn metrics
            if commit.merge:
                continue

            for mod_file in commit.modified_files:
                # Use new_path for added/modified files, old_path for deleted
                file_path = mod_file.new_path or mod_file.old_path
                if not file_path:
                    continue

                # Filter out irrelevant files (docs, configs, binaries)
                extension = Path(file_path).suffix.lower()
                if extension not in config.RELEVANT_EXTENSIONS:
                    continue

                # Normalize path to match source code miner output
                posix_path = Path(file_path).as_posix()

                self.dataset.append(
                    {
                        "repo_name": self.repo_name,
                        "commit_hash": commit.hash,
                        "author_name": commit.author.name,
                        "committer_date": commit.committer_date.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "file_path": posix_path,
                        "lines_added": mod_file.added_lines,
                        "lines_deleted": mod_file.deleted_lines,
                    }
                )

        return self.dataset


def append_to_csv(data, output_path):
    """Appends dataset to CSV, writing headers only if the file is newly created."""
    df = pd.DataFrame(data)
    if not df.empty:
        file_exists = output_path.is_file()
        df.to_csv(output_path, mode="a", index=False, header=not file_exists)
