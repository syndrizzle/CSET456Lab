import subprocess
import sys
from pathlib import Path

# Add src to system path
sys.path.append(str(Path(__file__).resolve().parent))

import config
from code_miner import SourceCodeMiner
from code_miner import append_to_csv as append_code_csv
from commit_miner import CommitHistoryMiner
from commit_miner import append_to_csv as append_commit_csv


def clone_repository(repo_url, repo_path):
    """Clones the repository locally if it doesn't exist."""
    if not repo_path.exists():
        print(f"Cloning {repo_url} into {repo_path}...")
        subprocess.run(["git", "clone", repo_url, str(repo_path)], check=True)
    else:
        print(f"Repository already exists at {repo_path}. Skipping clone.")


def clear_previous_outputs():
    """Removes old CSV files so we don't append to outdated data during re-runs."""
    for file in [config.SOURCE_CODE_CSV, config.COMMIT_HISTORY_CSV]:
        if file.exists():
            file.unlink()
            print(f"Cleared previous output: {file.name}")


def main():
    print("Initializing Lab 2 Pipeline...")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Clear old files for a fresh test run
    clear_previous_outputs()

    # For quick testing, we can slice the list to just test the first repository (Flask)
    # Change `config.REPOSITORIES[:1]` to `config.REPOSITORIES` when you are ready to run all 5.
    test_repos = config.REPOSITORIES[:1]

    print(f"Targeting {len(test_repos)} repository(ies) for sequential mining.")

    for repo_url in test_repos:
        repo_name = repo_url.rstrip("/").split("/")[-1]
        repo_path = config.DATA_DIR / repo_name

        print(f"\n{'=' * 40}")
        print(f"Processing Repository: {repo_name}")
        print(f"{'=' * 40}")

        # Step 1: Clone
        clone_repository(repo_url, repo_path)

        # Step 2: Mine Source Code
        code_miner = SourceCodeMiner(repo_path, repo_name)
        code_data = code_miner.mine()
        append_code_csv(code_data, config.SOURCE_CODE_CSV)
        print(f"Extracted {len(code_data)} source files.")

        # Step 3: Mine Commit History
        commit_miner = CommitHistoryMiner(repo_path, repo_name)
        commit_data = commit_miner.mine()
        append_commit_csv(commit_data, config.COMMIT_HISTORY_CSV)
        print(f"Extracted {len(commit_data)} commit file records.")

    print(
        "\nPipeline Phase 1 & 2 Complete! Source and Commit CSVs generated in lab2/output/."
    )


if __name__ == "__main__":
    main()
