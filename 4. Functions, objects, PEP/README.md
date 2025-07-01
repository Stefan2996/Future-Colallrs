In this exercise, you are tasked to write a Python program that simulates operations on a school database. The program should enable the creation of three types of users (student, teacher, and homeroom teacher), as well as manage them.

1. Write a program that displays available commands upon launch. The commands are: create, manage, end.

2. Handle each command uniquely:
  - 'create': The program should start the user creation process.
  - 'manage': The program should start the user management process.
  - 'end': Terminate the program.

User Creation Process:

1. Prompt for a user type to create: student, teacher, homeroom teacher, end. After creating a user (except for 'end'), the menu should be displayed again.
  - 'student': Prompt for the student's first and last name (as one or two variables, depending on your design) and the class name (e.g., "3C").
  - 'teacher': Prompt for the teacher's first and last name (as one or two variables, depending on your design), the subject they teach, and the names of the classes they teach, until an empty line is entered.
  - 'homeroom teacher': Prompt for the homeroom teacher's first and last name (as one or two variables, depending on your design), and the name of the class they lead.
  - 'end': Return to the main menu.

User Management Process:

1. Prompt for an option to manage: class, student, teacher, homeroom teacher, end. After managing an option (except for 'end'), the menu should be displayed again.
  - 'class': Prompt for a class to display (e.g., "3C"), the program should list all students in the class and the homeroom teacher.
  - 'student': Prompt for a student's first and last name, the program should list all the classes the student attends and the teachers of these classes.
  - 'teacher': Prompt for a teacher's first and last name, the program should list all the classes the teacher teaches.
  - 'homeroom teacher': Prompt for a homeroom teacher's first and last name, the program should list all students the homeroom teacher leads.
  - 'end': Return to the main menu.

Hints:

- Use loops and conditionals to control the flow of your program.
- Keep track of users and their attributes in suitable data structures.
- Handle possible errors like entering a user that doesn't exist in the database.