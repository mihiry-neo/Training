import os

EXCLUDED_FOLDERS = {"spark_home"}
PARTIAL_LIMITS = {
    "airflow_logs": 5,   # Show only first 5 items
    "data_lake": 5       # Show only first 5 items
}
visited_paths = set()


def is_excluded(path):
    """Check if path is under an excluded folder like spark_home."""
    return any(folder in path.split(os.sep) for folder in EXCLUDED_FOLDERS)


def get_partial_limit(folder_name):
    """Return limit if folder has partial display rules."""
    return PARTIAL_LIMITS.get(folder_name, None)


def display_tree(path, prefix="", max_depth=None, current_depth=0, output_file=None):
    """
    Display folder structure as a tree and write unique paths to a file.
    Includes limited items from airflow_logs and data_lake.
    Skips everything under spark_home.
    """
    if max_depth is not None and current_depth > max_depth:
        return

    # Skip entire folder if under spark_home
    if is_excluded(path):
        return

    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        print(f"{prefix}[Permission Denied]")
        return

    folder_name = os.path.basename(path)
    limit = get_partial_limit(folder_name)
    if limit is not None:
        items = items[:limit]  # Trim items if limit set

    for i, item in enumerate(items):
        item_path = os.path.join(path, item)
        is_last = (i == len(items) - 1)

        # Avoid printing items under spark_home
        if is_excluded(item_path):
            continue

        current_prefix = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        # Print tree
        print(f"{prefix}{current_prefix}{item}/" if os.path.isdir(item_path) else f"{prefix}{current_prefix}{item}")

        # Write to file (only unique paths)
        abs_path = os.path.abspath(item_path)
        if output_file and abs_path not in visited_paths:
            visited_paths.add(abs_path)
            output_file.write(f"{abs_path}\n")

        # Recurse if directory and not a symlink
        if os.path.isdir(item_path) and not os.path.islink(item_path):
            display_tree(item_path, next_prefix, max_depth, current_depth + 1, output_file)


# === Main ===
if __name__ == "__main__":
    folder_path = "."  # Set your target folder here
    output_file_path = "all_paths.txt"

    print(f"Folder tree for: {os.path.abspath(folder_path)}")
    print("=" * 60)

    with open(output_file_path, "w", encoding="utf-8") as f:
        display_tree(folder_path, max_depth=None, output_file=f)

    print(f"\nUnique filtered paths saved to: {output_file_path}")
