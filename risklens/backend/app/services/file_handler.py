import os
from pathlib import Path
import pandas as pd
from uuid import uuid4
from typing import Union
from metrics_extractor import parse_financial_highlights  # ✅ Import your parser

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
    file_extension = Path(original_filename).suffix
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as f:
        f.write(file_obj.read())

    return file_path


def read_excel(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Reads ONLY the 'Income Statement' sheet from an Excel file and returns it as a pandas DataFrame.
    """
    try:
        df = pd.read_excel(file_path, sheet_name="Income Statement")
        return df
    except ValueError:
        print("❌ 'Income Statement' sheet not found in file.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return pd.DataFrame()


def delete_file(file_path: Union[str, Path]) -> bool:
    """
    Deletes a file from disk.
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


def process_uploaded_file(file_obj, original_filename: str) -> dict:
    """
    Saves, reads, and extracts financial highlights from the 'Income Statement' sheet.
    Returns a dictionary of extracted metrics.
    """
    # Step 1: Save file
    file_path = save_file(file_obj, original_filename)

    # Step 2: Read the 'Income Statement' sheet
    df = read_excel(file_path)

    if df.empty:
        print("⚠️ No data found in 'Income Statement' sheet.")
        delete_file(file_path)
        return {}

    # Step 3: Extract metrics
    metrics = parse_financial_highlights(df)

    # Step 4: Delete file after processing (optional)
    delete_file(file_path)

    return metrics


# 🧪 Example usage (comment out in production)
if __name__ == "__main__":
    print("📂 Running file_handler test...")

    # Pretend we got an uploaded file
    with open("test.xlsx", "rb") as fake_file:
        extracted_data = process_uploaded_file(fake_file, "test.xlsx")
        print("📊 Extracted Metrics:", extracted_data)
