from pathlib import Path

# Target Repositories for Lab 2
REPOSITORIES = [
    "https://github.com/pallets/flask",
    "https://github.com/psf/requests",
    "https://github.com/pytest-dev/pytest",
    "https://github.com/fastapi/fastapi",
    "https://github.com/scikit-learn/scikit-learn"
]

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Dataset Output Paths
SOURCE_CODE_CSV = OUTPUT_DIR / "source_code_dataset.csv"
COMMIT_HISTORY_CSV = OUTPUT_DIR / "commit_history_dataset.csv"
MERGED_DATASET_CSV = OUTPUT_DIR / "merged_dataset.csv"

# Relevant Extensions (Filtering out irrelevant files)
RELEVANT_EXTENSIONS = {".py", ".c", ".cpp", ".h", ".js", ".java"}
