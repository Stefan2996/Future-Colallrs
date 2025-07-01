#Initialization of classes
class Student:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name

    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}, Class: {self.class_name}"

class Teacher:
    def __init__(self, first_name, last_name, subject, classes_taught=None):
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject
        self.classes_taught = classes_taught if classes_taught is not None else []

    def __str__(self):
        return f"Teacher: {self.first_name} {self.last_name}, Subject: {self.subject}, Classes: {', '.join(self.classes_taught)}"

class HomeroomTeacher:
    def __init__(self, first_name, last_name, homeroom_class):
        self.first_name = first_name
        self.last_name = last_name
        self.homeroom_class = homeroom_class

    def __str__(self):
        return f"Homeroom teacher: {self.first_name} {self.last_name}, Class: {self.homeroom_class}"


#Initialization of variables
students = []
teachers = []
homeroom_teachers = []
command = ""

while True:
    print("Available commands: create, manage, end")
    command = input("Enter the command: ").lower()

    if command == "create":
        print("\nAvailable user types: student, teacher, homeroom teacher, end - return to main menu")
        user_type = input("Enter the command: ").lower()

        if user_type == "student":
            first_name = input("Enter the student's name: ")
            last_name = input("Enter the student's last name: ")
            class_name = input("Enter the class name (example 4C): ")
            students.append(Student(first_name, last_name, class_name))
            print(f"Student {first_name} {last_name} added to class {class_name}.")

        elif user_type == "teacher":
            first_name = input("Enter the teacher's name: ")
            last_name = input("Enter the teacher's last name: ")
            subject = input("Enter the subject the teacher teaches: ")
            classes = []
            print("Enter the names of the classes the teacher teaches (press Enter to finish):")
            while True:
                class_name = input()
                if not class_name:
                    break
                classes.append(class_name.upper())
            teachers.append(Teacher(first_name, last_name, subject, classes))
            print(f"Teacher {first_name} {last_name} by subject {subject} teaches classes: {', '.join(classes)}.")

        elif user_type == "homeroom teacher":
            first_name = input("Enter the name of the homeroom teacher: ")
            last_name = input("Enter the class teacher's last name: ")
            homeroom_class = input("Enter the name of the class that the class teacher teaches (example: 1B): ")
            homeroom_teachers.append(HomeroomTeacher(first_name, last_name, homeroom_class.upper()))
            print(f"Homeroom teacher {first_name} {last_name} teaches a class {homeroom_class.upper()}.")

        elif user_type == "end":
            print("Exit to the previous page")
            break

        else:
            print("Incorrect. Please select from the options provided.")

    elif command == "manage":
        print("\nSelect a parameter: class, student, teacher, homeroom teacher, end")
        manage_type = input("Enter parameter: ").lower()

        if manage_type == 'class':
            class_name_to_display = input("Enter the class name to display (e.g., 1B): ").upper()
            students_in_class = [s for s in students if s.class_name == class_name_to_display]
            homeroom_teacher_of_class = next((ht for ht in homeroom_teachers if ht.homeroom_class == class_name_to_display), None)

            print(f"\nInformation for class {class_name_to_display}:")
            if students_in_class:
                print("Students:")
                for student in students_in_class:
                    print(f"- {student.first_name} {student.last_name}")
            else:
                print("There are no students in this class.")

            if homeroom_teacher_of_class:
                print(f"Homeroom Teacher: {homeroom_teacher_of_class.first_name} {homeroom_teacher_of_class.last_name}")
            else:
                print("This class does not have a homeroom teacher.")

        elif manage_type == 'student':
            student_name_to_find = input("Enter the student's first and last name (example: John Doe): ").split()
            if len(student_name_to_find) == 2:
                first_name_to_find, last_name_to_find = student_name_to_find
                found_student = None
                for s in students:
                    if s.first_name == first_name_to_find and s.last_name == last_name_to_find:
                        found_student = s
                        break
                if found_student:
                    print(f"\nInformation for student {found_student.first_name} {found_student.last_name}:")
                    print(f"Class: {found_student.class_name}")
                    teachers_of_student = set()
                    for teacher in teachers:
                        if found_student.class_name in teacher.classes_taught:
                            teachers_of_student.add(f"{teacher.first_name} {teacher.last_name} ({teacher.subject})")
                    if teachers_of_student:
                        print("Teachers:")
                        for teacher_info in teachers_of_student:
                            print(f"- {teacher_info}")
                    else:
                        print("This student does not have any assigned teachers yet.")
                else:
                    print(f"Student {first_name_to_find} {last_name_to_find} not found.")
            else:
                print(
                    "Incorrect input of first and last name. Please enter the first and last name separated by a space.")

        elif manage_type == 'teacher':
            teacher_name_to_find = input("Enter the teacher's first and last name (example: Jane Doe): ").split()
            if len(teacher_name_to_find) == 2:
                first_name_to_find, last_name_to_find = teacher_name_to_find
                found_teacher = None
                for t in teachers:
                    if t.first_name == first_name_to_find and t.last_name == last_name_to_find:
                        found_teacher = t
                        break
                if found_teacher:
                    print(f"\nInformation for teacher {found_teacher.first_name} {found_teacher.last_name}:")
                    if found_teacher.classes_taught:
                        print("Teaches classes:")
                        for class_name in found_teacher.classes_taught:
                            print(f"- {class_name}")
                    else:
                        print("This teacher does not teach any classes.")
                else:
                    print(f"Teacher {first_name_to_find} {last_name_to_find} not found.")
            else:
                print(
                    "Incorrect input of first and last name. Please enter the first and last name separated by a space.")
        elif manage_type == 'homeroom teacher':
            ht_name_to_find = input("Enter the homeroom teacher's first and last name (example Peter Brown): ").split()
            if len(ht_name_to_find) == 2:
                first_name_to_find, last_name_to_find = ht_name_to_find
                found_ht = None
                for ht in homeroom_teachers:
                    if ht.first_name == first_name_to_find and ht.last_name == last_name_to_find:
                        found_ht = ht
                        break
                if found_ht:
                    print(f"\nInformation for homeroom teacher {found_ht.first_name} {found_ht.last_name}:")
                    students_in_homeroom_class = [s for s in students if s.class_name == found_ht.homeroom_class]
                    if students_in_homeroom_class:
                        print(f"Students in class {found_ht.homeroom_class}:")
                        for student in students_in_homeroom_class:
                            print(f"- {student.first_name} {student.last_name}")
                    else:
                        print("There are no students in class {found_ht.homeroom_class}.")
                else:
                    print(f"Homeroom teacher {first_name_to_find} {last_name_to_find} not found.")
            else:
                print(
                    "Incorrect input of first and last name. Please enter the first and last name separated by a space.")

    elif command == "end":
        print("End of program")
        break

    else:
        print("Wright the right command")