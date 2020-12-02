from fastapi import FastAPI, Request
import subprocess
import uvicorn


app = FastAPI()


@app.put("/download/")
async def exec_download(request: Request):
    data = await request.body()
    file_name = data.decode()
    # file = open(f"C:/Users/Elad/shest_try/files/{file_name}", 'r').read()
    file = open(f"C:\\Users\\Elad\\shest_try\\files\\{file_name}", 'r').read()
    return file


@app.put("/upload/")
async def upload(request: Request):
    data = await request.body()
    data = data.decode('unicode_escape')
    data = data.split(",")
    file_name = data[0]
    data.pop(0)
    content = ",".join(data)

    # file = open(f"C:/Users/Elad/shest_try/files/{file_name}", 'w')
    file = open(f"C:\\Users\\Elad\\shest_try\\files/{file_name}", 'w')
    file.write(content)
    file.close()


@app.put("/regular/")
async def regular(request: Request):
    data = await request.body()
    command = data.decode().split(" ")
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = proc.communicate()
    return output


if __name__ == '__main__':
    uvicorn.run("main:app")
