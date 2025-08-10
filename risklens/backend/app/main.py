# main.py
from fastapi import FastAPI, UploadFile, File
from risklens.backend.app.services.file_handler import process_uploaded_file
from risklens.backend.app.services.metrics_extractor import parse_income_statement

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Step 1: Process Excel into a dictionary of DataFrames
    df_dict = process_uploaded_file(file.file, file.filename)

    # Step 2: Extract metrics from the DataFrames
    metrics = parse_income_statement(df_dict)

    return {"metrics": metrics}
