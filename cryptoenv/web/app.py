from pathlib import Path
from json import dumps as json_dumps, loads as json_loads

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from cryptoenv.crypto.decryptor import Crypto
from cryptoenv.crypto.configuration import ConfigHandler
from cryptoenv.crypto.exceptions import (
    EncryptedFileDoesNotExist,
    ErrorDecryptingFile,
    ErrorEncryptingFile,
    EncryptedFileAlreadyExist,
)
from cryptoenv.web import STATIC_DIR, TEMPLATES_DIR
from cryptoenv.web.models import EncryptedFile, RequestData
from cryptoenv.web.file_handlers import get_config_template, validate_filename


app = FastAPI()


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )


@app.post("/open")
async def open_file(password_data: RequestData):
    # filename = ""

    # validate_filename()

    file = EncryptedFile(
        password=password_data.password,
    )

    try:
        decrypted_content = file.crypto.read_encrypted_file()

        decrypted_content_dict = json_loads(decrypted_content)

        config_handler = ConfigHandler(decrypted_content_dict)

    except EncryptedFileDoesNotExist as efdne_ex:
        code = 404
        error_data = {
            "message": str(efdne_ex),
            "slug": "file-does-not-exist",
        }

        return JSONResponse(
            content=error_data,
            status_code=code,
        )

    except ErrorDecryptingFile as edf_ex:
        code = 405
        error_data = {
            "message": str(edf_ex),
            "slug": "error-decrypting-file",
        }

        return JSONResponse(
            content=error_data,
            status_code=code,
        )

    except Exception as ex:
        return {"error": str(ex)}

    # serialized_config = config_handler.serialize_config()
    config_dict = config_handler.config_to_dict()

    return JSONResponse(
        content={
            "decrypted_content": config_dict,
        },
        status_code=200,
    )


@app.post("/new_file")
async def new_file(password_data: RequestData):
    file = EncryptedFile(
        password=password_data.password,
    )

    template_content = json_dumps(get_config_template())

    try:
        file.crypto.create_encrypted_file(content=template_content)

    except EncryptedFileAlreadyExist as efae_ex:
        code = 405
        error_data = {
            "message": str(efae_ex),
            "slug": "file-already-exists",
        }

        return JSONResponse(
            content=error_data,
            status_code=code,
        )

    return JSONResponse(
        content={
            "decrypted_content": template_content,
        },
        status_code=200,
    )


def runserver():
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)


def run_web_app():
    runserver()


# class EncryptedFile(BaseModel):
#     filename: str
#     password: str
#     content: str = None
#     validated_filename: str = None
#     encrypted_content: str = None

#     def get_encryptor(self):
#         return Encryptor(self.password)

#     def validate_password(self):
#         password = self.password

#         if password is None or password == "":
#             raise ValueError("Password must not be empty.")

#     def validate_filename(self):
#         filename = self.filename.strip()

#         if not filename or filename == "":
#             raise ValueError("Please enter a file name.")

#         filename = str(Path(filename).with_suffix(".encrypted"))
#         self.validated_filename = filename

#     def encrypt_content(self):
#         self.encrypted_content = self.get_encryptor().encryp_content(self.content)

#     def decrypt_content(self):
#         decrypted_content = self.get_encryptor().decrypt_content(self.encrypted_content)

#         return decrypted_content


# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse(
#         name="index.html",
#         context={"request": request},
#     )


# @app.post("/new_file")
# async def generate_file(encrypted_file: EncryptedFile):
#     global config_string

#     try:
#         encrypted_file.validate_filename()
#         encrypted_file.validate_password()

#         encrypted_file.content = config_string
#         encrypted_file.encrypt_content()

#         return {
#             "filename": encrypted_file.validated_filename,
#             "encrypted_content": encrypted_file.encrypted_content,
#         }

#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/decrypt")
# async def decrypt_file(encrypted_file: EncryptedFile):
#     try:
#         decrypted_content = encrypted_file.decrypt_content()

#         config_handler = DecryptedConfigHandler(decrypted_content)

#         serialized_config = config_handler.serialize_config()

#         return {
#             "decrypted_content": serialized_config,
#         }
#     except Exception as e:
#         return {"error": str(e)}


if __name__ == "__main__":
    runserver()
