from EasyTk import ezTk
from tkinter import Tk, Frame
from abc import ABC, abstractmethod
from typing import Literal, Callable

class ezFrameManager(Frame): pass

class ezFrame(ABC):
    """Its Basically A Collection Of Widgets. 
    
    Args:
        master (str): The "master" Of This "Widget", Just Like Any Other Widget In Vanilla Tk.
        name (str): The Name Of ezFrame Instance.
        **kwargs: You Can Customize Other Attribute Here.
    """
    def __init__(self, master: ezFrameManager = None, name: str = "ezFrame", **kwargs: dict):
        self.master: ezFrameManager = master
        self.name: str = name
        self.kwargs: dict = kwargs

        self.Frame: Frame = None
        self.Plcae: Callable = lambda: None

    def __getattr__(self, name: str):
        if name in self.kwargs: return self.kwargs[name]

    @abstractmethod
    def UIInit(self):
        """
        You Need Implement This Method And Remember To Instantiate self.Frame In It.\n
        Alternatively, If You Want To Automate The Placement Of The Frame On A Form, You Can Implement The self.DoPlace Method.
        """
        pass # hook

    def DoPlace(self):
        pass # hook

    def draw(self):
        self.UIInit()
        self.DoPlace()

    def destroy(self):
        if self.Frame is None: return
        self.Frame.destroy()
        self.Frame = None

    def tkraise(self, aboveThis=None):
        self.Frame.tkraise(aboveThis)

class ezFrameManager(Frame):
    """You Could Enable/Disable/Switch For Different Frames With A Easy Way By Use It.

    Args:
        master (str): The "master" Of This "Widget", Just Like Any Other Widget In Vanilla Tk.
        **kwargs: You Can Customize Other Attribute Here.
    """
    SwitchModeList: list = ["tkraise", "redraw"]
    def __init__(self, master: Tk | ezTk, **kwargs: dict):
        super().__init__(master=master, **kwargs)

        self.master: Tk | ezTk = master
        self._SwitchMode_: Literal["tkraise", "redraw"] = "tkraise"
        self.kwargs: dict = kwargs
        
        self.Frames_NextIndex: int = 0
        self.Frames_IndexName: dict[int, str] = {}
        self.Frames_NameFrame: dict[str, ezFrame] = {}
        self.Frames_Persisted: list[str] = []
        self.Frame_Activated: str = None

        self.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def __getattr__(self, name: str):
        if name in self.kwargs: return self.kwargs[name]

    def __getitem__(self, key: int | str) -> ezFrame | None:
        if self.Frames_IndexName.__len__() == 0: return None

        if isinstance(key, int):
            if key == -1: key = list(self.Frames_IndexName)[-1]
            elif not key in self.Frames_IndexName: return None

            return self.Frames_NameFrame[self.Frames_IndexName[key]]
        else:
            if not key in self.Frames_NameFrame: return None

            return self.Frames_NameFrame[key]

    def AddFrame(self, frame: ezFrame):
        name = frame.name
        self.Frames_IndexName[self.Frames_NextIndex] = name
        self.Frames_NameFrame[name] = frame
        self.Frames_NextIndex += 1
        if self._SwitchMode_ == "tkraise" or name in self.Frames_Persisted: frame.draw()

    def Remove(self, key: int | str, even_persist: bool = False) -> tuple[bool, str]:
        if self.Frames_IndexName.__len__() == 0: return None

        index: int = 0
        name: str = ""
        if isinstance(key, int):
            if key == -1: key = list(self.Frames_IndexName)[-1]
            elif not key in self.Frames_IndexName: return None

            index = key
            name = self.Frames_IndexName[key]
        else:
            for _index_, _name_ in self.Frames_IndexName.items():
                if _name_ == key:
                    name = _name_
                    index = _index_
                    break
            else:
                return None

        if key in self.Frames_Persisted and not even_persist: return
            
        if name == self.Frame_Activated:
            self.Switch(FirstFrame:=self.Frames_IndexName[list(self.Frames_IndexName)[0]])
            self.Frame_Activated = FirstFrame

        self.Frames_NameFrame[name].destroy()
        self.Frames_NameFrame.pop(name)
        self.Frames_IndexName.pop(index)
        return name

    def Switch(self, key: str | int):
        if isinstance(key, int):
            if key == -1: key = list(self.Frames_IndexName)[-1]
            elif not key in self.Frames_IndexName: return
            key = self.Frames_IndexName[key]
        if not key in self.Frames_NameFrame: return

        NewFrame = self.Frames_NameFrame[key]
        if self._SwitchMode_ == "redraw":
            if not self.Frame_Activated is None and not self.Frame_Activated in self.Frames_Persisted: self.Frames_NameFrame[self.Frame_Activated].destroy()
            NewFrame.draw()
        else:
            NewFrame.tkraise()

        self.Frame_Activated = key

    def SwitchMode(self, mode: Literal["tkraise", "redraw"]):
        if not mode in self.SwitchModeList: return
        self._SwitchMode_ = mode

        match self._SwitchMode_:
            case "tkraise":
                for name, frame in self.Frames_NameFrame.items():
                    if frame.Frame is None: frame.draw()
                if self.Frame_Activated: self.Frames_NameFrame[self.Frame_Activated].tkraise()
            case "redraw":
                for name, frame in self.Frames_NameFrame.items():
                    if frame.Frame is None or frame.name == self.Frame_Activated or name in self.Frames_Persisted: continue
                    frame.destroy()
                if self.Frame_Activated: self.Frames_NameFrame[self.Frame_Activated].draw()

    def Refresh(self, doplace_only: bool = False):
        for name in self.Frames_Persisted:
            if (frame:=self.Frames_NameFrame[name]) is None:
                    frame.draw()
            elif doplace_only:
                frame.DoPlace()
            else:
                frame.destroy()
                frame.draw()
        self.update_idletasks()
        # print(self["frame_Home"].Pos, self["frame_Home"].Size)
        for name, frame in self.Frames_NameFrame.items():
            if name in self.Frames_Persisted: continue
            if not frame.Frame is None:
                if doplace_only:
                    frame.DoPlace()
                else:
                    frame.destroy()
                    frame.draw()

        if self._SwitchMode_ == "tkraise" and self.Frame_Activated: self.Frames_NameFrame[self.Frame_Activated].tkraise()
