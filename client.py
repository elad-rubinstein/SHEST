"""
Implement a tkinter client who communicates with a fastapi server
and executes commands
"""

import requests
from threading import Thread
import tkinter


root = tkinter.Tk()
frame = tkinter.Frame(root)
command_inp = tkinter.Text(frame, width=70, height=1, fg="green")


def retrieve_input():
    """
    Get a command input from the user and get the output to the command
    from a fastapi server
    """

    command = command_inp.get("1.0", "end-1c").split(" ")
    if command[0] == 'download':
        file = command[1].split("\\")[-1]
        response = requests.put(f'http://127.0.0.1:8000/download/', data=file)
        f = open(command[1], 'w')
        f.write(eval(response.content.decode()))
        f.close()

        for widget in frame.winfo_children():
            widget.destroy()
        output = tkinter.Label(frame, text=f"{file} has been downloaded from"
                                           f" the server!")
        output.grid(row=0, column=0)
        root.update()

    elif command[0] == "upload":
        file = command[1].split("\\")[-1]
        content = open(command[1], 'r').read()
        requests.put(f'http://127.0.0.1:8000/upload/',
                     data=f"{file},{content}")

        for widget in frame.winfo_children():
            widget.destroy()
        output = tkinter.Label(frame, text=f"{file}"
                                           f" has been uploaded to the server!")
        output.grid(row=0, column=0)
        root.update()

    else:
        response = requests.put('http://127.0.0.1:8000/regular/',
                                data=" ".join(command))
        response = response.content.decode('unicode_escape')

        for widget in frame.winfo_children():
            widget.destroy()
        output = tkinter.Label(frame, text=f"output:\n{response}")
        output.grid(row=0, column=0)
        root.update()


def run():
    """
    Make the necessary changes to the tkinter root
    """

    frame.grid(row=0, column=0)
    title = tkinter.Label(frame, text="Hy there! Please type a command and I "
                                      "will execute it for for you:\nupload: "
                                      "upload <path>\ndownload: download <path>"
                          , font=(None, 15))
    title.grid(row=0, column=0)
    space1 = tkinter.Label(frame, text="\n")
    space1.grid(row=1, column=0)
    command_inp.grid(row=2, column=0)
    confirm = tkinter.Button(frame, text="confirm",
                             command=lambda: retrieve_input())
    confirm.grid(row=2, column=1)
    space2 = tkinter.Label(frame, text="\n")
    space2.grid(row=3, column=0)
    root.update()


def main():
    """
    Run the tkinter root and call in a thread to make changes to it
    """

    Thread(target=run).start()
    root.mainloop()


if __name__ == '__main__':
    main()
