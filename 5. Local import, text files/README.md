## Simple Accounting System / Warehouse with a Text Database
### Exercise:
In this exercise, you'll extend the functionality of the company account and warehouse operations program from the previous lesson. You'll implement saving and loading of account balance, warehouse inventory, and operation history to/from a text file.

1. **You can store balance, inventory and history in separate files or in one file.**

2. **At the start of the program, if the file(s) exists, load the data from the file and use it to initialize the program state.**
  - If the file does not exist or if there are any errors during file reading (e.g., the file is corrupted or not readable), handle these cases gracefully.
  - Make sure to save all the data to correct files when the program is being shutdown.

#### Hints:
- Use built-in Python functions for file I/O and converting data to Python objects (i.e. literal_eval).
- Remember to handle any file I/O errors that may occur.
- Think about the format in which you'll save the data to the file. The format should be easy to read back into the program.
- Always close the files after you're done with them to free up system resources.
