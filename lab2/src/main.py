import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import config


def main():
    print("Initializing Lab 2 Pipeline...")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Targeting {len(config.REPOSITORIES)} repositories for multi-mining.")
    # Future steps: loop through repos, run code_miner, run commit_miner, merge.


if __name__ == "__main__":
    main()
