from EasyTk import ezTk
from tkinter import Tk, Frame
from abc import ABC, abstractmethod
from typing import Literal, Callable

class ezFrame(ABC): pass
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

    def OtherHook(self):
        pass

    def draw(self):
        self.UIInit()
        self.DoPlace()
        self.OtherHook()

    def destroy(self):
        if self.Frame is None: return
        self.Frame.destroy()
        self.Frame = None

    def tkraise(self, aboveThis=None):
        self.Frame.tkraise(aboveThis)

class ezFrameList():
    def __init__(self):
        self.next_index: int = 0

        self.name_index: dict[str, int] = {}
        self.index_name: dict[int, str] = {}
        
        self.name_frame: dict[str, ezFrame] = {}

    def __call__(self, name: str):
        """_Get ezFrame Instance Directly By name Without Any Checking._"""
        return self.name_frame[name]

    def __iter__(self):
        for index in self.index_name:
            name = self.index_name[index]
            frame = self.name_frame[name]
            yield index, name, frame

    def __getitem__(self, key: str | int):
        """在 Index 索引下, 0 | 1 作为关键字保留, 用于指示 第一位序 | 最末位序 的帧.
        """
        match key:
            case 0:
                key: str = next(iter(self.name_index))
            case 1:
                key: str = next(reversed(self.name_index))
            case _:
                key: str = self.__getname__(key)
        if key is None:
            return key
        else:
            return self.name_frame[key]

    def __getindex__(self, key: int | str) -> None | int:
        if isinstance(key, str) and key in self.name_index:
            return self.name_index[key]
        elif isinstance(key, int) and key in self.index_name:
            return key
        else:
            return None

    def __getname__(self, key: int | str) -> None | str:
        if isinstance(key, str) and key in self.name_index:
            return key
        elif isinstance(key, int) and key in self.index_name:
            return self.index_name[key]
        else:
            return None

    def __getindex_name__(self, key: int | str):
        if isinstance(key, int) and key in self.index_name:
            return self.index_name[key], key
        elif isinstance(key, str) and key in self.name_index:
            return key, self.name_index[key]
        else:
            return None, None

    def append(self, frame: ezFrame) -> None:
        name: str = frame.name
        index: int = self.next_index if (_index := self.__getindex__(name)) is None else _index

        self.name_index[name] = index
        self.index_name[index] = name
        self.name_frame[name] = frame

        self.next_index += 1

    def pop(self, key: int | str):
        name, index = self.__getindex_name__(key)
        if name is None: return None

        self.index_name.pop(index)
        self.name_index.pop(name)

        return self.name_frame.pop(name)


class ezFrameManager(Frame):
    """You Could Enable/Disable/Switch For Different Frames With A Easy Way By Use It.

    Args:
        master (str): The "master" Of This "Widget", Just Like Any Other Widget In Vanilla Tk.
        **kwargs: You Can Customize Other Attribute Here.
    """
    def __init__(self, master: Tk | ezTk, **kwargs: dict):
        super().__init__(master=master, **kwargs)

        self.master: Tk | ezTk = master
        self._SwitchMode_: Literal["tkraise", "redraw"] = "tkraise"
        self.kwargs: dict = kwargs

        self.frames: ezFrameList = ezFrameList()

        self.frames_persisted: list[str] = []
        self.frame_activated: str = None

        self.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def __getattr__(self, name: str):
        if name in self.kwargs: return self.kwargs[name]

    def __getitem__(self, key: int | str) -> ezFrame | None:
        return self.frames[key]

    def AddFrame(self, frames: ezFrame | list[ezFrame], top_frame: str | int = None):
        if isinstance(frames, list):
            for frame in frames:
                self.frames.append(frame)
                if self._SwitchMode_ == "tkraise" or frame.name in self.frames_persisted:
                    frame.draw()
                    self.frame_activated = frame.name
        else:
            self.frames.append(frames)
            if self._SwitchMode_ == "tkraise" or frames.name in self.frames_persisted:
                frames.draw()
                self.frame_activated = frames.name

        if top_frame is None or (frame:=self.frames[top_frame]) is None: return
        match self._SwitchMode_:
            case "redraw":
                frame.draw()
                self.frame_activated = frame.name
            case "tkraise":
                frame.tkraise()
                self.frame_activated = frame.name

    def Remove(self, key: int | str, even_persisted: bool = False):
        name: str = self.frames.__getname__(key)
        if name is None: return

        # Persisted Check
        if name in self.frames_persisted and not even_persisted: return

        # Make Sure There Has Some Frame Been Activated
        if name == self.frame_activated:
            if self.frames_persisted:
                self.frame_activated = self.frames_persisted[0]
            else:
                self.Switch(name_firstframe:=list(self.frames)[0][2])
                self.frame_activated = name_firstframe

        self.frames.pop(name).destroy()

    def Switch(self, key: str | int):
        new_frame: ezFrame = self.frames[key]
        if new_frame is None: return

        match self._SwitchMode_:
            case "redraw":
                if not self.frame_activated in self.frames_persisted:
                    self.frames[self.frame_activated].destroy()
                if new_frame.name in self.frames_persisted:
                    new_frame.tkraise()
                else:
                    new_frame.draw()
            case "tkraise":
                new_frame.tkraise()

        self.frame_activated = new_frame.name

    def SwitchMode(self, mode: Literal["tkraise", "redraw"]):
        if not mode in ["tkraise", "redraw"]: return
        self._SwitchMode_ = mode

        match self._SwitchMode_:
            case "tkraise":
                frame_activated: ezFrame = None
                for index, name, frame in self.frames:
                    if name == self.frame_activated:
                        frame_activated = frame
                        continue
                    elif name in self.frames_persisted:
                        continue
                    frame.draw()
                if not frame_activated is None: frame_activated.tkraise()
            case "redraw":
                frame_activated: ezFrame = None
                for index, name, frame in self.frames:
                    if name == self.frame_activated:
                        frame_activated = frame
                        continue
                    elif name in self.frames_persisted:
                        continue
                    frame.destroy()

                if not frame_activated is None: frame_activated.draw()

    def Refresh(self, doplace_only: bool = False):
        for name in self.frames_persisted:
            frame: ezFrame = self.frames(name)
            if doplace_only:
                frame.DoPlace()
            else:
                frame.destroy()
                frame.draw()
        # self.update_idletasks()
        match self._SwitchMode_:
            case "redraw":
                if self.frame_activated is None:
                    return
                frame: ezFrame = self.frames(self.frame_activated)
                if doplace_only:
                    frame.DoPlace()
                else:
                    frame.destroy()
                    frame.draw()
            case "tkraise":
                for index, name, frame in self.frames:
                    if name in self.frames_persisted: continue
                    if doplace_only:
                        frame.DoPlace()
                    else:
                        frame.destroy()
                        frame.draw()
