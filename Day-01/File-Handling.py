from os import path
import os
import csv

print("File Exists ",path.exists("demo.txt"))
print("Directory Exists\t",path.exists("Day-01"))

script_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to script
file_path = os.path.join(script_dir, "demo.txt")

with open(file_path, 'w+') as file:
    file.write("Hello, How are you? I'm Mihir Yadav. Today we are dealing with File Handling.")
    file.seek(0)
    fread = file.read()
    print(fread)
    file.tell()
    file.write("Let's start with it. There are multiple modes while reading and writing file such as 'w','r','a','w+','r+' and many more.")
    file.seek(0)
    fread2 = file.read()
    print(fread2)


print("File exists", path.exists("demo.csv"))
print("Directory exist", path.exists("Day-01"))

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path2 = os.path.join(script_dir,'demo.csv')

with open(file_path2, "w+", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name','Message'])
    writer.writerow(['Mihir','This is a csv file being written using CSV.writer in file handling'])

with open(file_path2,'r') as file:
    read = csv.reader(file)
    for row in read:
        print(row)

with open(file_path2, 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['This is going to be a long day','This has been a long day'])
    file.seek(0)
    print("Reading the updated csv")
    read = csv.reader(file)
    for row in read:
        print(row)
    
