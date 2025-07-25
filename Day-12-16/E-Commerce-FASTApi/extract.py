import os

def extract_project_files(project_dir, output_file):
    allowed_extensions = {'.py', '.yml'}
    allowed_filenames = {'Dockerfile', 'docker-compose.yml'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(project_dir):
            for file in files:
                file_ext = os.path.splitext(file)[1]
                if file_ext in allowed_extensions or file in allowed_filenames:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_dir)
                    outfile.write(f"\n\n### FILE: {rel_path} ###\n\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"# Could not read {rel_path}: {e}\n")

# Usage
project_directory = '.'  # Or full path to your ecommerce_api folder
output_txt = 'ecommerce_project_code.txt'
extract_project_files(project_directory, output_txt)
print(f"✅ All code and configs extracted to {output_txt}")
