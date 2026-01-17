from fastapi import FastAPI, UploadFile, File, HTTPException
from auth import create_token, verify_password
from users import USERS
from spleeter_service import separate_audio
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/login")
def login(username: str, password: str):
    user = USERS.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({"sub": username, "admin": user["is_admin"]})
    return {"access_token": token}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    separate_audio(path)
    return {"message": "Separação concluída"}
