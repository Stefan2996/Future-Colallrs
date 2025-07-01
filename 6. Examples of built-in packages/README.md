## Program for Editing .CSV Files
### Exercise:
In this exercise, you're tasked to create a Python script called 'reader.py' that modifies a CSV file based on user-provided changes, displays its content in the terminal, and saves the modified file to a provided destination.

1. **The script should be run as `reader.py <src> <dst> <change1> <change2> ...`. 'src' is the path of the CSV file to be modified.**
    - If the file does not exist or the path specified is not a file, display an error message and the filenames in the same directory.

2. **'dst' is the target path where the modified CSV file will be saved.**

3. **'change1' ... 'changeN' are strings of the form "X,Y,value". 'X' is the column (also counting from 0), 'Y' is the row to modify (counting from 0), and 'value' is the new value for the given cell.**

4. **After applying all changes, the script should display the content of the modified CSV file in the terminal and save it to the destination path.**

#### Example:
If the script is run as follows: 

*python reader.py in.csv out.csv 0,0,piano 3,1,mug 1,2,17 3,3,0*

And the 'in.csv' file content is: 

door,3,7,0<br>
sand,12,5,1<br>
brush,22,34,5<br>
poster,red,8,stick<br>

The following 'out.csv' file should be generated:

piano,3,7,0<br>
sand,12,5,mug<br>
brush,17,34,5<br>
poster,red,8,0<br>

### Hints:
- Remember how to handle command-line arguments in a Python script.
- Use the built-in csv module to read from and write to CSV files.
- Be mindful of the zero-based indexing of rows and columns.
- Make sure to handle errors that might occur during file I/O operations.
- For easier testing, use extension for your IDE that displays CSV files in human-readable form (if you’re using Visual Studio Code, you can install Edit csv or CSV to Table extension)

### Additional Challenge (Optional):
Enhance your script to handle invalid 'change' arguments gracefully. If a 'change' argument does not have the correct format or if the specified row or column does not exist in the CSV file, display a helpful error message and skip that change.
