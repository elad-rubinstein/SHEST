""" SHEST FASTAPI SERVER """

from cryptography.fernet import Fernet
from fastapi import FastAPI, Request
from os import popen
from uvicorn import run
from fastapi.responses import StreamingResponse


app = FastAPI()


def load_key():
    """Load the previously generated key"""

    with open('secret.key', 'r') as file:
        return file.read()


def encrypt_message(message: str):
    """
    Encrypts a message"
    :param message: A regular message.
    :return: The encrypted message.
    """

    key = load_key()
    f = Fernet(key)
    message = message.encode()
    encrypted_message = f.encrypt(message)
    return encrypted_message


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    :param encrypted_message: The encrypted message to decrypt.
    :return: The decrypted message.
    """

    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


async def stream_back(file_name: str):
    """
    Yield file content in chunks
    :param file_name: A file name.
    :return: Chunks of a file.
    """

    with open(f"C:\\Users\\Elad\\PycharmProjects\\SHEST\\"
              f"files\\{file_name}", 'r') as file:
        for chunk in file:
            yield encrypt_message(chunk)


@app.put("/download/")
async def exec_download(request: Request):
    """
    Configure a path for download commands
    :param request: An encrypted download request containing a file_name.
    :return: An encrypted streaming response of a file content in chunks.
    """

    data = await request.body()
    file_name = decrypt_message(data).decode()
    return StreamingResponse(stream_back(file_name))


@app.put("/upload/{file_name}")
async def upload(request: Request, file_name: str, mode='a'):
    """
    Configure a path for upload commands
    :param request: An encrypted upload command.
    :param file_name: A file name given in the path.
    :param mode: The mode of the file: append or rewrite.
    """

    data = await request.body()
    with open(f"C:\\Users\\Elad\\PycharmProjects\\SHEST\\files\\{file_name}",
              mode) as file:
        file.write(decrypt_message(data).decode())


@app.put("/regular/")
async def regular(request: Request):
    """
    Configure a path for regular commands
    :param request: An encrypted command.
    :return: An encrypted output for the given command.
    """

    data = await request.body()
    command = decrypt_message(data).decode()
    output = popen(command).read()
    return encrypt_message(output)


if __name__ == '__main__':
    run("main:app")
