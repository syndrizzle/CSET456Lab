# Lab 1: Software Repository Mining

**Objective:** Mine a GitHub repository (Flask) to extract files, methods, commits, authors, LOC, and basic repository statistics to produce a machine-readable dataset.

## GenAI Usage Declaration
* **Tool Used:** Gemini
* **Purpose:** Used for initial software architecture design, rapid development of the Python data pipeline, and generating the PyDriller boilerplate.
* **Verification:** The generated code was reviewed, tested, and structurally organized into modular components (`config.py`, `file_analyzer.py`, `git_miner.py`, `exporter.py`) before execution.

## Repository Statistics Summary
* **Target Repository:** https://github.com/pallets/flask[cite: 2]
* **Total Files:** [Insert total_files from JSON]
* **Source Code Files:** [Insert source_code_files from JSON]
* **Total Lines of Code (LOC):** [Insert total_loc from JSON]
* **Programming Languages Identified:** [Insert languages]
* **Total Commits:** [Insert total_commits]
* **Most Active Contributor:** [Insert most_active_contributor]

## How to Run the Project
1. Activate the virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Execute the pipeline: `python src/main.py`
4. Results are generated in the `output/` directory as `file_level_dataset.csv` and `repository_stats.json`[cite: 1, 2].

## Observations & Learnings
* **Repository Architecture:** [Add a 1-2 sentence observation about Flask's file structure or language distribution based on your CSV output]
* **Git History:** [Add a 1-2 sentence observation about the commit frequency or who the primary contributors are]
