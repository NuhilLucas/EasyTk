
from tkinter import Widget as tk_Widget, Frame as tk_Frame, Label as tk_Label, Entry as tk_Entry, Button as tk_Button, Canvas as tk_Canvas
from tkinter import Tk, PhotoImage, Event
from tkinter.font import Font

from PIL import Image as PILImage, ImageTk as PILImageTk
from typing import Literal, Callable

from sys import exit as SysExit
from os.path import exists as FileExists

from ctypes import windll

# from EasyTk._WinStyles import WinStyles, WinStates, ResetWinStyle

WINDLLU32 = windll.user32

import logging

LogPrint = print

# --------------------------------------------------

class EasyTk(Tk):
    def __init__(self): self.RootType: str; self.Type: str
class Widget():
    def __init__(self): self.RootType: str; self.Type: str
class Label(Widget, tk_Label): pass
class Button(Widget, tk_Button): pass

# --------------------------------------------------

class Content():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Text(self, text: str = None):
        match self.Master.Type:
            case "EasyTk":
                if text == None:
                    return self.Master.title("")
                else:
                    self.Master.wm_title(text)
            case "Label":
                if text == None:
                    return self.Master.cget("text")
                else:
                    self.Master.configure(text=text)
            case "Button":
                if text == None:
                    return self.Master.cget("text")
                else:
                    self.Master.configure(text=text)

    def Title(self, title: str | None = None):
        match self.Master.Type:
            case "EasyTk":
                if title == None:
                    return self.Master.title() if self.Master.TitleBar == None else self.Master.TitleBar.TitleText.cget("text")
                else:
                    self.Master.wm_title(title)
                    if self.Master.TitleBar != None:
                        self.Master.TitleBar.TitleText.configure(text=title)
                        self.Master.update_idletasks()

    def Image(
            self,
            path: str,
            scale: Literal["Cut", "Fill", "Ratio", "Stretch"] | None = None,

            ratio: float = 1.00,
            width: int = None,
            height: int = None
    ):
        if not FileExists(path): return

        Img = PILImage.open(path)
        if any((scale == None, width==None, height==None)) != True or scale == "Ratio":
            SizeW, SizeH = Img.width, Img.height
            match scale:
                case "Cut":
                    Img.resize((width, height))
                case "Fill":
                    WHRatio_Target: float = width / height
                    WHRatio_Image: float = SizeW / SizeH
                    if WHRatio_Target > WHRatio_Image:
                        if WHRatio_Image > 1:
                            ratio = width / SizeW
                        else:
                            ratio = height / SizeH
                    else:
                        if WHRatio_Image > 1:
                            ratio = height / SizeH
                        else:
                            ratio = width / SizeW
                    Img = Img.resize((int(SizeW * ratio), int(SizeH * ratio)), PILImage.LANCZOS)
                    # Img = Img.resize((10, 10), PILImage.LANCZOS)
                case "Ratio":
                    Img = Img.resize((int(SizeW * ratio), int(SizeH * ratio)), PILImage.LANCZOS)
                case "Stretch":
                    pass
                case _: return

        Img = PILImageTk.PhotoImage(Img)

        match self.Master.Type:
            case "EasyTk":
                pass
            case "Label":
                self.Master.configure(image=Img)

class Style():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Geometry(self, width: int = None, height: int = None) -> tuple:
        match self.Master.Type:
            case "EasyTk":
                width = self.Master.winfo_width() if width == None else width
                height = self.Master.winfo_height() if height == None else height
                self.Master.wm_geometry(f"{width}x{height}")
                return (width, height)
            case "Frame":
                geometry = {}
                if width  != None: geometry['width']  = width
                if height != None: geometry['height'] = height
                self.Master.configure(**geometry)
    
    def SizeLimit(self, mode: Literal["MAX", "MIN", "ALL"] = None, size: tuple | None = None) -> tuple:
        match self.Master.Type:
            case "EasyTk":
                if mode == "MAX":
                    return self.Master.wm_maxsize(*size) if size != None else self.Master.wm_maxsize()
                if mode == "MIN":
                    return self.Master.wm_minsize(*size) if size != None else self.Master.wm_minsize()

    def SizeFix(self, mode: Literal["Execute", "Cancel"] = "Execute") -> None:
        match self.Master.Type:
            case "EasyTk":
                def __SizeFix():
                    if self.Master.winfo_viewable() == 0: self.Master.after(50, __SizeFix); return
                    Size: tuple = (self.Master.winfo_width(), self.Master.winfo_height())
                    if mode == "Execute": self.Master.wm_maxsize(*Size); self.Master.wm_minsize(*Size)
                    elif mode == "Cancel": self.Master.wm_maxsize(self.Master.winfo_screenwidth(), self.Master.winfo_screenheight()); self.Master.wm_minsize(0, 0)
                __SizeFix()

    def Font(
            self,
            font: str | Font,
            size: int = ...,
            style: tuple | Literal["bold", "italic", "underline", "overstrike"] = ()
    ):
        if isinstance(font, str) and size: font = (font, size, *style) if isinstance(style, tuple) else (font, size, style)
        match self.Master.Type:
            case "EasyTk":
                pass
            case "Label":
                self.Master.configure(font=font)
            case "Button":
                self.Master.configure(font=font)

    def Foreground(self, color: str):
        match self.Master.RootType:
            case "EasyTk":
                self.Master.configure(foreground=color)
            case "Widget":
                self.Master.configure(foreground=color)

    def Background(self, color: str):
        match self.Master.RootType:
            case "EasyTk":
                self.Master.configure(bg=color)
            case "Widget":
                self.Master.configure(bg=color)

    def Alignment(self, anchor: Literal["center", "n", "s", "w", "e", "nw", "ne", "sw", "se"]):
        match self.Master.Type:
            case "Label":
                self.Master.configure(anchor=anchor)

class Behavior():
    def __init__(self, master: EasyTk | Widget | Button = None):
        self.Master = master

    def Bind(self):
        match self.Master.Type:
            case "Button":
                return self.Master.bind

    def After(self, ms: int | None = None, func: Callable = None, *args) -> int | None:
        if (ms, func) == (None, None): return 
        match self.Master.Type:
            case 'EasyTk':
                return self.Master.after_idle(func, *args) if ms in (None, 0) else self.Master.after(ms, func, *args)

    def AfterCancel(self, id: int) -> None:
        match self.Master.Type:
            case 'EasyTk':
                return self.Master.after_cancel(id)

    def MaxedSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_MAXIMIZE)

    def MinedSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_MINIMIZE)
    
    def RestoredSize(self):
        match self.Master.Type:
            case 'EasyTk':
                WINDLLU32.ShowWindow(self.Master.HWND, WinStates.SW_RESTORE)

class Layout():
    def __init__(self, master: EasyTk | Widget = None):
        self.Master = master
    
    def Pack(
            self,
            anchor: Literal["center", "n", "s", "w", "e", "nw", "ne", "sw", "se"] = ...,
            expand: bool = ...,
            fill: Literal['none', 'x', 'y', 'both'] = ...,
            side: Literal['left', 'right', 'top', 'bottom'] = ...,
            ipadx: int = ...,
            ipady: int = ...,
            padx: int = ...,
            pady: int = ...,
            **kwargs
    ):
        _kwargs: dict = {Key: Value for Key, Value in locals().items() if Key not in ("self", "args", "kwargs") and Value is not ...}; _kwargs.update(kwargs)
        self.Master.pack_configure(**_kwargs)

    def Place(
            self,
            bordermode: Literal['inside', 'outside', 'ignore'] = ...,
            width: int = ...,
            height: int = ...,
            x: int = ...,
            y: int = ...,
            relheight: str | float = ...,
            relwidth: str | float = ...,
            relx: str | float = ...,
            rely: str | float = ...,
            **kwargs
    ):
        _kwargs: dict = {Key: Value for Key, Value in locals().items() if Key not in ("self", "args", "kwargs") and Value is not ...}; _kwargs.update(kwargs)
        self.Master.place_configure(**_kwargs)

class Configure():
    def __init__(self, master: EasyTk | Widget = None):
        self.Master = master
    
    def Configure(self, cnf=None, **kw):
        return self.Master.configure(cnf, **kw)

# --------------------------------------------------

class Widget():
    def __init__(self, master = None, *args, **kwargs):
        self.Master: EasyTk | Widget = master
        self.RootType: str = "Widget"
        self.Type: str = "Widget"

    def _Configure(self, cnf=None, **kw):
        return self.Master.configure(cnf, kw)

    Configure = _Configure

class Frame(Widget, tk_Frame):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Frame.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Frame"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Label(Widget, tk_Label):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Label.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Label"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Button(Widget, tk_Button):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Button.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Button"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

class Canvas(Widget, tk_Canvas):
    def __init__(self, master = None, *args, **kwargs):
        Widget.__init__(self, master=master)
        tk_Canvas.__init__(self, master=master, *args, **kwargs)

        self.Type: str = "Canvas"

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)

    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Layout(self) -> Layout:
        return Layout(self)

# --------------------------------------------------

class TitleBar(Widget):
    def __init__(self, master: EasyTk, DPIScale: float = 1.00, ResizeEdgePx: int = 5, bg:str = "#2c3e50", height: int = 45, *args, **kwargs):
        Widget.__init__(self, master=master)

        self.Master: EasyTk = master
        for zWidget in self.Master.winfo_children(): zWidget.destroy()

        self.DPIScale: float = DPIScale

        self.Resources: dict[str] = {
            "TitleIcon": r"C:\Users\Lucas\Desktop\星星.png"
        }

        self.ResizeArgs: dict = {
            "InResizeZone": False,
            "EdgePx": ResizeEdgePx,
            "Type": None,
            "WinSizeW": None,
            "WinSizeH": None,
            "CursorX": None,
            "CursorY": None,
        }

        self.DragArgs: dict = {
            "DragStarted": False,
            "WinPosX": None,
            "WinPosY": None,
            "CursorX": None,
            "CursorY": None,
            "RelativeX": None,
            "RelativeY": None,
        }

        self.SetStyle(bg, height)
        self.InitUI()
        self.InitWidgetInfo()
        self.UIConfig()
        self.UILayout()
        self.BindEvents()
        self.BindResizeZones()

    def SetStyle(self, bg: str, height: int):
        self.SIZE_Mainheight: int = int(height * self.DPIScale)
        self.SIZE_Btnheight: int = int(2 * self.DPIScale)

        self.COLOR_MainBackground: str = bg
        self.COLOR_BtnBackground: str = "#4F4F4F"

    def InitUI(self):
        self.TitleBar: Frame = Frame(self.Master)
        self.TitleIcon: Label = Label(self.TitleBar)
        self.TitleText: Label = Label(self.TitleBar)
        self.TitleBtns: Frame = Frame(self.TitleBar)

        self.TitleBtn_Min: Button = Button(self.TitleBtns)
        self.TitleBtn_Max: Button = Button(self.TitleBtns)
        self.TitleBtn_Ext: Button = Button(self.TitleBtns)

        self.LayoutedMark: Frame = Frame(self.TitleBar)

    def InitWidgetInfo(self):
        self.TitleWidgets: dict[int, dict[str, Button | Frame | Label, str]] = {
            1: {
                "Name": "TitleBar",
                "Widget": self.TitleBar,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            2: {
                "Name": "TitleIcon",
                "Widget": self.TitleIcon,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            3: {
                "Name": "TitleText",
                "Widget": self.TitleText,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            4: {
                "Name": "TitleBtns",
                "Widget": self.TitleBtns,
                "Bind": [("<Button-1>", self.Drag_Press), ("<B1-Motion>", self.Drag_Move), ("<ButtonRelease-1>", self.Drag_Release), ("<Double-Button-1>", self.DBClick_Maximize)]
            },
            5: {
                "Name": "TitleBtn_Min",
                "Widget": self.TitleBtn_Min,
                "Icon_Default": "━",
                "Bind": [("<ButtonRelease-1>", self.Btn_Minimize)]
            },
            6: {
                "Name": "TitleBtn_Max",
                "Widget": self.TitleBtn_Max,
                "Icon_Default": "❐",
                "Bind": [("<ButtonRelease-1>", self.Btn_Maximize)]
            },
            7: {
                "Name": 'TitleBtn_Ext',
                "Widget": self.TitleBtn_Ext,
                "Icon_Default": "✖",
                "Bind": [("<ButtonRelease-1>", self.Btn_Exit)]
            }
        }

    def UIConfig(self): 
        self.TitleBar.Style.Background(self.COLOR_MainBackground)
        self.TitleBar.Style.Geometry(height=self.SIZE_Mainheight)

        self.TitleIcon.Style.Background(self.TitleBar["bg"])
        self.TitleIcon.Content.Image(self.Resources["TitleIcon"], scale="Fill", width=30, height=30)

        self.TitleText.Style.Foreground("#FFFFFF")
        self.TitleText.Style.Background(self.TitleBar["bg"])
        self.TitleText.Style.Font("Arial", 13)
        self.TitleText.Style.Alignment("w")
        self.TitleText.Content.Text(self.Master.title())

        self.TitleBtns.Style.Background(self.TitleBar["bg"])

        for TitleBtnIndex in self.TitleWidgets:
            if self.TitleWidgets[TitleBtnIndex]["Widget"].Type != "Button": continue
            TitleBtn: Button = self.TitleWidgets[TitleBtnIndex]["Widget"]
            Icon: str = self.TitleWidgets[TitleBtnIndex]["Icon_Default"]

            TitleBtn.Style.Font("Arial", 13)
            TitleBtn.Content.Text(Icon)

        self.LayoutedMark.Style.Geometry(0, 0)

    def UILayout(self):
        self.TitleBar.Layout.Place(x=0, y=0, relwidth=1.0, height=self.SIZE_Mainheight, bordermode="inside")

        self.TitleIcon.Layout.Pack(anchor="center", side="left")
        self.TitleText.Layout.Pack(anchor="center", side="left")

        self.TitleBtns.Layout.Pack(anchor="center", side="right")

        for TitleBtnIndex in self.TitleWidgets:
            if self.TitleWidgets[TitleBtnIndex]["Widget"].Type != "Button": continue
            self.TitleWidgets[TitleBtnIndex]["Widget"].Layout.Pack(anchor="center", side="left", padx=(0, 5))

        self.LayoutedMark.Layout.Place(x=0, y=0)

    # ----------
    def BindEvents(self):
        for TitleBtnIndex in self.TitleWidgets:
            zWidget = self.TitleWidgets[TitleBtnIndex]["Widget"]
            zBindConfigs: list[str] = self.TitleWidgets[TitleBtnIndex]["Bind"]
            for zEvent, zFunc in zBindConfigs: zWidget.bind(zEvent, zFunc)

        def LayoutedMarkFunc(event: Event):
            self.Master.Style.SizeLimit(
                "MIN",
                size=(self.TitleIcon.winfo_width() + self.TitleText.winfo_width() + self.TitleBtns.winfo_width() + 5, 0)
            )
            self.LayoutedMark.unbind("<Map>")
            self.LayoutedMark.destroy()
        self.LayoutedMark.bind( "<Map>", LayoutedMarkFunc)
    # ----------
    def Drag_Press(self, event: Event):
        # 校验
        if self.Master.Maximized["Cooldown"]: return # 确保不处于最大化冷却期

        self.DragArgs["WinPosX"], self.DragArgs["WinPosY"] = self.Master.winfo_x(), self.Master.winfo_y()
        self.DragArgs["CursorX"], self.DragArgs["CursorY"] = event.x_root, event.y_root
        self.DragArgs["RelativeX"], self.DragArgs["RelativeY"] = self.DragArgs["CursorX"] - self.DragArgs["WinPosX"], self.DragArgs["CursorY"] - self.DragArgs["WinPosY"]
        
        self.DragArgs["DragStarted"] = True

    def Drag_Move(self, event: Event):
        # 校验
        if self.Master.Maximized["Cooldown"]: return # 确保不处于最大化冷却期
        if not self.DragArgs["DragStarted"]: return # 确保处于拖拽开始状态

        if self.Master.Maximized["State"]:
            WinPosSize: list[str] = self.Master.Maximized["Pos"].split('+')
            SizeW = int(WinPosSize[0].split("x")[0])
            PosX, PosY = (int(Pos) for Pos in WinPosSize[1:])
            
            if SizeW + PosX <= self.DragArgs["CursorX"]:
                PosX = event.x_root - SizeW*event.x//self.Master.winfo_width()
            else:
                PosX = event.x_root - SizeW//2
            PosY = event.y_root-self.SIZE_Mainheight//2
            PosY = PosY if PosY > 0 else 0
            self.DragArgs["RelativeX"] = event.x_root - PosX
            self.DragArgs["RelativeY"] = event.y_root - PosY

            self.Btn_Maximize()

            self.Master.Maximized["State"] = False
        else:
            PosX, PosY = (int(Pos) for Pos in self.Master.geometry().split("+")[1:])
            NewX = event.x_root - self.DragArgs["RelativeX"]
            NewY = event.y_root - self.DragArgs["RelativeY"]
            self.Master.geometry(f"+{NewX}+{NewY}")

    def Drag_Release(self, event: Event):
        self.DragArgs["DragStarted"] = False
    # ----------
    def DBClick_Maximize(self, event: Event):
        # 校验
        if self.ResizeArgs["Type"]: return # 确保不处于 ReSize 判定区
        if self.Master.Maximized["Cooldown"]: return # 确保不处于双击最大化冷却期

        self.Master.Maximized["Cooldown"] = True

        if self.Master.Maximized["State"]:
            self.Master.Maximized["State"] = False
            self.Master.Behavior.RestoredSize()
        else:
            self.Master.Maximized["State"] = True
            self.Master.Maximized["Pos"] = self.Master.geometry()
            self.Master.Behavior.MaxedSize()

        self.Master.Behavior.After(self.Master.Maximized["CooldownTime"], lambda: self.Master.Maximized.__setitem__("Cooldown", False))
    # ----------
    def Btn_Minimize(self, event: Event = None):
        self.Master.Behavior.MinedSize()

    def Btn_Maximize(self, event: Event = None):
        if self.Master.Maximized["State"]:
            self.Master.Maximized["State"] = False
            self.Master.Behavior.RestoredSize()
        else:
            self.Master.Maximized["State"] = True
            self.Master.Maximized["Pos"] = self.Master.geometry()
            self.Master.Behavior.MaxedSize()

    def Btn_Exit(self, event: Event):
        self.Master.Exit()
    # ----------
    def BindResizeZones(self):
        self.Master.bind("<Motion>", self.Resize_ZoneHitCheck)
        self.Master.bind("<Button-1>", self.Resize_Press)
        self.Master.bind("<B1-Motion>", self.Resize_Move)

    def Resize_ZoneHitCheck(self, event: Event):
        # 校验
        if self.Master.Maximized["State"]: return # 确保不处于最大化状态

        WinPos_X = event.x_root - self.Master.winfo_x()
        WinPos_Y = event.y_root - self.Master.winfo_y()
        WinSize_W = self.Master.winfo_width()
        WinSize_H = self.Master.winfo_height()

        HitState: tuple = (
            WinPos_X < self.ResizeArgs["EdgePx"],              # Hit_Left
            WinPos_X > WinSize_W - self.ResizeArgs["EdgePx"],  # Hit_Right
            WinPos_Y < self.ResizeArgs["EdgePx"],              # Hit_Top
            WinPos_Y > WinSize_H - self.ResizeArgs["EdgePx"]   # Hit_Bottom
        )

        match HitState:
            case (True, False, True, False): # Hit_Left & Hit_Top
                self.ResizeArgs["Type"] = 'nw'
                self.Master.configure(cursor='top_left_corner')
            case (True, False, False, True): # Hit_Left & Hit_Bottom
                self.ResizeArgs["Type"] = 'sw'
                self.Master.configure(cursor='bottom_left_corner')
            case (False, True, True, False): # Hit_Right & Hit_Top
                self.ResizeArgs["Type"] = 'ne'
                self.Master.configure(cursor='top_right_corner')
            case (False, True, False, True): # Hit_Right & Hit_Bottom
                self.ResizeArgs["Type"] = 'se'
                self.Master.configure(cursor='bottom_right_corner')
            case (True, False, False, False): # Hit_Left
                self.ResizeArgs["Type"] = 'w'
                self.Master.configure(cursor='sb_h_double_arrow')
            case (False, True, False, False): # Hit_Right
                self.ResizeArgs["Type"] = 'e'
                self.Master.configure(cursor='sb_h_double_arrow')
            case (False, False, True, False): # Hit_Top
                self.ResizeArgs["Type"] = 'n'
                self.Master.configure(cursor='sb_v_double_arrow')
            case (False, False, False, True): # Hit_Bottom
                self.ResizeArgs["Type"] = 's'
                self.Master.configure(cursor='sb_v_double_arrow')
            case _:
                self.ResizeArgs["Type"] = None
                self.Master.configure(cursor='')

    def Resize_Press(self, event: Event):
        self.Resize_ZoneHitCheck(event)  # 确保按下时仍处于热区
        if self.ResizeArgs["Type"]:
            self.ResizeArgs["CursorX"] = event.x_root
            self.ResizeArgs["CursorY"] = event.y_root
            self.ResizeArgs["WinSizeW"] = self.Master.winfo_width()
            self.ResizeArgs["WinSizeH"] = self.Master.winfo_height()
        else:
            self.ResizeArgs["Type"] = None

    def Resize_Move(self, event: Event):
        # 校验
        if not self.ResizeArgs["Type"]: return # 确保光标处于 ReSize 判定区域

        DeltaX = event.x_root - self.ResizeArgs["CursorX"]
        DeltaY = event.y_root - self.ResizeArgs["CursorY"]

        Width_New = self.ResizeArgs["WinSizeW"]
        Height_New = self.ResizeArgs["WinSizeH"]
        X_New = self.Master.winfo_x()
        Y_New = self.Master.winfo_y()

        Min_Height = self.SIZE_Mainheight
        Min_Width = self.Master.minsize()[0]

        if 'e' in self.ResizeArgs["Type"]:
            Width_New = max(Min_Width, self.ResizeArgs["WinSizeW"] + DeltaX)
        if 's' in self.ResizeArgs["Type"]:
            Height_New = max(Min_Height, self.ResizeArgs["WinSizeH"] + DeltaY)
        if 'w' in self.ResizeArgs["Type"]:
            # 新宽度 = 原宽度 - 鼠标横向移动量(向左拖 DeltaX<0, 宽度应增加)
            Width_New = max(Min_Width, self.ResizeArgs["WinSizeW"] - DeltaX)
            # 窗口左上角 x 应移动 DeltaX, 以保持鼠标“吸附”在左边缘
            X_New = self.ResizeArgs["CursorX"] - (Width_New - self.ResizeArgs["WinSizeW"])
        if 'n' in self.ResizeArgs["Type"]:
            # 新高度 = 原高度 - 鼠标纵向移动量(向上拖 DeltaY<0, 高度应增加)
            Height_New = max(Min_Height, self.ResizeArgs["WinSizeH"] - DeltaY)
            # 窗口左上角 y 应移动 DeltaY, 以保持鼠标“吸附”在上边缘
            Y_New = self.ResizeArgs["CursorY"] - (Height_New - self.ResizeArgs["WinSizeH"])

        self.Master.geometry(f"{int(Width_New)}x{int(Height_New)}+{int(X_New)}+{int(Y_New)}")

# --------------------------------------------------

class EasyTk(Tk):
    def __init__(
            self,
            IndepTitleBar: bool = False,
            WinTransparent: tuple[bool, str] = (False, "gray15")
    ):
        super().__init__(className = 'EasyTk')

        self.RootType: str = 'EasyTk'
        self.Type: str = 'EasyTk'

        self.HWND: int = 0

        self.DPIScale: float = self.GetSysDPI()

        # 重写
        self.RewriteEvent()

        # self.Configure: Configure = Configure(self)

        # 窗口状态
        self.Destroyed: bool = False
        self.Maximized: dict[str | bool | str] = {
            "State": False,
            "Cooldown": False,
            "CooldownTime": 200,
            "Pos": ""
        }
        self.Minimized: dict[str | bool | str] = {
            "State": False,
            "Cooldown": False,
            "CooldownTime": 200,
            "Pos": ""
        }

        # 启用独立标题栏
        self.TitleBar = self.IndepTitleBar() if IndepTitleBar else None

        # 启用透明窗口支持
        self.TRANSPARENT_COLOR: str = WinTransparent[1]
        if WinTransparent[0]: self.wm_attributes("-transparentcolor", self.TRANSPARENT_COLOR)

        self.bind("<F3>", self.Debug_ShowZones)

    @property
    def Content(self) -> Content:
        return Content(self)

    @property
    def Style(self) -> Style:
        return Style(self)
    
    @property
    def Behavior(self) -> Behavior:
        return Behavior(self)

    @property
    def Configure(self) -> Configure:
        return Configure(self)

    @property
    def WinState(self) -> Literal["Waiting", "Displaying", "Destroyed", "Minimized"]:
        if self.Destroyed: return "Destroyed"
        if self.Minimized["State"]: return "Minimized"
        State: int | str = self.winfo_viewable()
        return "Waiting" if State == 0 else "Displaying" if State else State

    def GetSysDPI(self) -> float:
        windll.shcore.SetProcessDpiAwareness(1)
        user32 = WINDLLU32
        user32.SetProcessDPIAware()
        dpi = user32.GetDpiForSystem()
        return dpi / 96.0

    def RewriteEvent(self):
        self.protocol("WM_DELETE_WINDOW", self.Exit)

    def IndepTitleBar(self):
        self.wm_overrideredirect(True)
        zTitleBar = TitleBar(self)
        return zTitleBar

    def Run(self):
        self.update_idletasks()
        self.HWND = WINDLLU32.GetParent(self.winfo_id())
        if self.TitleBar != None: ResetWinStyle(self.HWND, "UnTtlBar")

        self.mainloop()

    def Exit(self, Level: Literal["Window", "Program"] = "Window", ExitCode: int | tuple[int, str] = 0):
        if isinstance(ExitCode, int): ExitCode = (ExitCode, "")
        elif isinstance(ExitCode, tuple):
            if len(ExitCode) == 1 and isinstance(ExitCode[0], int): ExitCode = (ExitCode[0], "")
            elif all([len(ExitCode) == 2, isinstance(ExitCode[0], int), isinstance(ExitCode[1], str)]): pass
            else: raise ValueError(f"Expect <tuple[int, str]>, got <tuple{[type(Value).__name__ for Value in ExitCode]}>.")
        else: raise ValueError(f"Expect <int | tuple>, got <{type(ExitCode).__name__}>.")

        self.quit()
        self.destroy()

        self.Destroyed = True

        if Level == "Program":
            if isinstance(ExitCode, int):
                ExitMessage: str = "" ; ExitCode: int = ExitCode
            else:
                ExitMessage: str = ExitCode[1]; ExitCode: int = ExitCode[0]
            LogPrint(ExitMessage) if ExitMessage else None
            SysExit(ExitCode if isinstance(ExitCode, int) else ExitCode[0])

    """ --- 调试显示器 --- """
    def Debug_ShowZones(self, event: Event = None):
        pass

# ----------------------------------------------------------------------------------------------------

from ctypes import windll
from enum import IntFlag
from typing import Literal

WINDLLU32 = windll.user32

class WinStyles(IntFlag):
    """Windows 窗口样式标志 (Window Styles) """
    
    WS_OVERLAPPED = 0x00000000
    """创建一个重叠窗口(默认顶层窗口).通常与 WS_CAPTION 一起使用."""

    WS_POPUP = 0x80000000
    """创建一个弹出窗口(无边框、无标题栏，通常用于对话框或自定义窗口)."""

    WS_CHILD = 0x40000000
    """创建一个子窗口(必须有父窗口).不能与 WS_POPUP 同时使用."""

    WS_MINIMIZE = 0x20000000
    """创建时窗口最小化."""

    WS_VISIBLE = 0x10000000
    """创建后窗口可见."""

    WS_DISABLED = 0x08000000
    """禁用窗口(不响应用户输入)."""

    WS_CLIPSIBLINGS = 0x04000000
    """剪裁子窗口区域，防止绘制到其他同级窗口上(常用于 MDI 或复杂 UI)."""

    WS_CLIPCHILDREN = 0x02000000
    """父窗口绘制时不绘制到子窗口区域(提高性能)."""

    WS_CAPTION = 0x00C00000
    """创建标题栏"""

    WS_BORDER = 0x00800000
    """创建细边框(单像素边框，无标题栏)."""

    WS_SYSMENU = 0x00080000
    """在标题栏左侧显示系统菜单(关闭按钮等).必须与 `WS_CAPTION` 一起使用才有效."""

    WS_DLGFRAME = 0x00400000
    """创建对话框风格边框(无标题栏，但有系统菜单区域)."""

    WS_VSCROLL = 0x00200000
    """包含垂直滚动条."""

    WS_HSCROLL = 0x00100000
    """包含水平滚动条."""

    WS_THICKFRAME = 0x00040000
    """可调整大小的边框(也称 WS_SIZEBOX).允许用户拖动边框改变窗口大小."""

    WS_MAXIMIZE = 0x01000000
    """创建时窗口最大化."""

    WS_MINIMIZEBOX = 0x00020000
    """显示最小化按钮(必须与 `WS_SYSMENU` 一起使用)."""

    WS_MAXIMIZEBOX = 0x00010000
    """显示最大化按钮(必须与 `WS_SYSMENU` 一起使用)."""

    # 扩展样式 (通常用于 CreateWindowEx 的 dwExStyle 参数) 
    WS_EX_DLGMODALFRAME = 0x00000001
    """为窗口添加双线边框(即使没有 WS_CAPTION)."""

    WS_EX_NOPARENTNOTIFY = 0x00000004
    """子窗口创建/销毁时不通知父窗口."""

    WS_EX_TOPMOST = 0x00000008
    """窗口置顶(总在最前)."""

    WS_EX_ACCEPTFILES = 0x00000010
    """允许窗口接收拖放文件(需处理 WM_DROPFILES)."""

    WS_EX_TRANSPARENT = 0x00000020
    """窗口透明(鼠标事件穿透到下层窗口，不是视觉透明)."""

    WS_EX_MDICHILD = 0x00000040
    """MDI 子窗口(必须有 MDI 客户区父窗口)."""

    WS_EX_TOOLWINDOW = 0x00000080
    """工具窗口：不在任务栏显示，标题栏较小."""

    WS_EX_WINDOWEDGE = 0x00000100
    """带凸起边缘的边框(3D 效果)."""

    WS_EX_CLIENTEDGE = 0x00000200
    """客户区带凹陷边框(如 Edit 控件)."""

    WS_EX_CONTEXTHELP = 0x00000400
    """标题栏右侧显示“?”帮助按钮(与 WS_MAXIMIZEBOX 互斥)."""

    WS_EX_RIGHT = 0x00001000
    """窗口文本从右到左(用于阿拉伯语等)."""

    WS_EX_LEFT = 0x00000000
    """默认：文本从左到右."""

    WS_EX_RTLREADING = 0x00002000
    """标题栏文本从右到左显示."""

    WS_EX_LEFTSCROLLBAR = 0x00004000
    """垂直滚动条在左侧(用于 RTL 语言)."""

    WS_EX_CONTROLPARENT = 0x00010000
    """父窗口可处理子控件的 Tab 键导航(用于对话框)."""

    WS_EX_STATICEDGE = 0x00020000
    """静态 3D 边框(无交互效果)."""

    WS_EX_APPWINDOW = 0x00040000
    """强制窗口在任务栏显示(即使没有父窗口或为工具窗口)."""

    WS_EX_LAYERED = 0x00080000
    """支持分层窗口(用于透明、异形窗口，需配合 SetLayeredWindowAttributes 或 UpdateLayeredWindow)."""

    WS_EX_NOINHERITLAYOUT = 0x00100000
    """不继承父窗口的布局(如 RTL 设置)."""

    WS_EX_LAYOUTRTL = 0x00400000
    """使用 RTL 布局(Mirrored window)."""

    WS_EX_COMPOSITED = 0x02000000
    """使用双缓冲绘制(减少闪烁，但可能影响性能)."""

    WS_EX_NOACTIVATE = 0x08000000
    """窗口显示时不激活(如通知气泡)."""

    @classmethod
    def ReturnAll(cls) -> dict[str, int]:
        return {member.name: member.value for member in cls}

class WinStates(IntFlag):
    """Windows 窗口显示状态 (ShowWindow 命令) """
    
    SW_HIDE = 0
    """隐藏窗口"""

    SW_SHOWNORMAL = 1
    """激活并显示窗口(如果是第一次显示, 窗口会按原始大小和位置显示)"""

    SW_NORMAL = 1
    """同 SW_SHOWNORMAL"""

    SW_SHOWMINIMIZED = 2
    """激活窗口并将其最小化"""

    SW_SHOWMAXIMIZED = 3
    """激活窗口并将其最大化"""

    SW_MAXIMIZE = 3
    """同 SW_SHOWMAXIMIZED"""

    SW_SHOWNOACTIVATE = 4
    """显示窗口但不激活(不获取焦点)"""

    SW_SHOW = 5
    """显示窗口(如果是隐藏的), 但不改变其激活状态"""

    SW_MINIMIZE = 6
    """最小化窗口, 激活Z序中的下一个顶层窗口"""

    SW_SHOWMINNOACTIVE = 7
    """显示窗口为最小化状态, 但不激活"""

    SW_SHOWNA = 8
    """显示窗口(如果是隐藏的), 但不改变其激活状态(同 SW_SHOW)"""

    SW_RESTORE = 9
    """激活并显示窗口(如果是最小化或最大化状态, 恢复到原始大小和位置)"""

    SW_SHOWDEFAULT = 10
    """根据启动应用程序时指定的 STARTUPINFO 结构中的值来显示窗口"""

    SW_FORCEMINIMIZE = 11
    """强制最小化窗口(即使用户正在使用其他窗口)"""

    @classmethod
    def ReturnAll(cls) -> dict[str, int]:
        return {member.name: member.value for member in cls}

def ResetWinStyle(HWND: int, mode: Literal["Basic", "UnTtlBar"] | list | tuple = "Basic"):
    """Reset or customize the window style of a given HWND.

    Args:
        HWND (int): Handle to the target window.
        mode (optional): 
            - "Basic": Apply default window style.
            - "UnTtlBar": Remove title bar and border.
            - (Style_New, ExStyle_New): Custom style tuple, e.g., (0x12345678, 0x87654321).
              Both values should be integers representing new window style and extended style.
            Defaults to "Basic".

    Examples:
        >>> ResetWinStyle(hwnd, "UnTtlBar")
        >>> ResetWinStyle(hwnd, (0x12345678, 0x87654321))
    """

    GWL_STYLE = -16
    GWL_EXSTYLE = -20
    
    # 获取样式
    Style_Current = WINDLLU32.GetWindowLongPtrW(HWND, GWL_STYLE)
    ExStyle_Current = WINDLLU32.GetWindowLongPtrW(HWND, GWL_EXSTYLE)
    
    Style_New = None
    ExStyle_New = None

    match mode:
        case "Basic":
            Style_New = (
                WinStyles.WS_OVERLAPPED |
                WinStyles.WS_CAPTION |
                WinStyles.WS_SYSMENU |
                WinStyles.WS_THICKFRAME |
                WinStyles.WS_MINIMIZEBOX |
                WinStyles.WS_MAXIMIZEBOX |
                WinStyles.WS_VISIBLE
            )
            ExStyle_New = (
                WinStyles.WS_EX_WINDOWEDGE |
                WinStyles.WS_EX_APPWINDOW
            )
        case "UnTtlBar":
            Style_New = (
                WinStyles.WS_VISIBLE
            )
            ExStyle_New = (
                WinStyles.WS_EX_APPWINDOW
            )
        case _:
            Style_New = mode[0]
            ExStyle_New = mode[1]

    # 设置样式
    WINDLLU32.SetWindowLongPtrW(HWND, GWL_STYLE, Style_New)
    WINDLLU32.SetWindowLongPtrW(HWND, GWL_EXSTYLE, ExStyle_New)

    # 重新激活窗口以应用样式
    WINDLLU32.ShowWindow(HWND, WinStates.SW_MINIMIZE)
    WINDLLU32.ShowWindow(HWND, WinStates.SW_RESTORE)

    return Style_Current, ExStyle_Current

if __name__ == "__main__":
    from tkinter import Tk, Button, Label, Entry, Checkbutton, Radiobutton, Scale, Listbox, Text, Spinbox, OptionMenu, Frame
    import tkinter.font as tkFont

    root: Tk = Tk()

    root.configure(bg="#6CA9E7")
    root.wm_overrideredirect(True)
    root.geometry("600x500")

    # 获取窗口句柄并重置样式
    WINDLLU32 = windll.user32
    HWND = root.winfo_id()
    root.update_idletasks()
    ResetWinStyle(HWND, "UnTtlBar")
    

    # 添加大量控件（10+）
    Label(root, text="Label 示例", bg="#6CA9E7", fg="white", font=("Arial", 12)).pack(pady=5)
    
    Entry(root, width=30).pack(pady=5)
    
    Button(root, text="按钮 Button", command=lambda: print("Clicked!")).pack(pady=5)
    
    Checkbutton(root, text="复选框 Checkbutton", bg="#6CA9E7").pack(pady=5)
    
    Radiobutton(root, text="单选按钮1", variable="radio", value=1, bg="#6CA9E7").pack()
    Radiobutton(root, text="单选按钮2", variable="radio", value=2, bg="#6CA9E7").pack(pady=5)
    
    Scale(root, from_=0, to=100, orient="horizontal", bg="#6CA9E7").pack(pady=5)
    
    listbox = Listbox(root, height=4)
    for i in range(1, 6):
        listbox.insert("end", f"列表项 {i}")
    listbox.pack(pady=5)
    
    Text(root, height=3, width=40).pack(pady=5)
    
    Spinbox(root, from_=0, to=100, width=10).pack(pady=5)
    
    options = ["选项1", "选项2", "选项3"]
    OptionMenu(root, "选择", *options).pack(pady=5)
    
    frame = Frame(root, bg="lightgray", width=200, height=50)
    frame.pack(pady=10)
    frame.pack_propagate(False)
    Label(frame, text="Frame 容器", bg="lightgray").pack()

    

    root.mainloop()

if __name__ == "__main__":
    root = EasyTk(True)
    root.Content.Title("WoLeGeSaoGang我了个骚肛")
    root.geometry("1000x600+970+550")
    root.Run()

    