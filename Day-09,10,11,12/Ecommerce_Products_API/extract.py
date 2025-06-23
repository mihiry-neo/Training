import os

# Change this to the directory you want to scan
ROOT_DIR = "C:\\Users\\user\\Documents\\GitHub\\Training\\Day-09,10,11,12\\Ecommerce_Products_API"

# Output file name
OUTPUT_FILE = "all_python_code.txt"

# Whether to include subdirectories
RECURSIVE = True

all_code = []

for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    all_code.append(f"# --- File: {file_path} ---\n{code}\n")
            except Exception as e:
                print(f"❌ Failed to read {file_path}: {e}")
    
    if not RECURSIVE:
        break  # Prevent going into subdirectories

# Write to a single .txt file
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("\n\n".join(all_code))

print(f"✅ All Python code has been written to: {OUTPUT_FILE}")
