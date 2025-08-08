import os
from pathlib import Path
import pandas as pd
from uuid import uuid4
from typing import Union

# Where uploaded files will be stored
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(file_obj, original_filename: str) -> Path:
    """
    Saves an uploaded file to disk with a unique name to avoid overwriting.

    Args:
        file_obj: The file object (e.g., from UploadFile.file)
        original_filename: Name of the uploaded file from user

    Returns:
        Path to the saved file
    """
    # ✅ Step 1: Create a safe filename (UUID prevents duplicates)
    file_extension = Path(original_filename).suffix
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # ✅ Step 2: Save file to disk
    with open(file_path, "wb") as f:
        f.write(file_obj.read())

    return file_path


def read_excel(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Reads an Excel file and returns it as a pandas DataFrame.

    Args:
        file_path: Path to the Excel file

    Returns:
        Pandas DataFrame containing the file data
    """
    try:
        df = pd.read_excel(file_path)  # 🔹 You can add sheet_name= if needed
        return df
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return pd.DataFrame()


def delete_file(file_path: Union[str, Path]) -> bool:
    """
    Deletes a file from disk.

    Args:
        file_path: Path to the file

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        os.remove(file_path)
        return True
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Error deleting file: {e}")
        return False


# 🧪 Example usage (comment out in production)
if __name__ == "__main__":
    # Pretend we got an uploaded file
    print("📂 Running file_handler test...")

    # Example: Save → Read → Delete
    fake_file = open("test.xlsx", "rb")  # Replace with your test file
    saved_path = save_file(fake_file, "test.xlsx")
    print(f"✅ Saved to: {saved_path}")

    data = read_excel(saved_path)
    print(f"📊 Data preview:\n{data.head()}")

    if delete_file(saved_path):
        print("🗑️ File deleted.")
