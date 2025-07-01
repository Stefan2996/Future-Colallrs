## Simple accounting system / Warehouse
### Exercise:
In this exercise, you are tasked to write a Python program that simulates operations on a company's account and a warehouse. The program should handle various commands for performing operations like adding/subtracting balance, recording sales and purchases, displaying account balance, showing warehouse status, and reviewing recorded operations.

### Instructions:
1. **Write a program that displays available commands upon launch. The commands are:**
  - balance
  - sale
  - purchase
  - account
  - list
  - warehouse
  - review
  - end

2. **Handle each command uniquely:**
  - 'balance': The program should prompt for an amount to add or subtract from the account.
  - 'sale': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly.
  - 'purchase': The program should prompt for the name of the product, its price, and quantity. Perform necessary calculations and update the account and warehouse accordingly. Ensure that the account balance is not negative after a purchase operation.
  - 'account': Display the current account balance.
  - 'list': Display the total inventory in the warehouse along with product prices and quantities.
  - 'warehouse': Prompt for a product name and display its status in the warehouse.
  - 'review': Prompt for two indices 'from' and 'to', and display all recorded operations within that range. If ‘from’ and ‘to’ are empty, display all recorder operations. Handle cases where 'from' and 'to' values are out of range.
  - 'end': Terminate the program.

3. **After executing any command, the program should again display the list of commands and prompt for the next command.**

#### Hints:
- Use a loop to continuously prompt for commands until the 'end' command is entered.
- Keep track of the account balance and warehouse inventory.
- Remember to handle edge cases, like invalid command inputs, negative amounts during a 'purchase' operation, or out-of-range indices during a 'review' operation.
- The balance, sale, and purchase commands are remembered by the program.
- Handle user inputs that are not as expected. The program should not crash in these cases, but instead, it should display an appropriate error message.
