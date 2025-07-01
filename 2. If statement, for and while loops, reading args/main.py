# Initialization of variables
package_weight = 0  # current parcel weight
item_weight = 0  # item weight

sent_packages = 0  # total number of parcels
total_weight = 0  # total weight for the shift
total_unused_capacity = 0  # total unused weight

unused_capacities = []  # list of parcels that were not fully filled for the shift

total_items = int(input("Enter the number of items you wish to send: "))

for item_count in range(1, total_items + 1):
    # Working with exceptions
    try:
        item_weight = int(input(f"Enter the weight of item {item_count} (1-10 kg, or 0 to stop): "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the weight.")
        continue

    # Exiting the program
    if item_weight == 0:
        print("Exiting the program.")
        break

    # Checking for acceptable weight
    if item_weight < 1 or item_weight > 10:
        print("Incorrect item weight. Weight should be min 1 kg., max 10 kg.")
        continue

    # Adding product to the current package
    if package_weight + item_weight > 20:
        sent_packages += 1
        total_weight = total_weight + package_weight
        unused_capacity = 20 - package_weight
        total_unused_capacity = total_unused_capacity + unused_capacity
        unused_capacities.append(unused_capacity)

        # Start a new package with the current item
        package_weight = item_weight
    elif package_weight == 20:
        unused_capacities.append(0)
    else:
        # Add the item to the current package
        package_weight += item_weight

# At the end, send the last package if it has items
if package_weight > 0:
    sent_packages += 1
    total_weight = total_weight + package_weight
    unused_capacity = 20 - package_weight
    total_unused_capacity += unused_capacity
    unused_capacities.append(unused_capacity)

# Finding the most 'unused' package
max_unused_capacity = max(unused_capacities)

# What if there are several packages?
max_unused_package_numbers = []
for i in range(len(unused_capacities)):
    if unused_capacities[i] == max_unused_capacity:
        max_unused_package_numbers.append(i + 1)  # +1 because we need number, not index

# Display the results
print(f"""-- {sent_packages} packages sent
-- The total weight of the items is {total_weight} kilograms
-- Total 'unused' capacity (non-optimal packaging) is {total_unused_capacity} kilograms
-- The list of unused capacities looks like {unused_capacities}
-- The most 'unused' package is number {max_unused_package_numbers} its unused capacity is {max_unused_capacity}""")  # 0 - if the package is full