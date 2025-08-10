from fastapi import FastAPI, UploadFile, File
fr

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    metrics = process_uploaded_file(file.file, file.filename)
    return {"metrics": metrics}
