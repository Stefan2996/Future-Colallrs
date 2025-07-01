import datetime

current_time = datetime.datetime.now()

user_name = input("Hello, enter some information about you to create a greeting card. What is your name? ")
recipient = input("Enter the name of recipient: ")
recipient_birth = int(input("Thank you. And now enter the year of his/she birth: "))
user_message = input("Enter your message: ")

recipient_age = current_time.year - recipient_birth

print(f"""\n{recipient}, let's celebrate your {recipient_age} years of awesomeness!
Wishing you a day filledwith joyand laughteras you turn {recipient_age}!

{user_message}

With loveand best wishes,
{user_name}""")