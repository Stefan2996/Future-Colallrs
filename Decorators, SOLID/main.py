from ast import literal_eval
import sys

# File names for storing data
BALANCE_FILE = "company_balance.txt"
WAREHOUSE_FILE = "warehouse.txt"
HISTORY_FILE = "history.txt"

# **MODIFIED:** GLOBAL registry for commands
_GLOBAL_COMMAND_REGISTRY = {}


# **MODIFIED:** Decorator function moved outside the class
def assign(command_name):
    """
    Decorator for registering command methods in the global registry.
    """

    def decorator(func):
        _GLOBAL_COMMAND_REGISTRY[command_name.lower()] = func  # Register the function
        return func  # Return the original function

    return decorator


class Manager:
    def __init__(self, initial_balance=1000000):
        self.company_balance = initial_balance
        self.warehouse = {}
        self.history = []

        self._commands = {}
        # **MODIFIED:** Populate instance commands from the GLOBAL registry
        for cmd_name, cmd_func in _GLOBAL_COMMAND_REGISTRY.items():
            # Bind the method to the instance so 'self' is correctly passed when called
            self._commands[cmd_name] = cmd_func.__get__(self, self.__class__)

        self._load_data()

    # --- Data Loading and Saving Methods ---
    def _load_data(self):
        """Loads data from files on Manager initialization."""
        try:
            with open(BALANCE_FILE, "r") as f:
                self.company_balance = int(f.readline())
            print(f"Balance loaded from {BALANCE_FILE}: {self.company_balance} PLN")
        except FileNotFoundError:
            print(f"Balance file ({BALANCE_FILE}) not found. Default balance used.")
        except ValueError:
            print(f"Error reading balance from {BALANCE_FILE}. Default balance used.")

        try:
            with open(WAREHOUSE_FILE, "r") as f:
                warehouse_data = f.read()
                if warehouse_data:
                    self.warehouse = literal_eval(warehouse_data)
            print(f"Warehouse loaded from {WAREHOUSE_FILE}.")
        except FileNotFoundError:
            print(f"Warehouse file ({WAREHOUSE_FILE}) not found. Default warehouse used.")
        except (ValueError, SyntaxError):
            print(f"Error reading warehouse from {WAREHOUSE_FILE}. Default warehouse used.")

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                self.history = [line.strip() for line in f]
            print(f"History loaded from {HISTORY_FILE}. Found {len(self.history)} operations.")
        except FileNotFoundError:
            print(f"History file ({HISTORY_FILE}) not found. History is empty.")
        except UnicodeDecodeError:
            print(f"Encoding error reading history from {HISTORY_FILE}. History may be incomplete.")

    def _save_data(self):
        """Saves data to files on program exit."""
        try:
            with open(BALANCE_FILE, "w") as f:
                f.write(str(self.company_balance))
            print(f"Balance saved in {BALANCE_FILE}: {self.company_balance} PLN")
        except Exception as e:
            print(f"Error saving balance to {BALANCE_FILE}: {e}")

        try:
            with open(WAREHOUSE_FILE, "w") as f:
                f.write(str(self.warehouse))
            print(f"Warehouse saved in {WAREHOUSE_FILE}.")
        except Exception as e:
            print(f"Error saving warehouse to {WAREHOUSE_FILE}: {e}")

        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                for item in self.history:
                    f.write(item + "\n")
            print(f"History saved in {HISTORY_FILE}.")
        except Exception as e:
            print(f"Error saving history to {HISTORY_FILE}: {e}")

    # --- Command Methods defined using decorators ---

    # **MODIFIED:** Decorator 'assign' is now imported (or defined globally)
    @assign("balance")
    def _handle_balance(self):
        balance_operation = input("What operation do you want to perform? add/sub: ").lower()
        if balance_operation == "add":
            try:
                balance_num = int(input("Enter the amount you want to add to the company account: "))
                if balance_num < 0:
                    print("Amount cannot be negative.")
                else:
                    self.company_balance += balance_num
                    print(f"Now on your balance: {self.company_balance} PLN")
                    self.history.append(f"Adding money ({balance_num}) to an account")
            except ValueError:
                print("Invalid input. Please enter a whole number.")
        elif balance_operation == "sub":
            try:
                balance_num = int(input("Enter the amount you want to subtract from the company account: "))
                if balance_num < 0:
                    print("Amount cannot be negative.")
                elif self.company_balance < balance_num:
                    print("Insufficient funds to subtract this amount.")
                else:
                    self.company_balance -= balance_num
                    print(f"Now on your balance: {self.company_balance} PLN")
                    self.history.append(f"Withdrawing money ({balance_num}) from an account")
            except ValueError:
                print("Invalid input. Please enter a whole number.")
        else:
            print("Enter the correct command (add or sub)")

    # **MODIFIED:** Decorator is now @assign
    @assign("sale")
    def _handle_sale(self):
        name_of_products = list(self.warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        sale_product = input("Enter the name of the product you want to sell: ").lower()
        if sale_product in name_of_products:
            product_info = self.warehouse[sale_product]
            product_price = product_info["price"]
            product_quantity = product_info["quantity"]
            print(f"Available in stock {product_quantity} items"
                  f"\nThe price of this is: {product_price} PLN")
            try:
                sale_quantity = int(input(f"How much of {sale_product} do you want to sell? "))
                if sale_quantity <= 0:
                    print("Quantity must be greater than zero.")
                elif sale_quantity > product_quantity:
                    print(
                        "You will not be able to perform this operation. You do not have enough goods in your warehouse.")
                    self.history.append(
                        f"Attempted to sell ({sale_product}) quantity ({sale_quantity}), but not enough in stock.")
                else:
                    self.warehouse[sale_product]["quantity"] -= sale_quantity
                    sale_amount = product_price * sale_quantity
                    self.company_balance += sale_amount
                    self.history.append(f"Selling {sale_quantity} item(s) of ({sale_product})"
                                        f" for ({sale_amount}) PLN, balance: {self.company_balance} PLN")
                    print(
                        f"You sold {sale_quantity} {sale_product} and made a profit of {sale_amount} PLN"
                        f"\nNow on your account {self.company_balance} PLN")
            except ValueError:
                print("Invalid input. Please enter a whole number for quantity.")
        else:
            print("Enter the correct product from the list.")

    # **MODIFIED:** Decorator is now @assign
    @assign("purchase")
    def _handle_purchase(self):
        while True:
            purchase_product = input("Enter the name of the product you want to buy: ").lower()

            try:
                purchase_product_quantity = int(input("Enter the quantity of the item you want to buy: "))
                if purchase_product_quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a whole number (without letters).")
                continue

            try:
                purchase_product_price = int(input("Enter the price of the item you want to buy: "))
                if purchase_product_price <= 0:
                    print("Price must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a whole number (without letters).")
                continue

            total_cost = purchase_product_quantity * purchase_product_price
            print(
                f"You want to buy {purchase_product_quantity} items ({purchase_product}), the total amount is {total_cost} PLN.")

            while True:
                purchase_answer = input("Do you want to continue? y/n ").lower()
                if purchase_answer in ("n", "no"):
                    print("Okay, then let's go to the main page.")
                    break
                elif purchase_answer in ("y", "yes"):
                    if self.company_balance >= total_cost:
                        if purchase_product in self.warehouse:
                            self.warehouse[purchase_product]["quantity"] += purchase_product_quantity
                        else:
                            self.warehouse[purchase_product] = {"price": purchase_product_price,
                                                                "quantity": purchase_product_quantity}
                        self.company_balance -= total_cost
                        self.history.append(f"Purchase ({purchase_product}) in quantity ({purchase_product_quantity}) "
                                            f"for ({total_cost}) PLN, balance: {self.company_balance} PLN")
                        print(f"Successfully purchased {purchase_product_quantity} {purchase_product}(s).")
                    else:
                        print(
                            f"You do not have enough funds in your account for this purchase. Needed {total_cost} PLN, available {self.company_balance} PLN.")
                        self.history.append(
                            f"Attempted purchase of ({purchase_product}) for ({total_cost}) PLN, insufficient funds.")

                    name_of_products = list(self.warehouse.keys())
                    print(f"\nNow your product list looks like this: {name_of_products}"
                          f"\nAnd on your account: {self.company_balance} PLN")
                    break
                else:
                    print("Enter the correct answer (y/n).")
            break

    # **MODIFIED:** Decorator is now @assign
    @assign("account")
    def _handle_account(self):
        self.history.append(f"Checked balance: {self.company_balance} PLN")
        print(f"Now on your balance: {self.company_balance} PLN")

    # **MODIFIED:** Decorator is now @assign
    @assign("list")
    def _handle_list(self):
        name_of_products = list(self.warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        product_request = input("Enter the name of any product available in stock: ").lower()
        if product_request in name_of_products:
            product_info = self.warehouse[product_request]
            product_price = product_info["price"]
            product_quantity = product_info["quantity"]
            self.history.append(f"Checked quantity of ({product_request}) in stock: {product_quantity}")
            print(f"In stock now: {product_quantity} items"
                  f"\nPrice for one product: {product_price} PLN"
                  f"\nThe total cost is {product_quantity * product_price} PLN")
        else:
            print("Enter the correct product from the list.")

    # **MODIFIED:** Decorator is now @assign
    @assign("warehouse")
    def _handle_warehouse(self):
        name_of_products = list(self.warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        availability_request = input("Enter the product you want to know the status of: ").lower()
        if availability_request in name_of_products:
            product_quantity = self.warehouse[availability_request]["quantity"]
            self.history.append(f"Viewed product ({availability_request}) availability in stock: {product_quantity}")
            if product_quantity > 0:
                print(f"The {availability_request} is in stock ({product_quantity} items).")
            else:
                print(f"The {availability_request} is out of stock.")
        else:
            print("Enter the correct product from the list.")

    # **MODIFIED:** Decorator is now @assign
    @assign("review")
    def _handle_review(self):
        operation_number = 1
        history_len = len(self.history)
        print(
            f"\nHistory of all operations during the program. At the moment {history_len} operations have been performed")
        review_from_str = input(
            "From which operation to start the withdrawal with? ('Enter' to see the full list of actions) ").strip()
        review_to_str = input(
            "On which operation should the output be completed? ('Enter' to see the full list of actions) ").strip()

        if not review_from_str and not review_to_str:
            for message in self.history:
                print(f"Operation {operation_number}. {message}")
                operation_number += 1
        else:
            try:
                review_from = int(review_from_str) if review_from_str else 1
                review_to = int(review_to_str) if review_to_str else history_len

                if review_from < 1 or review_to > history_len or review_from > review_to:
                    print("Enter the correct range of operations (starting from 1).")
                else:
                    for i, message in enumerate(self.history[review_from - 1:review_to]):
                        print(f"Operation {review_from + i}. {message}")
            except ValueError:
                print("Enter the correct numeric value for the operation number.")

    # **MODIFIED:** Decorator is now @assign
    @assign("end")
    def _handle_end(self):
        self._save_data()
        print("End of the program")
        sys.exit(0)

    # Method to execute commands
    def execute_command(self, command_name):
        command_name = command_name.lower()
        if command_name in self._commands:
            self._commands[command_name]()
        else:
            print("Enter the correct command")


# --- Main Program Execution ---
if __name__ == "__main__":
    manager = Manager()

    while True:
        print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end:")
        command = input("Enter the command You want to execute: ")

        manager.execute_command(command)