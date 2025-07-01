#Initialization of variables
command = ""
company_balance = 1000000
history = []
warehouse = {
    "bike": {
        "price": 540,
        "quantity": 0
    },
    "computer": {
        "price": 4800,
        "quantity": 3
    },
    "smartphone": {
        "price": 2700,
        "quantity": 8
    },
    "microwave": {
        "price": 1100,
        "quantity": 3
    }
}

while True:
    print("\nAvailable commands: balance, sale, purchase, account, list, warehouse, review, end:")
    command = input("Enter the command You want to execute: ")

    #Add or subtract amounts from the company's overall balance sheet
    if command.lower() == "balance":
        balance = input("What operation do you want to perform? add/sub: ")
        if balance.lower() == "add":
            balance_num = int(input("Enter the amount you want to add to the company account: "))
            company_balance += balance_num
            print(f"Now on your balance: {company_balance} PLN")
            history.append(f"Adding money ({balance_num}) to an account")
        elif balance.lower() == "sub":
            balance_num = int(input("Enter the amount you want to subtract from the company account: "))
            company_balance -= balance_num
            print(f"Now on your balance: {company_balance} PLN")
            history.append(f"Withdrawing money ({balance_num}) from an account")
        else:
            print("Enter the correct command (add or sub)")

    #Sale of goods and crediting of funds for this transaction
    elif command.lower() == "sale":
        name_of_products = list(warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        sale_product = input("Enter the name of the product you want to sell: ")
        if sale_product.lower() in name_of_products:
            product_price = warehouse[sale_product]["price"]
            product_quantity = warehouse[sale_product]["quantity"]
            print(f"Available in stock {product_quantity} items"
                  f"\nThe price of this is: {product_price} PLN")
            sale_quantity = int(input(f"How much of {sale_product} do you want to sell? "))
            if sale_quantity > product_quantity or sale_quantity < 0:
                print("You will not be able to perform this operation. You do not have enough goods in your warehouse.")
                history.append(f"You tried to sell the ({sale_product}), but you didn't have enough of it in stock.")
            else:
                warehouse[sale_product]["quantity"] -= sale_quantity
                company_balance += product_price * sale_quantity
                history.append(f"Selling an ({sale_quantity}) item(s) ({sale_product})"
                               f" and receiving money ({product_price * sale_quantity}) into the account")
                print(
                    f"You sold {sale_quantity} {sale_product} and made a profit of {product_price * sale_quantity} PLN"
                    f"\nNow on your account {company_balance} PLN")
        else:
            print("Enter the correct product")

    #Purchase of goods and deduction of funds for this operation, adding new goods to the warehouse
    elif command.lower() == "purchase":
        while True:
            #Initializing new variables and dealing with their exceptions
            purchase_product = input("Enter the name of the product you want to buy: ")
            purchase_product = purchase_product.lower()

            while True:
                try:
                    purchase_product_quantity = int(input("Enter the quantity of the item you want to buy: "))
                    if purchase_product_quantity <= 0:
                        print("Quantity must be greater than zero.")
                    else:
                        break  #Exit the loop if the input is correct
                except ValueError:
                    print("Invalid input. Please enter a whole number (without letters).")

            while True:
                try:
                    purchase_product_price = int(input("Enter the price of the item you want to buy: "))
                    if purchase_product_price <= 0:
                        print("Price must be greater than zero.")
                    else:
                        break  #Exit the loop if the input is correct
                except ValueError:
                    print("Invalid input. Please enter a whole number (without letters).")

            print(f"You want to buy {purchase_product_quantity} items ({purchase_product}), the total amount is {purchase_product_quantity * purchase_product_price}:")

            #Adding a new product to the warehouse
            while True:
                purchase_answer = input("Do you want to continue? y/n ")
                if purchase_answer.lower() == "n" or purchase_answer.lower() == "no":
                    print("Okay, then let's go to the main page")
                    break
                elif purchase_answer.lower() == "y" or purchase_answer.lower() == "yes":
                    #Checking for funds in the account
                    if company_balance > purchase_product_price * purchase_product_quantity:
                        warehouse[f"{purchase_product}"] = {"price": purchase_product_price, "quantity": purchase_product_quantity}
                        company_balance -= purchase_product_price * purchase_product_quantity
                        history.append(f"Purchase ({purchase_product}) in quantity ({purchase_product_quantity})"
                                       f" and subtracting money ({purchase_product_price * purchase_product_quantity}) from the account")
                    else:
                        print("You do not have enough funds in your account for this purchase")

                    name_of_products = list(warehouse.keys())
                    print(f"\nNow your product list looks like this: {name_of_products}"
                          f"\nAnd on your account: {company_balance} PLN")
                    break #Exiting the purchase cycle after successful (or unsuccessful) addition of a product
                else:
                    print("Enter the correct answer")
            break

    #Find out how much money is in the account
    elif command == "account":
        history.append("You have checked your balance")
        print(f"Now on your balance: {company_balance} PLN")

    #Display total inventory in the warehouse along with prices and quantities of products
    elif command.lower() == "list":
        name_of_products = list(warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        product_request = input("Enter the name of any product available in stock: ")
        if product_request.lower() in name_of_products:
            product_price = warehouse[product_request]["price"]
            product_quantity = warehouse[product_request]["quantity"]
            history.append(f"You have checked the quantity of ({product_request}) in stock")
            print(f"In stock now: {product_quantity} items"
                  f"\nPrice for one product: {product_price} PLN"
                  f"\nThe total cost is {product_quantity * product_price} PLN")
        else:
            print("Enter the correct product")

    #Request product name and display its status in stock
    elif command.lower() == "warehouse":
        name_of_products = list(warehouse.keys())
        print(f"\nList of products: {name_of_products}")
        availability_request = input("Enter the product you want to know the status of: ")
        if availability_request.lower() in name_of_products:
            product_quantity = warehouse[availability_request]["quantity"]
            history.append(f"View product ({availability_request}) availability in stock")
            if product_quantity > 0:
                print(f"The {availability_request} is in stock")
            else:
                print(f"The {availability_request} is out of stock")
        else:
            print("Enter the correct product")


    #History of all operations
    elif command.lower() == "review":
        operation_number = 1
        history_len = len(history)
        print(f"\nHistory of all operations during the program. At the moment {history_len} operations have been performed")
        review_from_str = input("From which operation to start the withdrawal with? ('Enter' to see the full list of actions) ")
        review_to_str = input("On which operation should the output be completed? ('Enter' to see the full list of actions) ")

        if not review_from_str and not review_to_str:
            for message in history:
                print(f"Operation {operation_number}. {message}")
                operation_number += 1

        else:
            try:
                review_from = int(review_from_str)
                review_to = int(review_to_str)

                if review_from < 0 or review_to > history_len or review_from > review_to:
                    print("Enter the correct range of operations.")
                elif review_from == 0 and not review_to == history_len:
                    for message in history:
                        print(f"Operation {operation_number}. {message}")
                        operation_number += 1
                elif review_from == 0 and review_to > 0:
                    for i, message in enumerate(history[:review_to]):
                        print(f"Operation {i + 1}. {message}")
                elif review_from > 0 and review_to > 0:
                    for i, message in enumerate(history[review_from - 1:review_to]):
                        print(f"Operation {review_from + i}. {message}")
                else:
                    print("Enter the correct range of operations.")

            except ValueError:
                print("Enter the correct numeric value for the operation number.")

    #Exiting the program
    elif command.lower() == "end":
        print("End of the program")
        break

    else:
        print("Enter the correct command")