import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import config
from code_miner import SourceCodeMiner
from code_miner import append_to_csv as append_code_csv
from commit_miner import CommitHistoryMiner
from commit_miner import append_to_csv as append_commit_csv
from dataset_merger import DatasetMerger


def clone_repository(repo_url, repo_path):
    if not repo_path.exists():
        print(f"Cloning {repo_url} into {repo_path}...")
        subprocess.run(["git", "clone", repo_url, str(repo_path)], check=True)
    else:
        print(f"Repository already exists at {repo_path}. Skipping clone.")


def clear_previous_outputs():
    for file in [
        config.SOURCE_CODE_CSV,
        config.COMMIT_HISTORY_CSV,
        config.MERGED_DATASET_CSV,
    ]:
        if file.exists():
            file.unlink()
            print(f"Cleared previous output: {file.name}")


def main():
    print("Initializing Lab 2 Pipeline...")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    clear_previous_outputs()

    # Now looping through ALL 5 repositories
    for repo_url in config.REPOSITORIES:
        repo_name = repo_url.rstrip("/").split("/")[-1]
        repo_path = config.DATA_DIR / repo_name

        print(f"\n{'=' * 40}")
        print(f"Processing Repository: {repo_name}")
        print(f"{'=' * 40}")

        clone_repository(repo_url, repo_path)

        code_miner = SourceCodeMiner(repo_path, repo_name)
        code_data = code_miner.mine()
        append_code_csv(code_data, config.SOURCE_CODE_CSV)

        commit_miner = CommitHistoryMiner(repo_path, repo_name)
        commit_data = commit_miner.mine()
        append_commit_csv(commit_data, config.COMMIT_HISTORY_CSV)

    print("\nPhase 1 & 2 Complete! Running Phase 3 (Merge)...")
    merger = DatasetMerger()
    merger.merge()
    print("\nLab 2 Pipeline Fully Complete.")


if __name__ == "__main__":
    main()
