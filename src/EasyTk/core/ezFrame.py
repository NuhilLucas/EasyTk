from EasyTk import ezTk
from tkinter import Tk, Frame as tkFrame
from abc import ABC, abstractmethod
from typing import Literal, Iterable, Any, Callable
from collections import deque

class ezFrame(tkFrame, ABC): pass
class ezFrameHub(tkFrame): pass

class ezFrame(tkFrame, ABC):
    """Its Basically A Collection Of Widgets. 
    
    Args:
        master (str): The "master" Of This "Widget", Just Like Any Other Widget In Vanilla Tk.
        name (str): The Name Of ezFrame Instance.
        **kwargs: You Can Customize Other Attribute Here.
    """

    def __init__(
            self,
            master: Tk | ezTk | ezFrameHub = None,
            name: str = "ezFrame",
            **kwargs: Any
    ):
        self.kwargs: dict[str, Any] = kwargs

        self.master: Tk | ezTk | ezFrameHub = master
        self.name: str = name

        self.drawed: bool = False

    @abstractmethod
    def _ui_init_(self):
        # hook
        pass

    def _bind_(self):
        # hook
        pass

    @abstractmethod
    def _do_place_(self):
        # hook
        pass

    def _other_hook_(self):
        # hook
        pass

    def draw(self) -> None:
        if self.drawed: return
        super().__init__(master=self.master, **self.kwargs)
        self._ui_init_()
        self._bind_()
        self._do_place_()
        self._other_hook_()
        self.drawed = True

    def destroy(self) -> None:
        if not self.drawed: return
        super().destroy()
        self.drawed = False

    def tkraise(self, aboveThis: Any | None = None) -> None:
        if not self.drawed: self.draw()
        super().tkraise(aboveThis)

class ezFrameRegistry():
    def __init__(self):
        self.FRAMES: dict[str, ezFrame] = dict()
        self.activated: str = None
        self.activated_history: deque[str] = deque(maxlen=10)
        self.persisted: set[str] = set()

    def __iter__(self):
        for name, frame in self.FRAMES.items():
            yield name, frame

    def __len__(self):
        return self.FRAMES.__len__()

    def __bool__(self):
        return bool(self.FRAMES)

    def __contains__(self, name: str) -> bool:
        return name in self.FRAMES

    def __getitem__(self, name: str) -> ezFrame:
        return self.FRAMES[name]

    def __setitem__(self, name: str, frame: ezFrame) -> None:
        if not name == frame.name: raise ValueError(f"name does not match the instance name attribute: name: {name}; frame.name: {frame.name}")
        self.add(frame=frame)

    def add(self, frame: ezFrame) -> None:
        if frame.name in self.FRAMES: raise Exception("Attempted to override an already-added frame instance.")
        self.FRAMES[frame.name] = frame

    def rep(self, old_frame: ezFrame | str, new_frame: ezFrame) -> ezFrame:
        name: str = old_frame if isinstance(old_frame, str) else old_frame.name
        old_frame = self.FRAMES[name]
        self.FRAMES[name] = new_frame
        return old_frame

    def pop(self, name: str) -> ezFrame:
        frame: ezFrame = self.FRAMES.pop(name)
        if name == self.activated: self.activated = None
        self.persisted.remove(name)
        return frame

    def persist(self, name: str) -> ezFrame:
        frame: ezFrame = self.FRAMES[name]
        self.persisted.add(name)
        return frame

    def unpersist(self, name: str):
        frame: ezFrame = self.FRAMES[name]
        self.persisted.discard(name)
        return frame

    def activate(self, name: str | None) -> None:
        if name is None: self.activated = name; return

        if not name in self.FRAMES: raise KeyError(name)

        self.activated_history.append(self.activated)

        self.activated = name

    def last_activated(self) -> str | None:
        while self.activated_history:
            frame_name: str = self.activated_history.pop()
            if frame_name in self.FRAMES: return frame_name
        else:
            return None

    def first_frame_name(self):
        return next(iter(self.FRAMES), None)

class ezFrameHub(tkFrame):
    """You Could Enable/Disable/Switch For Different Frames With A Easy Way By Use It.

    Args:
        master (str): The "master" Of This "Widget", Just Like Any Other Widget In Vanilla Tk.
        **kwargs: You Can Customize Other Attribute Here.
    """
    
    def __init__(
            self,
            master: Tk | ezTk = None,
            switch_mode: Literal["redraw", "tkraise"] = "tkraise",
            **kwargs: Any
    ):
        super().__init__(master=master, **kwargs)

        self.kwargs: dict = kwargs

        self.master: Tk | ezTk = master

        self.frame_reg: ezFrameRegistry = ezFrameRegistry()

        self.switch_types: set[Literal["redraw", "tkraise"]] = {"tkraise", "redraw"}
        self.switch_mode: Literal["redraw", "tkraise"] = switch_mode if switch_mode in self.switch_types else "tkraise"

        self._ui_init_()
        self._bind_()

    def __contains__(self, name: str):
        return name in self.frame_reg

    def __getitem__(self, name: str) -> ezFrame | None:
        return self.frame_reg[name]

    def _ui_init_(self):
        self.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def _bind_(self):
        pass

    def configure(
            self,
            switch_mode: Literal["redraw", "tkraise"] = None,
            cnf = None,
            **kwargs
    ):
        match switch_mode, switch_mode==self.switch_mode:
            case "redraw", False:
                for name, frame in self.frame_reg:
                    if (
                        (name == self.frame_reg.activated) or
                        (name in self.frame_reg.persisted) or
                        (not frame.drawed)
                    ): continue
                    frame.destroy()
                self.switch_mode = switch_mode
            case "tkraise", False:
                for name, frame in self.frame_reg:
                    if (
                        (name == self.frame_reg.activated or name in self.frame_reg.persisted) and
                        (not frame.drawed)
                    ): continue
                    frame.draw()
                self.frame_reg[self.frame_reg.activated].tkraise()
                self.switch_mode = switch_mode

        return super().configure(cnf=cnf, **kwargs)

    def switch(self, name: str, command: Callable = lambda frame: None):
        if not name in self.frame_reg or name == self.frame_reg.activated: return

        new_frame: ezFrame = self.frame_reg[name]

        match self.switch_mode:
            case "redraw":
                if not self.frame_reg.activated in self.frame_reg.persisted: self.frame_reg[self.frame_reg.activated].destroy()
                if new_frame.name in self.frame_reg.persisted: new_frame.tkraise()
                else: new_frame.draw()
            case "tkraise":
                new_frame.tkraise()

        command(new_frame)

        self.frame_reg.activate(name)

    def add_frame(self, frames: ezFrame | Iterable[ezFrame], top_frame: str = None):
        frames: Iterable[ezFrame] = (frames,) if isinstance(frames, ezFrame) else frames

        is_tkraise: bool = (self.switch_mode == "tkraise")
        for frame in frames:
            self.frame_reg.add(frame)
            if is_tkraise: frame.draw()

        top_frame: str = (top_frame if top_frame in self.frame_reg else None) or (self.frame_reg.activated) or (self.frame_reg.first_frame_name())
        if top_frame is None: return
        match self.switch_mode:
            case "redraw":
                self.frame_reg[top_frame].draw()
            case "tkraise":
                self.frame_reg[top_frame].tkraise()
        self.frame_reg.activate(top_frame)

    def rem_frame(self, name: str, even_persisted: bool = False):
        if (
            (not name in self.frame_reg) or
            (name in self.frame_reg.persisted and not even_persisted)
        ): return

        self.frame_reg.pop(name).destroy()

        frame_name_to_activate: str = self.frame_reg.last_activated() or self.frame_reg.first_frame_name()
        if not frame_name_to_activate is None:
            match self.switch_mode:
                case "redraw":
                    self.frame_reg[frame_name_to_activate].draw()
                case "tkraise":
                    self.frame_reg[frame_name_to_activate].tkraise()

        self.frame_reg.activate(frame_name_to_activate)

    def persist_frame(self, frames: str | Iterable[str]):
        frames_name: Iterable[str] = (frames,) if isinstance(frames, str) else frames
        
        is_redraw: bool = (self.switch_mode == "redraw")
        for frame_name in frames_name:
            if not frame_name in self.frame_reg: continue
            if is_redraw: self.frame_reg.persist(frame_name).draw()

        if not is_redraw: return
        self.frame_reg[self.frame_reg.activated].tkraise()

    def unpersist_frame(self, frames: str | Iterable[str]):
        frames_name: Iterable[str] = (frames,) if isinstance(frames, str) else frames
        
        is_redraw: bool = (self.switch_mode == "redraw")
        for frame_name in frames_name:
            if not frame_name in self.frame_reg: continue
            if is_redraw and not self.frame_reg.activated == frame_name: self.frame_reg.unpersist(frame_name).destroy()

if __name__ == "__main__":
    from EasyTk import ezTk

    root: ezTk = ezTk("Test")
    root.Geometry.Size(400, 300)

