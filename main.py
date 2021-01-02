""" Shest (Shell Over REST) Api Server """

from os import popen
from pathlib import Path

from cryptography.fernet import Fernet
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from uvicorn import run

app = FastAPI()


def encrypt_message(message: str) -> bytes:
    """
    Encrypt a message

    :param message: A regular message.
    :return: The encrypted message.
    """

    f = Fernet("BccKLSpQGIdcP5CYpEQ-nPEQhMuNmFMguTkf7gyyIf0=")
    message = message.encode()
    encrypted_message = f.encrypt(message)
    return encrypted_message


def decrypt_message(encrypted_message: bytes) -> str:
    """
    Decrypt an encrypted message

    :param encrypted_message: The encrypted message to decrypt.
    :return: The decrypted message.
    """

    f = Fernet("BccKLSpQGIdcP5CYpEQ-nPEQhMuNmFMguTkf7gyyIf0=")
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message


async def read_file(file_name: str) -> bytes:
    """
    Yield file content in chunks

    :param file_name: A file name.
    :return: Chunks of a file.
    """

    with Path.cwd().joinpath(f'files\\{file_name}').open(mode='r') as file:
        for chunk in file:
            yield encrypt_message(chunk)


@app.put("/download/")
async def exec_download(request: Request) -> StreamingResponse:
    """
    Stream back the requested file's content

    :param request: An encrypted download request containing a file_name.
    :return: An encrypted streaming response of a file content in chunks.
    """

    data = await request.body()
    file_name = decrypt_message(data).decode()
    return StreamingResponse(read_file(file_name))


@app.put("/upload/{file_name}")
async def exec_upload(request: Request, file_name: str, mode: str):
    """
    Write a given chunk of a file content into a file in a specific location

    :param request: An encrypted upload command.
    :param file_name: A file name given in the path.
    :param mode: The mode of the file: append or rewrite.
    """

    data = await request.body()
    with Path.cwd().joinpath(f'files\\{file_name}').open(mode=mode) as file:
        file.write(decrypt_message(data).decode())


@app.put("/regular/")
async def run_regular_command(request: Request) -> bytes:
    """
    Run a command and response it's output

    :param request: An encrypted command.
    :return: An encrypted output for the given command.
    """

    data = await request.body()
    command = decrypt_message(data).decode()
    output = popen(command).read()
    return encrypt_message(output)


if __name__ == '__main__':
    run("main:app")
