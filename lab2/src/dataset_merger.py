import config
import pandas as pd


class DatasetMerger:
    def __init__(self):
        self.code_csv = config.SOURCE_CODE_CSV
        self.commit_csv = config.COMMIT_HISTORY_CSV
        self.merged_csv = config.MERGED_DATASET_CSV

    def merge(self):
        print("\nLoading extracted datasets for merging...")

        try:
            df_code = pd.read_csv(self.code_csv)
            df_commit = pd.read_csv(self.commit_csv)
        except FileNotFoundError as e:
            print(
                f"Error: Missing dataset. Did the miners finish running? Details: {e}"
            )
            return

        print(
            f"Loaded {len(df_code)} source files and {len(df_commit)} commit file records."
        )

        # Aggregate commit history at the file level
        print("Aggregating commit history metrics per file...")
        commit_agg = (
            df_commit.groupby(["repo_name", "file_path"])
            .agg(
                total_commits=("commit_hash", "count"),
                unique_authors=("author_name", "nunique"),
                total_lines_added=("lines_added", "sum"),
                total_lines_deleted=("lines_deleted", "sum"),
            )
            .reset_index()
        )

        # Merge datasets (Inner join drops files that exist in one dataset but not the other)
        print("Merging source code and commit history datasets...")
        df_merged = pd.merge(
            df_code, commit_agg, on=["repo_name", "file_path"], how="inner"
        )

        # Save to output
        df_merged.to_csv(self.merged_csv, index=False)
        print(
            f"Merge complete! Final dataset contains {len(df_merged)} relevant files."
        )
        print(f"Saved to: {self.merged_csv}")


if __name__ == "__main__":
    merger = DatasetMerger()
    merger.merge()
