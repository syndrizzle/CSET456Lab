# Lab 2: Multi-Repository Mining and Dataset Preparation

**Objective:** Mine five open-source repositories to extract source code and commit history, clean the data, and combine them into a single relevant dataset for downstream analysis.

## Dataset Statistics (Outputs)
* **Dataset 1 (Source Code):** Extracted `[Insert Row Count]` source files across 5 repositories, filtering out binaries, documentation, and configuration files.
* **Dataset 2 (Commit History):** Extracted `[Insert Row Count]` file-level modifications, specifically ignoring merge commits to prevent duplicate churn counting.
* **Dataset 3 (Merged):** The resulting dataset contains `[Insert Row Count]` strictly relevant source code files joined with their evolutionary git metrics.

## Problem Analysis: Potential Uses for this Dataset
By combining static code metrics (LOC, size, language) with evolutionary metrics (total commits, authors, code churn), this dataset can be used to solve several SE/AI domain problems:
1. **Defect Prediction / Bug-Proneness:** Files with high code churn (lots of additions/deletions), multiple distinct authors, and high LOC are historically more prone to bugs. This dataset could train a machine learning classifier to flag risky files.
2. **Code Maintainability Analysis:** Identifying legacy files that are excessively large (high LOC) but rarely touched (low commit count) versus hot-spots that require constant maintenance.
3. **Developer Effort Estimation:** Evaluating how many distinct contributors are required to maintain source files of different languages or sizes.

## GenAI Usage Declaration
* **Tool Used:** Gemini
* **Purpose:** Used for data modeling (determining which features to keep/drop), writing the pandas aggregation/merge logic, and sequential pipeline structuring.
