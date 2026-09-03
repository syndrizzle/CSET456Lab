from pathlib import Path

REPO_URL = "https://github.com/pallets/flask"

# Paths for this repo
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Outputs
CSV_OUTPUT_PATH = OUTPUT_DIR / "file_level_dataset.csv"
JSON_OUTPUT_PATH = OUTPUT_DIR / "repository_stats.json"

# File Extensions
LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".html": "HTML",
    ".css": "CSS",
    ".md": "Markdown",
    ".rst": "ReStructuredText",
    ".yml": "YAML",
    ".bat": "Batch",
    ".yaml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".sh": "Shell",
    ".c": "C",
    ".h": "C Header",
}
