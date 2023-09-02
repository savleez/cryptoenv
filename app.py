from pathlib import Path
from typing import Union

from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


from cryptoenv import Encryptor


app = FastAPI()


class EncryptedFile(BaseModel):
    filename: str
    password: str
    content: str = None
    validated_filename: str = None
    encrypted_content: str = None

    def get_encryptor(self):
        return Encryptor(self.password)

    def validate_password(self):
        password = self.password

        if password is None or password == "":
            raise ValueError("Password must not be empty.")

    def validate_filename(self):
        filename = self.filename.strip()

        if not filename or filename == "":
            raise ValueError("Please enter a file name.")

        filename = str(Path(filename).with_suffix(".encrypted"))
        self.validated_filename = filename

    def encrypt_content(self):
        self.encrypted_content = self.get_encryptor().encryp_content(self.content)

    def decrypt_content(self):
        decrypted_content = self.get_encryptor().decrypt_content(self.encrypted_content)

        return decrypted_content


app.mount("/static", StaticFiles(directory="cryptoenv/web_gui/static"), name="static")
templates = Jinja2Templates(directory="cryptoenv/web_gui/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )


@app.post("/new_file")
async def generate_file(encrypted_file: EncryptedFile):
    try:
        encrypted_file.validate_filename()
        encrypted_file.validate_password()

        ## TODO: Define initial content
        encrypted_file.content = "Initial content"
        encrypted_file.encrypt_content()

        return {
            "filename": encrypted_file.validated_filename,
            "content": encrypted_file.encrypted_content,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/decrypt")
async def decrypt_file(encrypted_file: EncryptedFile):
    try:
        decrypted_content = encrypted_file.decrypt_content()

        return {
            "decrypted_content": decrypted_content,
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
