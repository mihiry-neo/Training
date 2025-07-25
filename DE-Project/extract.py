import os

# Define extensions to include
included_extensions = ['.py', '.yml', '.yaml', '.sql', '.sh', '.posthog']
special_files = ['dockerfile']  # case-insensitive match
excluded_dirs = {'project_venv', '__pycache__', '.git', 'node_modules', '.idea','extract.py','all_paths.txt','path.py','airflow_logs'}

output_file = 'project_code_dump_mi.txt'
base_dir = '.'  # starting directory

with open(output_file, 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(base_dir):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()

            # Check if file matches included extensions or is a special name (e.g., Dockerfile)
            if (
                any(file_lower.endswith(ext) for ext in included_extensions) or
                file_lower in special_files
            ):
                out.write(f"\n{'='*80}\n")
                out.write(f"File: {file_path}\n")
                out.write(f"{'='*80}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        out.write(f.read())
                except Exception as e:
                    out.write(f"Could not read file {file_path}: {e}")
                out.write('\n\n')

print(f"✅ Code exported to: {output_file}")
