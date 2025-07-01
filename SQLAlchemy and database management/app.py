from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os # Для os.path.join и os.path.abspath

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Create a path to the SQLite database file
# app.root_path is the root directory of your Flask application (where app.py is located)
# 'site.db' - database file name
database_path = os.path.join(app.root_path, 'site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
# Disable tracking of modifications, as it consumes a lot of memory and is not always necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_super_secret_key' # Important secret key for flash messages

db = SQLAlchemy(app)

# --- DEFINITION OF MODELS (DATABASE SCHEMA) ---

# Model for products in stock
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False) # Unit price

    def __repr__(self):
        return f"Product('{self.name}', quantity={self.quantity}, price={self.price})"

# Model for a company balance sheet
class CompanyBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=1000000.0) # Initial balance

    def __repr__(self):
        return f"CompanyBalance(amount={self.amount})"

# Model for transaction history
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Transaction('{self.description}', '{self.timestamp}')"


# --- OTHER FUNCTIONS FOR WORKING WITH THE DATABASE ---

def get_current_balance_db():
    balance_record = CompanyBalance.query.first()
    if not balance_record:
        # If there is no balance record, create it with the initial value
        balance_record = CompanyBalance(amount=1000000.0)
        db.session.add(balance_record)
        db.session.commit()
    return balance_record.amount

def update_balance_db(amount, is_add=True):
    balance_record = CompanyBalance.query.first()
    if not balance_record:
        balance_record = CompanyBalance(amount=1000000.0)
        db.session.add(balance_record)
        db.session.commit()

    if is_add:
        balance_record.amount += amount
        description = f"Adding funds ({amount}) to the account."
    else:
        if balance_record.amount < amount:
            description = f"Attempt to withdraw ({amount}) PLN, insufficient funds."
            # We record history even if the operation fails
            add_transaction_db(description + f" (Balance: {balance_record.amount} PLN)")
            db.session.commit()
            return False, "Insufficient funds."
        balance_record.amount -= amount
        description = f"Withdrawal of funds ({amount}) from the account."

    add_transaction_db(description + f" Current balance: {balance_record.amount} PLN")
    db.session.commit()
    return True, f"Balance updated. Current balance: {balance_record.amount} PLN."

def get_current_stock_level_db():
    total_items = db.session.query(db.func.sum(Product.quantity)).scalar()
    return total_items if total_items is not None else 0

def get_warehouse_items_db():
    return Product.query.all()

def add_transaction_db(description):
    new_transaction = Transaction(description=description)
    db.session.add(new_transaction)
    # db.session.commit() # The commit will be done in external functions to group operations

def get_history_range_db(line_from=None, line_to=None):
    query = Transaction.query.order_by(Transaction.timestamp.asc(), Transaction.id.asc())

    total_records = query.count()

    start_index = 0
    end_index = total_records

    try:
        if line_from is not None:
            start_index = int(line_from) - 1
        if line_to is not None:
            end_index = int(line_to)
    except ValueError:
        # In case of conversion error, reset filters
        return query.all(), 0  # Return everything and the initial index 0

    # Checking the correctness of the range
    if start_index < 0: start_index = 0
    if end_index > total_records: end_index = total_records

    # If the start index is greater than or equal to the end index and it is not an empty range
    if start_index >= end_index and total_records > 0:
        return [], 0  # Empty list

    # We apply limits to obtain the required cut
    filtered_records = query.offset(start_index).limit(end_index - start_index).all()

    return filtered_records, start_index

# --- FLASK ROUTES ---
@app.route("/")
@app.route("/index")
def index():
    current_balance = get_current_balance_db()
    current_stock_level = get_current_stock_level_db()
    warehouse_items = get_warehouse_items_db()
    return render_template("index.html",
                           balance=current_balance,
                           stock_level=current_stock_level,
                           warehouse_items=warehouse_items)


@app.route("/purchase", methods=['GET', 'POST'])
def purchase():
    current_balance = get_current_balance_db()
    current_stock_level = get_current_stock_level_db()

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity_str = request.form.get('quantity')
        price_str = request.form.get('price')

        if not all([product_name, quantity_str, price_str]):
            flash("All fields must be filled in!", "error")
        else:
            try:
                quantity = int(quantity_str)
                price = float(price_str) # Replaced int with float

                if quantity <= 0 or price <= 0:
                    flash("Quantity and price must be greater than zero!", "error")
                else:
                    product = Product.query.filter_by(name=product_name.lower()).first()
                    total_cost = quantity * price

                    current_bal = get_current_balance_db()
                    if current_bal < total_cost:
                        add_transaction_db(
                            f"Attempted to purchase ({product_name}) for ({total_cost}) PLN, insufficient funds. Balance: {current_bal} PLN.")
                        db.session.commit()
                        flash(
                            f"Insufficient funds to purchase. Required: {total_cost} PLN, available: {current_bal} PLN.",
                            "error")
                    else:
                        success, msg = update_balance_db(total_cost, is_add=False)  # Withdraw the money
                        if success:
                            if product:
                                product.quantity += quantity
                                product.price = price  # Update the price if the product is already available
                            else:
                                new_product = Product(name=product_name.lower(), quantity=quantity, price=price)
                                db.session.add(new_product)

                            add_transaction_db(f"Purchase: {quantity} units ({product_name}) for {total_cost} PLN.")
                            db.session.commit()  # Commit all changes in this transaction
                            flash(f"Successfully purchased {quantity} units of {product_name}. Cost: {total_cost} PLN.",
                                  "success")
                            return redirect(url_for('purchase'))  # Redirect to the GET version of the page
                        else:
                            flash(msg, "error")  # This message is already being processed by update_balance_db
            except ValueError:
                flash("Quantity must be an integer, price must be a number!", "error")
            except Exception as e:
                db.session.rollback()  # Roll back changes in case of error
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("purchase.html",
                           balance=current_balance,
                           stock_level=current_stock_level)


@app.route("/sale", methods=['GET', 'POST'])
def sale():
    current_balance = get_current_balance_db()
    current_stock_level = get_current_stock_level_db()
    warehouse_items = get_warehouse_items_db()

    if request.method == 'POST':
        product_name = request.form.get('product_name')
        quantity_str = request.form.get('quantity')

        if not all([product_name, quantity_str]):
            flash("All fields must be filled in!", "error")
        else:
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    flash("The quantity to sell must be greater than zero!", "error")
                else:
                    product = Product.query.filter_by(name=product_name.lower()).first()
                    if not product:
                        flash(f"Product '{product_name}' not found in stock.", "error")
                    elif product.quantity < quantity:
                        add_transaction_db(
                            f"Attempting to sell ({product_name}) in ({quantity}) but not enough in stock ({product.quantity}).")
                        db.session.commit()
                        flash(f"There are not enough goods in stock. Available: {product.quantity}, requested: {quantity}.",
                              "error")
                    else:
                        sale_amount = product.price * quantity
                        product.quantity -= quantity

                        success, msg = update_balance_db(sale_amount, is_add=True)  # Adding money
                        if success:
                            add_transaction_db(f"Sale: {quantity} units ({product_name}) for {sale_amount} PLN.")
                            db.session.commit()  # Commit all changes
                            flash(f"Successfully sold {quantity} units of {product_name}. Profit: {sale_amount} PLN.",
                                  "success")
                            return redirect(url_for('sale'))
                        else:
                            flash(msg, "error")  # This message has already been processed by update_balance_db
            except ValueError:
                flash("The quantity must be an integer!", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("sale.html",
                           balance=current_balance,
                           stock_level=current_stock_level,
                           warehouse_items=warehouse_items)


@app.route("/balance_change", methods=['GET', 'POST'])
def balance_change():
    current_balance = get_current_balance_db()
    current_stock_level = get_current_stock_level_db()

    if request.method == 'POST':
        operation_type = request.form.get('operation_type')
        amount_str = request.form.get('amount')

        if not all([operation_type, amount_str]):
            flash("All fields must be filled in!", "error")
        elif operation_type not in ['add', 'sub']:
            flash("Invalid operation type (must be 'add' or 'sub')!", "error")
        else:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash("The amount must be greater than zero!", "error")
                else:
                    success, msg = update_balance_db(amount, is_add=(operation_type == 'add'))
                    if success:
                        flash(msg, "success")
                        return redirect(url_for('balance_change'))
                    else:
                        flash(msg, "error")
            except ValueError:
                flash("The amount must be a number!", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"An unexpected error occurred: {e}", "error")

    return render_template("balance_change.html",
                           balance=current_balance,
                           stock_level=current_stock_level)


@app.route("/history/")
def history():
    line_from_str = request.args.get('line_from')
    line_to_str = request.args.get('line_to')

    # get_history_range_db returns (Transaction list of objects, actual_start_index)
    history_objects, actual_start_index = get_history_range_db(line_from_str, line_to_str)

    # Display only the description from the Transaction objects and number them
    numbered_history_descriptions = []
    for i, transaction in enumerate(history_objects):
        numbered_history_descriptions.append(
            (actual_start_index + i + 1, transaction.description)
            # i + 1 for loop.index, actual_start_index for offset
        )

    if (line_from_str is not None or line_to_str is not None) and not history_objects:
        flash("History in the specified range was not found or the range is invalid. Try again.", "warning")

    # Transfer already numbered descriptions to the template
    return render_template("history.html", history_records=numbered_history_descriptions)


@app.route("/base")
def base():
    return redirect(url_for('index'))


# Program launch code
if __name__ == '__main__':
    # Wrap db.create_all() in app_context so it works outside of a query
    with app.app_context():
        db.create_all() # Create tables when the application starts
        # Initialize the balance if it does not exist
        if not CompanyBalance.query.first():
            db.session.add(CompanyBalance(amount=1000000.0))
            db.session.commit()
            print("Initial balance record created.")

    app.run(debug=True)


    # def create_tables():
    #     # Create tables in the database before the first request to the application
    #     db.create_all()
    #     # Let's make sure there is a balance record if the DB is empty
    #     if not CompanyBalance.query.first():
    #         db.session.add(CompanyBalance(amount=1000000.0))
    #         db.session.commit()
    #     print("Database tables created or already exist.")