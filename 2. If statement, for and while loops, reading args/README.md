###Exercise:
In this exercise, you are tasked to create a Python program that simulates a package loading system. Each package can carry a maximum of 20 kg of goods. Items are added to the package with weights ranging from 1 to 10 kg. If adding an item to the package would exceed the 20 kg limit, the package should be sent, and the current item should start a new package. If an item with a weight of 0 is given, the program should terminate.

**1. Write a program that prompts the user for the maximum number of items to be shipped.**
**2. The program should allow the user to enter the weight of each item, one by one.**
**3. If adding an item would increase the total weight of the current package above 20 kg, mark the current package as sent and start a new package with the current item.**
**4. If an item with a weight of 0 kg is given, the program should terminate as if the maximum number of items has been reached.**
**5. At the end of the program, display the following information:**

  Number of packages sent
  Total weight of packages sent
  Total 'unused' capacity (non-optimal packaging). This is calculated as the number of packages sent multiplied by 20 kg, minus the total weight of packages sent.
  The package number that had the most 'unused' capacity and the amount of 'unused' capacity in that package.

####Hints:

- Use a loop to continuously prompt the user for item weights until the maximum number of items has been reached or an item with a weight of 0 kg is given.
- Keep track of the current package's total weight and the number of packages sent.
- Remember to handle cases where the weight of an item is outside the acceptable range (1 to 10 kg, unless it's 0).
- Handle user inputs that are not as expected (for example, if the user enters a string instead of a number for the item's weight). The program should not crash in these cases, but instead, it should display an appropriate error message.

####How to Use
Run the script: Execute the Python file from your terminal.