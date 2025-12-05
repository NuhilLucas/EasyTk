from tkinter import Tk, Event as TkEvent
from typing import Literal, Callable, Any

class ezTk(Tk):
    """
    ezTk 的 Docstring
    """
    def __init__(self, title: str = "Window"):
        super().__init__()

        self.wm_title(title)

        self.protocol("WM_DELETE_WINDOW", lambda: self.Exit("All"))

        self.Geometry: ezTk_Geometry = ezTk_Geometry(self)

    def Run(self):
        self.mainloop()

    def Exit(self, event: TkEvent):
        self.quit()
        self.destroy()
        # sys_exit(0)

class ezTk_Geometry():
    def __init__(self, master: ezTk):
        self._master_: ezTk = master

    def Pos(self, x: int = None, y: int = None, update: bool = False):
        self._master_.wm_geometry(
            None if x==y==None else f"+{self._master_.winfo_x() if x is None else x}+{self._master_.winfo_y() if y is None else y}"
        )
        if update: self._master_.update_idletasks()
        return self._master_.winfo_x(), self._master_.winfo_y()

    def Size(self, width: bool = None, height: bool = None, update: bool = False):
        self._master_.wm_geometry(
            None if width==height==None else f"{self._master_.winfo_width() if width is None else width}x{self._master_.winfo_height() if height is None else height}"
        )
        if update: self._master_.update_idletasks()
        return self._master_.winfo_width(), self._master_.winfo_height()

    def SizeFix(self, width: bool = None, height: bool = None):
        return self._master_.wm_resizable(not width, not height)

    def SizeLimit(self, mode: Literal["min", "max"] = None, width: bool = None, height: bool = None):
        match mode:
            case "min":
                last = self._master_.wm_minsize()
                return self._master_.wm_minsize(last[0] if width is None else width, last[1] if height is None else height)
            case "max":
                last = self._master_.wm_maxsize()
                return self._master_.wm_maxsize(last[0] if width is None else width, last[1] if height is None else height)

if __name__ == "__main__":
    root: ezTk = ezTk("测试用例")

    from tkinter import Label, Button, Entry

    zLabel = Label(root, text="标签")
    zLabel.pack()

    zButton = Button(root, text="标签")
    zButton.pack()

    zEntry = Entry(root)
    zEntry.pack()

    root.Geometry.Size(800, 600)
    root.Run()