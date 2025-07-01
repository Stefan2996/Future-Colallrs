import sys
import csv
import json
import os
from abc import ABC, abstractmethod


# --- Base File Manager Class ---
class FileManager(ABC):
    def __init__(self, src_path, dst_path, changes):
        self.src_path = src_path
        self.dst_path = dst_path
        self.changes = changes
        self.data = []

    def _check_source_file(self):
        """Checks if the source file exists and is a valid file."""
        if not os.path.exists(self.src_path):
            print(f"Error: Source file '{self.src_path}' does not exist.")
            print("Files in the current directory:")
            for item in os.listdir('.'):
                print(f"- {item}")
            return False
        if not os.path.isfile(self.src_path):
            print(f"Error: Path '{self.src_path}' is not a file.")
            print("Files in the current directory:")
            for item in os.listdir('.'):
                print(f"- {item}")
            return False
        return True

    @abstractmethod
    def _load_data(self):
        """Abstract method to load data from the source file into self.data."""
        pass

    @abstractmethod
    def _save_data(self):
        """Abstract method to save data from self.data to the destination file."""
        pass

    def _apply_changes(self):
        """Applies the given changes (X,Y,value) to the internal data (list of lists)."""
        print("\nApplying changes:")
        for change in self.changes:
            try:
                parts = change.split(',')
                if len(parts) != 3:
                    raise ValueError("Incorrect number of parts.")

                col_str, row_str, value = parts
                col = int(col_str.strip())
                row = int(row_str.strip())

                if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
                    print(f"  - Changing cell [{row},{col}] from '{self.data[row][col]}' to '{value}'")
                    self.data[row][col] = value
                else:
                    if not (0 <= row < len(self.data)):
                        print(f"  - Warning: Row index {row} out of bounds for change '{change}'. Skipping.")
                    else:
                        print(
                            f"  - Warning: Column index {col} out of bounds for row {row} in change '{change}'. Skipping.")
            except ValueError as e:
                print(f"  - Warning: Invalid change format '{change}'. Expected 'X,Y,value'. Error: {e}. Skipping.")
            except IndexError:
                print(f"  - Warning: Insufficient values in change '{change}'. Expected 'X,Y,value'. Skipping.")
            except Exception as e:
                print(f"  - An unexpected error occurred applying change '{change}': {e}. Skipping.")

    def _display_content(self, title):
        """Helper to display the 2D list content."""
        print(f"\n{title} content:")
        if not self.data:
            print("[Empty]")
            return
        for row in self.data:
            print(','.join(map(str, row)))

    def run(self):
        """Main execution flow for file modification."""
        if not self._check_source_file():
            return

        try:
            self._load_data()
        except FileNotFoundError:
            print(f"Error: Source file '{self.src_path}' not found during load.")
            return
        except PermissionError:
            print(f"Error: Permission denied when reading '{self.src_path}'.")
            return
        except Exception as e:
            print(f"Error loading data from '{self.src_path}': {e}")
            return

        self._display_content("Original")

        self._apply_changes()

        self._display_content("Modified")

        try:
            self._save_data()
            print(f"\nModified file saved to '{self.dst_path}'")
        except PermissionError:
            print(f"Error: Permission denied when writing to '{self.dst_path}'.")
        except Exception as e:
            print(f"Error saving modified file to '{self.dst_path}': {e}")


# --- Concrete CSV File Manager ---
class CsvFileManager(FileManager):
    def _load_data(self):
        """Loads CSV data into self.data."""
        try:
            with open(self.src_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                self.data = [row for row in reader]
        except UnicodeDecodeError:
            print(f"Error: UnicodeDecodeError when reading CSV. Check encoding for '{self.src_path}'.")
            raise
        except Exception as e:
            print(f"Error reading CSV file '{self.src_path}': {e}")
            raise

    def _save_data(self):
        """Saves self.data to CSV file."""
        try:
            with open(self.dst_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.data)
        except UnicodeEncodeError:
            print(f"Error: UnicodeEncodeError when writing CSV. Check encoding for '{self.dst_path}'.")
            raise
        except Exception as e:
            print(f"Error writing CSV file to '{self.dst_path}': {e}")
            raise


# --- Concrete JSON File Manager ---
class JsonFileManager(FileManager):
    def _load_data(self):
        """Loads JSON data into self.data (expects list of lists)."""
        try:
            with open(self.src_path, 'r', encoding='utf-8') as jsonfile:
                loaded_content = json.load(jsonfile)
                if isinstance(loaded_content, list) and all(isinstance(row, list) for row in loaded_content):
                    self.data = loaded_content
                else:
                    print("Warning: JSON file does not contain a list of lists. Initializing with empty data.")
                    self.data = []
        except json.JSONDecodeError:
            print(f"Error: JSONDecodeError when reading JSON. File '{self.src_path}' is not valid JSON.")
            raise
        except UnicodeDecodeError:
            print(f"Error: UnicodeDecodeError when reading JSON. Check encoding for '{self.src_path}'.")
            raise
        except Exception as e:
            print(f"Error reading JSON file '{self.src_path}': {e}")
            raise

    def _save_data(self):
        """Saves self.data to JSON file."""
        try:
            with open(self.dst_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(self.data, jsonfile, indent=4, ensure_ascii=False)
        except TypeError as e:
            print(f"Error: TypeError when writing JSON. Data contains non-serializable types: {e}")
            raise
        except UnicodeEncodeError:
            print(f"Error: UnicodeEncodeError when writing JSON. Check encoding for '{self.dst_path}'.")
            raise
        except Exception as e:
            print(f"Error writing JSON file to '{self.dst_path}': {e}")
            raise


# --- Main Program Logic ---

if len(sys.argv) < 4:
    print("Usage: reader.py <source_file> <destination_file> <change1> <change2> ...")
    sys.exit(1)

src_file = sys.argv[1]
dst_file = sys.argv[2]
changes = sys.argv[3:]


def get_file_manager_class(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        return CsvFileManager
    elif ext == '.json':
        return JsonFileManager
    else:
        raise ValueError(f"Unsupported file type for {filepath}. Supported types are .csv, .json.")


try:
    src_manager_class = get_file_manager_class(src_file)

    file_manager = src_manager_class(src_file, dst_file, changes)
    file_manager.run()

except ValueError as e:
    print(f"Configuration Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
