from . import config, exporter
from .file_analyser import RepoAnalyser
from .git_miner import GitHistoryMiner


def main() -> None:
    print(f"Starting repository mining for: {config.REPO_URL}")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("\n--- Phase 1: Repository Inventory ---")
    analyzer = RepoAnalyser(config.REPO_URL, config.DATA_DIR)
    file_data, repo_stats = analyzer.analyze()

    print("\n--- Phase 2: Git History Analysis ---")
    miner = GitHistoryMiner(analyzer.repo_path)
    git_stats = miner.mine()

    print("\n--- Phase 3: Exporting Data ---")
    exporter.export_to_csv(file_data)
    exporter.export_to_json(repo_stats, git_stats)

    print("\nLab 1 Pipeline Complete.")


if __name__ == "__main__":
    main()
