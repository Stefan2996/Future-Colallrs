from flask import Flask, render_template, request, redirect, url_for, flash
import os
from ast import literal_eval
import sys


# File names for storing data
BALANCE_FILE = "company_balance.txt"
WAREHOUSE_FILE = "warehouse.txt"
HISTORY_FILE = "history.txt"

_GLOBAL_COMMAND_REGISTRY = {}


def assign(command_name):
    def decorator(func):
        _GLOBAL_COMMAND_REGISTRY[command_name.lower()] = func
        return func

    return decorator


class Manager:
    def __init__(self, initial_balance=1000000):
        self.company_balance = initial_balance
        self.warehouse = {}  # Dictionary: {'product_name': {'price': N, 'quantity': M}}
        self.history = []

        self._commands = {}
        for cmd_name, cmd_func in _GLOBAL_COMMAND_REGISTRY.items():
            self._commands[cmd_name] = cmd_func.__get__(self, self.__class__)

        self._load_data()

    def _load_data(self):
        try:
            with open(BALANCE_FILE, "r") as f:
                self.company_balance = int(f.readline())
        except FileNotFoundError:
            pass  # Use the default balance.
        except ValueError:
            pass

        try:
            with open(WAREHOUSE_FILE, "r") as f:
                warehouse_data = f.read()
                if warehouse_data:
                    self.warehouse = literal_eval(warehouse_data)
        except FileNotFoundError:
            pass
        except (ValueError, SyntaxError):
            pass

        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                self.history = [line.strip() for line in f if line.strip()]  # Skipping empty lines
        except FileNotFoundError:
            pass
        except UnicodeDecodeError:
            pass
        except Exception as e:
            pass

    def _save_data(self):
        """Saves data to files."""
        try:
            with open(BALANCE_FILE, "w") as f:
                f.write(str(self.company_balance))
        except Exception as e:
            pass

        try:
            with open(WAREHOUSE_FILE, "w") as f:
                f.write(str(self.warehouse))
        except Exception as e:
            pass

        try:
            with open(HISTORY_FILE, "w") as f:
                for item in self.history:
                    f.write(item + "\n")
        except Exception as e:
            pass

    # --- Command Methods ---
    def add_or_subtract_balance(self, operation, amount):
        """Handles adding or subtracting balance."""
        amount = int(amount) # We assume that the number has already been validated

        if amount < 0:
            return "The amount cannot be negative.", False

        if operation == "add":
            self.company_balance += amount
            self.history.append(f"Adding funds ({amount}) to the account. Balance: {self.company_balance} PLN")
            self._save_data()
            return f"Balance successfully replenished. Current balance: {self.company_balance} PLN.", True
        elif operation == "sub":
            if self.company_balance < amount:
                self.history.append(
                    f"Attempt to withdraw ({amount}) PLN, insufficient funds. Balance: {self.company_balance} PLN")
                self._save_data()
                return f"Insufficient funds. Available: {self.company_balance} PLN, requested: {amount} PLN.", False
            else:
                self.company_balance -= amount
                self.history.append(f"Withdrawal of funds ({amount}) from the account. Balance: {self.company_balance} PLN")
                self._save_data()
                return f"Funds successfully withdrawn. Current balance: {self.company_balance} PLN.", True
        else:
            return "Invalid operation (must be 'add' or 'sub').", False

    def sell_product(self, product_name, quantity):
        """Handles selling a product."""
        product_name = product_name.lower()
        quantity = int(quantity)  # We assume that the number has already been validated

        if product_name not in self.warehouse:
            return f"Product '{product_name}' not found in stock.", False

        product_info = self.warehouse[product_name]
        product_price = product_info["price"]
        available_quantity = product_info["quantity"]

        if quantity <= 0:
            return "The quantity to sell must be greater than zero.", False
        elif quantity > available_quantity:
            self.history.append(
                f"Attempting to sell ({product_name}) in ({quantity}) but not enough in stock ({available_quantity}).")
            self._save_data()
            return f"Not enough product in stock. Available: {available_quantity}, requested: {quantity}.", False
        else:
            self.warehouse[product_name]["quantity"] -= quantity
            sale_amount = product_price * quantity
            self.company_balance += sale_amount
            self.history.append(
                f"Sale: {quantity} units ({product_name}) for {sale_amount} PLN. Balance: {self.company_balance} PLN. In stock: {self.warehouse[product_name]['quantity']} units.")
            self._save_data()
            return f"Successfully sold {quantity} units of {product_name}. Profit: {sale_amount} PLN. Current balance: {self.company_balance} PLN.", True

    def purchase_product(self, product_name, quantity, price):
        """Handles purchasing a product."""
        product_name = product_name.lower()
        quantity = int(quantity)
        price = int(price)

        if quantity <= 0:
            return "The quantity must be greater than zero..", False
        if price <= 0:
            return "The price must be greater than zero.", False

        total_cost = quantity * price

        if self.company_balance < total_cost:
            self.history.append(
                f"Attempted to buy ({product_name}) for ({total_cost}) PLN, insufficient funds. Balance: {self.company_balance} PLN.")
            self._save_data()
            return f"Insufficient funds to purchase. Required: {total_cost} PLN, available: {self.company_balance} PLN.", False
        else:
            if product_name in self.warehouse:
                self.warehouse[product_name]["quantity"] += quantity
            else:
                self.warehouse[product_name] = {"price": price, "quantity": quantity}
            self.company_balance -= total_cost
            self.history.append(
                f"Purchase: {quantity} units ({product_name}) for {total_cost} PLN. Balance: {self.company_balance} PLN. In stock: {self.warehouse[product_name]['quantity']} units.")
            self._save_data()
            return f"Successfully purchased {quantity} units of {product_name}. Cost: {total_cost} PLN. Current balance: {self.company_balance} PLN.", True

    def get_history_range(self, line_from=None, line_to=None):
        """
        Returns history based on optional start and end lines.
        Returns (list_of_history_records, actual_start_index)
        """

        if line_from is None and line_to is None:
            # If the entire history is requested, the starting index is 0
            return self.history, 0  # Return the entire history and the starting index 0 (for the 1st entry)

        try:
            start_index = int(line_from) - 1 if line_from is not None else 0
            end_index = int(line_to) if line_to is not None else len(self.history)

            if start_index < 0 or (start_index >= len(self.history) and len(self.history) > 0):
                return [], 0  # Invalid starting index

            if end_index > len(self.history):
                end_index = len(self.history)

            if start_index >= end_index:
                return [], 0  # Empty list if range is invalid

            # Return the history slice and the actual starting index of the slice
            return self.history[start_index:end_index], start_index
        except ValueError:
            return [], 0  # Return an empty list and 0 if the parameters are not numeric
        except Exception as e:
            print(f"Error in get_history_range: {e}")
            return [], 0

    # Methods for getting the current state (for the main page)
    def get_current_balance(self):
        return self.company_balance

    def get_current_stock_level(self):
        """Calculates total stock level. Can be sum of quantities or number of unique products."""
        total_items = sum(item['quantity'] for item in self.warehouse.values())
        # Or if you want number of unique products:
        # total_unique_products = len(self.warehouse)
        return total_items  # Return the total quantity of all goods in the warehouse

    def get_warehouse_items(self):
        return self.warehouse


# --- END OF MANAGER CLASS CODE ---


app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # For flash messages. I'll have to remember to change it to something unique.

manager = Manager()

# DECORATORS
@app.route("/")
@app.route("/index")
def index():
    current_balance = manager.get_current_balance()
    current_stock_level = manager.get_current_stock_level()
    warehouse_items = manager.get_warehouse_items()  # If you need to display warehouse details
    return render_template("index.html",
                           balance=current_balance,
                           stock_level=current_stock_level,
                           warehouse_items=warehouse_items)


@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    current_balance = manager.get_current_balance()
    current_stock_level = manager.get_current_stock_level()

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity_str = request.form.get('quantity')
        price_str = request.form.get('price')

        if not all([product_name, quantity_str, price_str]):
            flash("All fields must be filled in!", "error")
        else:
            try:
                quantity = int(quantity_str)
                price = int(price_str)
                message, success = manager.purchase_product(product_name, quantity, price)
                if success:
                    flash(message, "success")
                    return redirect(url_for('purchase'))  # Redirect to the GET version of the page
                else:
                    flash(message, "error")
            except ValueError:
                flash("Quantity and price must be whole numbers!", "error")
            except Exception as e:
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("purchase.html",
                           balance=current_balance,
                           stock_level=current_stock_level)


@app.route("/sale", methods=['GET', 'POST'])
def sale():
    current_balance = manager.get_current_balance()
    current_stock_level = manager.get_current_stock_level()
    warehouse_items = manager.get_warehouse_items()  # To display a list of products for sale

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity_str = request.form.get('quantity')

        if not all([product_name, quantity_str]):
            flash("All fields must be filled in!", "error")
        else:
            try:
                quantity = int(quantity_str)
                message, success = manager.sell_product(product_name, quantity)
                if success:
                    flash(message, "success")
                    return redirect(url_for('sale'))
                else:
                    flash(message, "error")
            except ValueError:
                flash("The quantity must be an integer!", "error")
            except Exception as e:
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("sale.html",
                           balance=current_balance,
                           stock_level=current_stock_level,
                           warehouse_items=warehouse_items)


@app.route("/balance_change", methods=['GET', 'POST'])
def balance_change():
    current_balance = manager.get_current_balance()
    current_stock_level = manager.get_current_stock_level()

    if request.method == 'POST':
        operation_type = request.form.get('operation_type')
        amount_str = request.form.get('amount')

        if not all([operation_type, amount_str]):
            flash("All fields must be filled in!", "error")
        elif operation_type not in ['add', 'sub']:
            flash("Invalid operation type (must be 'add' or 'sub')!", "error")
        else:
            try:
                amount = int(amount_str)
                message, success = manager.add_or_subtract_balance(operation_type, amount)
                if success:
                    flash(message, "success")
                    return redirect(url_for('balance_change'))
                else:
                    flash(message, "error")
            except ValueError:
                flash("The amount must be an integer!", "error")
            except Exception as e:
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("balance_change.html",
                           balance=current_balance,
                           stock_level=current_stock_level)


@app.route("/history/")
def history():
    # Get parameters from request.args (for GET requests)
    line_from_str = request.args.get('line_from')
    line_to_str = request.args.get('line_to')

    line_from = None
    line_to = None

    # Attempt to convert to int if values are present
    try:
        if line_from_str:
            line_from = int(line_from_str)
        if line_to_str:
            line_to = int(line_to_str)
    except ValueError:
        flash("Operation numbers must be integers.", "error")
        # Reset the parameters to show the entire history in case of incorrect input
        line_from = None
        line_to = None

    # Call the Manager method with the transformed parameters
    history_records, actual_start_index = manager.get_history_range(line_from, line_to)

    if (line_from is not None or line_to is not None) and not history_records:
        flash("History in the specified range was not found or the range is invalid. Try again.", "warning")

    # Pass actual_start_index to the template
    return render_template("history.html", history_records=history_records, actual_start_index=actual_start_index)


# Program launch code
if __name__ == '__main__':
    app.run(debug=True)