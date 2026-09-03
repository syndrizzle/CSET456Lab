import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from . import config
from .file_analyser import RepoAnalyser


def main():
    print(f"Starting repository mining for: {config.REPO_URL}")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("\n--- Phase 1: Repository Inventory ---")
    analyzer = RepoAnalyser(config.REPO_URL, config.DATA_DIR)
    _file_data, repo_stats = analyzer.analyze()

    print(f"Analysis complete for {repo_stats['repository_name']}.")
    print(f"Total Files: {repo_stats['total_files']}")
    print(f"Total LOC: {repo_stats['total_loc']}")
    print(f"Languages found: {', '.join(repo_stats['programming_languages'])}")


if __name__ == "__main__":
    main()
