from fastapi import FastAPI, UploadFile, File
import subprocess
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "Spleeter backend running"}

@app.post("/separate")
async def separate_audio(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    output_path = f"{OUTPUT_DIR}/{file_id}"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "spleeter",
        "separate",
        "-p", "spleeter:5stems",
        "-o", OUTPUT_DIR,
        input_path
    ], check=True)

    return {
        "message": "Audio separado com sucesso",
        "output_folder": output_path
    }
