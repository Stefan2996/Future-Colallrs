In this exercise, you will extend the previous CSV file modification program to also handle JSON and Pickle files. The program, "reader.py", will modify a CSV, JSON, or Pickle file, display its contents in the terminal, and then save it to a selected location. Make sure to use classes and inheritance in this program.

Instructions:

1. Write a program named "reader.py". This program will take in command-line arguments that specify the source file, destination file, and changes to be made.

2. The source (src) should be a path to a CSV, JSON, or Pickle file. If the file does not exist or the path is not a file, the program should display an error message and list the files in the same directory.

3. The destination (dst) should be the target path where the modified file will be saved.

4. The changes are strings in the form "X, Y, value", where X is the column (also counted from 0), Y is the row to be modified (counted from 0), and value is the new value for the specified cell.

5. The file type for both the source and destination files should be detected based on their extensions:
   - .csv for CSV files
   - .json for JSON files
   - .pickle for Pickle files

6. In the case of pickle and json, files are saved as lists of lists. Each row is a list of strings, and rows are stored in the list.

Example command for running the program:

python reader.py source.csv destination.json "0,0,piano" "1,1,mug"

Hints:

- Use Python's built-in csv, json, and pickle modules to handle reading and writing of files.
- Use Python's os module to handle file paths and to check if a file exists.
- Use Python's sys module to handle command-line arguments.