from tkinter import Tk, Event as TkEvent
from typing import Literal, Callable, Any
from typing import Self
from inspect import isclass

class ezTk(Tk):
    """
    ezTk 的 Docstring
    """
    def __init__(self, title: str = "Window"):
        super().__init__()

        self.wm_title(title)

        self._EventList_: list[str] = ["Run", "Exit"]
        self._CallbackFunc_: dict[str, list[Callable]] = {
            "Run": [],
            "Exit": []
        }

        self.UIInstance: Any | str | None = "NotInit"
        self.UIInit: Callable = lambda: None

        self.protocol("WM_DELETE_WINDOW", lambda: self.Exit("All"))
        self.EventCallback()

    def EventList(self, mode: Literal["add", "rmv", "show"] = "show", event: str = None):
        if mode == "show": return self._EventList_
        match mode:
            case "add": self._EventList_.append(event)
            case "rmv": self._EventList_.remove(event)

    def EventCallback(self, event: str = None, func: Callable = None):
        if event is None and not self._CallbackFunc_: self._CallbackFunc_: dict[str, list[Callable]] = {}
        if event in self._EventList_:
            if not event in self._CallbackFunc_: self._CallbackFunc_.update({event: []})
            self._CallbackFunc_[event].append(func)

    @property
    def Geometry(self):
        class _Geometry_():
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
        return _Geometry_(self)

    def Run(self):
        if self.UIInstance == "NotInit": self.UIInstance = self.UIInit(self)

        for func in self._CallbackFunc_["Run"]: func()
        self.mainloop()

    def Exit(self, event: TkEvent):
        for func in self._CallbackFunc_["Exit"]: func()
        self.quit()
        self.destroy()
        # sys_exit(0)

    def RunUIInit(self):
        self.UIInstance = self.UIInit(self)
        if self.UIInstance == "NotInit": raise RuntimeError("Incorrect return value: The return value of UIInit must not be 'NotInit'.")

    # def UIInit(master: Self, *args, **kwargs):
    #     pass # hook

if __name__ == "__main__":
    root: ezTk = ezTk("测试用例")

    def UIInit(self: ezTk):
        from tkinter import Label, Button, Entry

        zLabel = Label(self, text="标签")
        zLabel.pack()

        zButton = Button(self, text="标签")
        zButton.pack()

        zEntry = Entry(self)
        zEntry.pack()

    root.UIInit = UIInit

    root.Geometry.Size(800, 600)
    root.Run()