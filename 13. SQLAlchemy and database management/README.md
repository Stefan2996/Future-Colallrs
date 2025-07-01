## Implementing database in Accounting Web Application
### Exercise:
In this exercise, you will modify the existing accounting system web application to use an SQLite database for data persistence instead of a text file. You will create a database schema using Flask-SQLAlchemy, an extension for Flask that simplifies the use of SQLAlchemy for managing relational databases.

1. **Set up an SQLite database for your application. Design a schema using Flask-SQLAlchemy that can store all the necessary data (products, their quantities, account balance, transaction history, etc.).**

2. **Modify the application to use the SQLite database for all data storage. This includes updating the current stock level, account balance, and transaction history.**

3. **Ensure that the application can handle potential database errors gracefully.**

4. **Do not include the actual database file in your repository.**

### Hints:
- Flask-SQLAlchemy is a Flask extension that simplifies the use of SQLAlchemy, a powerful and flexible Object-Relational Mapper (ORM) for Python, with Flask applications.
- Remember to handle potential exceptions that might be raised when interacting with the database.
- When designing your database schema, consider the types of data you want to store in your tables
