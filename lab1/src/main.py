import sys
from pathlib import Path

from . import config

sys.path.append(str(Path(__file__).resolve().parent))


def main():
    print(f"Starting repository mining for: {config.REPO_URL}")
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Directories initialized successfully.")


if __name__ == "__main__":
    main()
