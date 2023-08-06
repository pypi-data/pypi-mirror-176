from tkwinico.load import load_winico
from tkwinico.command import *
from tkwinico.con import *


if __name__ == '__main__':
    import tkinter as tk

    Window = tk.Tk()


    def CallBack(Message, X, Y):
        if Message == WM_RBUTTONDOWN:
            Menu = tk.Menu(tearoff=False)
            Menu.add_command(label="Quit", command=Window.quit)
            Menu.tk_popup(X, Y)


    taskbar(ADD, load(APPLICATION), (Window.register(CallBack), MESSAGE, X, Y))

    Window.mainloop()