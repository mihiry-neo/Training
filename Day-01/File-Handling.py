from os import path

print("File Exists ",path.exists("demo.txt"))
print("Directory Exists\t",path.exists("Day-01"))

with open("demo.txt", 'w') as file:
    file = file.write("Hello, How are you? I'm Mihir Yadav. Today we are dealing with File Handling.")

print("Does File exists now? ", path.exists("demo.text"))


import os

script_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to script
file_path = os.path.join(script_dir, "demo.txt")

with open(file_path, 'w') as file:
    file.write("Hello, How are you? I'm Mihir Yadav. Today we are dealing with File Handling.")


