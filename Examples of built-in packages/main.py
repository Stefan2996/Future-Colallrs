import sys
import csv
import os

def modify_csv(src_path, dst_path, changes):
    """
    Modifies a CSV file based on user-provided changes,
    displays its content, and saves the modified file.

    Args:
        src_path (str): Path to the source CSV file.
        dst_path (str): Path to save the modified CSV file.
        changes (list): List of change strings in the format "X,Y,value".
    """
    if not os.path.exists(src_path) or not os.path.isfile(src_path):
        print(f"Error: Source file '{src_path}' does not exist or is not a file.")
        print("Files in the current directory:")
        for item in os.listdir('.'):
            print(f"- {item}")
        return

    data = []
    try:
        with open(src_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading source CSV file '{src_path}': {e}")
        return

    print("\nOriginal CSV content:")
    for row in data:
        print(','.join(row))

    print("\nApplying changes:")
    for change in changes:
        try:
            col_str, row_str, value = change.split(',')
            col = int(col_str)
            row = int(row_str)

            if 0 <= row < len(data) and 0 <= col < len(data[row]):
                print(f"  - Changing cell [{row},{col}] from '{data[row][col]}' to '{value}'")
                data[row][col] = value
            else:
                print(f"  - Warning: Invalid row or column index in change '{change}'. Skipping.")
        except ValueError:
            print(f"  - Warning: Invalid change format '{change}'. Expected 'X,Y,value'. Skipping.")
        except IndexError:
            print(f"  - Warning: Insufficient values in change '{change}'. Expected 'X,Y,value'. Skipping.")

    print("\nModified CSV content:")
    for row in data:
        print(','.join(row))

    try:
        with open(dst_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"\nModified CSV file saved to '{dst_path}'")
    except Exception as e:
        print(f"Error writing to destination CSV file '{dst_path}': {e}")

if len(sys.argv) < 4:
    print("Usage: reader.py <source_file> <destination_file> <change1> <change2> ...")
    sys.exit(1)

src_file = sys.argv[1]
dst_file = sys.argv[2]
changes = sys.argv[3:]

modify_csv(src_file, dst_file, changes)
