from tkinter import (
    Frame, Label, Button, Scale, Checkbutton, Entry, 
    StringVar, BooleanVar, IntVar, PhotoImage
)
from tkinter.ttk import Combobox
from PIL import Image, ImageTk, ImageFile
from EasyTk import ezTk, ezFrame, ezFrameManager

class Frame_LeftBar(ezFrame):
    def UIInit(self):
        """初始化左侧功能菜单的UI"""
        # 主容器：使用与设置面板协调的深灰背景
        self.Frame = Frame(master=self.master, name=self.name, width=200, bg="#242424")
        self.Frame.pack_propagate(False)

        btn_style = {
            "width": 23,
            "height": 2,
            "font": ("Microsoft YaHei", 11, "bold"),
            "bg": "#3A3A3A",
            "fg": "#E0E0E0",
            "activebackground": "#505050",
            "activeforeground": "white",
            "relief": "flat",
            "borderwidth": 0,
            "cursor": "hand2",
            "highlightthickness": 0
        }

        Label(
            self.Frame,
            text="功能选单",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#242424",
            fg="#FFFFFF"
        ).pack(fill="x", pady=(20, 25))

        # 带 hover 效果的按钮工厂
        def CreateButton(text, cmd):
            btn = Button(self.Frame, text=text, command=cmd, **btn_style)
            # 悬停高亮
            btn.bind("<Enter>", lambda e: btn.config(bg="#4A4A4A"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#3A3A3A"))
            return btn

        # 功能按钮(从上到下)
        CreateButton("主页", lambda: self.master.Switch("frame_Home")).pack(padx=5, pady=(0, 10))
        CreateButton("Frame 1", lambda: self.master.Switch("frame_1")).pack(padx=5, pady=(0, 10))

        # 底部按钮(退出)
        CreateButton("退出", lambda: self.master.master.Exit(None)).pack(side="bottom", padx=5, pady=(0, 20))
        CreateButton("设置", lambda: self.master.Switch("frame_Config")).pack(side="bottom", padx=5, pady=(0, 10))
    
    def DoPlace(self):
        self.Frame.pack(side="left", fill="y")

class Frame_Home(ezFrame):
    def UIInit(self):
        self.Frame = Frame(master=self.master, name=self.name, bg="#2D2D2D")
        self.Frame.pack_propagate(False)
        
        Path_Img: str = "./Logo.png"

        # 居中容器(整体略偏上)
        Frame_Center = Frame(self.Frame, bg="#2D2D2D")
        Frame_Center.place(relx=0.5, rely=0.45, anchor="center")

        # Logo
        self.LogoImg_Source: ImageFile = None
        self.LogoImg_Zoomed: PhotoImage = None
        self.Label_Logo = Label(Frame_Center, bg="#2D2D2D")
        self.Label_Logo.pack(pady=(0, 20))

        try:
            self.LogoImg_Source = Image.open(Path_Img)
        except Exception:
            pass

        def _LogoResize_(_):
            FrameW, FrameH = self.Size
            if FrameH < 10: return
            elif self.Label_Logo is None or self.LogoImg_Source is None:
                self.Label_Logo.config(image="", text="🖼️", font=("Segoe UI Emoji", 48), fg="#555555")
                return

            LogoImg_Zoomed = self.LogoImg_Source.copy()
            LogoImg_Zoomed.thumbnail((int(FrameW * 0.65), int(FrameH * 0.45)), Image.LANCZOS)
            self.LogoImg_Zoomed = ImageTk.PhotoImage(LogoImg_Zoomed)
            self.Label_Logo.config(image=self.LogoImg_Zoomed, text="")
            Frame_Center.unbind("<Configure>")
            Frame_Center.after(50, lambda: Frame_Center.bind("<Configure>", _LogoResize_))

        Frame_Center.bind("<Configure>", _LogoResize_)

        # === 标题与简介 ===
        Label(
            Frame_Center,
            text="Example Application",
            font=("Microsoft YaHei", 25, "bold"),
            bg="#2D2D2D",
            fg="#FFFFFF"
        ).pack(pady=(0, 12))

        Label(
            Frame_Center,
            text="请选择左侧功能开始操作",
            font=("Microsoft YaHei", 11),
            bg="#2D2D2D",
            fg="#A0A0A0"
        ).pack(pady=(0, 0))

        self.geomsync()

    def DoPlace(self):
        self.Frame.pack(side="right", fill="both", expand=True)

    def geomsync(self):
        # 初始化之后给其他框架同步尺寸[仅在初始化时执行]
        # self.Frame.bind("<Map>", lambda _: (self.Frame.unbind("<Map>"), self.master.Refresh(True)))

        # Frame_Home 尺寸变化时给当前激活框架同步尺寸[只要窗口尺寸变化就执行]
        self.frames_geomsync: set = {}
        def _syncfunc_(_):
            match self.master._SwitchMode_:
                case "redraw":
                    for frame_name in self.frames_geomsync:
                        if frame_name in self.master.frames_persisted or frame_name == self.master.frame_activated: self.master[frame_name].DoPlace()
                case "tkraise":
                    for frame_name in self.frames_geomsync:
                        self.master[frame_name].DoPlace()

        self.Frame.bind("<Configure>", _syncfunc_)

    @property
    def Pos(self):
        return self.Frame.winfo_x(), self.Frame.winfo_y()

    @property
    def Size(self):
        return self.Frame.winfo_width(), self.Frame.winfo_height()

class Frame_Config(ezFrame):
    def UIInit(self):
        """初始化所有UI控件和样式 —— 深色现代化配置面板"""
        # 主容器(深灰背景)
        self.Frame = Frame(master=self.master, name=self.name, bg="#2D2D2D")
        self.Frame.pack_propagate(False)

        PanelLeft = Frame(master=self.Frame, bg="#3A3A3A")
        PanelLeft.pack(side="left", fill="both", expand=True, padx=(5, 2.5), pady=5)
        PanelLeft.pack_propagate(False)

        PanelRight = Frame(master=self.Frame, bg="#3A3A3A")
        PanelRight.pack(side="right", fill="both", expand=True, padx=(2.5, 5), pady=5)
        PanelRight.pack_propagate(False)

        # === 储存所有变量，便于后续读取 ===
        self.config_vars = {}

        # === 主标题 ===
        Label(
            PanelLeft, text="系统配置", anchor="w",
            bg="#3A3A3A", fg="#FFFFFF",
            font=("Microsoft YaHei", 14, "bold")
        ).pack(fill="x", padx=12, pady=(10, 8))

        self.AddConfigRow_SplitLine(PanelLeft, color="#555555", height=1.5, padx=10, pady=(0, 12))
        # === 分组 1：通用设置 ===
        self.AddConfigRow_GroupTitle(PanelLeft, "通用设置")
        self.AddConfigRow_SplitLine(PanelLeft, color="#4A4A4A", height=1, padx=8, pady=(0, 6))
        self.AddConfigRow_Checkbox(PanelLeft, "开机自动启动", "auto_start", default=True)
        self.AddConfigRow_Combobox(PanelLeft, "界面语言:", "language", ["简体中文", "English", "日本語"], default="简体中文")

        # === 分组 2：显示与外观 ===
        self.AddConfigRow_GroupTitle(PanelLeft, "显示与外观")
        self.AddConfigRow_SplitLine(PanelLeft, color="#4A4A4A", height=1, padx=8, pady=(0, 6))
        self.AddConfigRow_Combobox(PanelLeft, "主题模式:", "theme", ["浅色模式", "深色模式", "自动"], default="深色模式")
        self.AddConfigRow_Slider(PanelLeft, "界面缩放:", "ui_scale", from_=80, to=150, default=100, unit="%")
        self.AddConfigRow_Checkbox(PanelLeft, "启用平滑动画", "smooth_anim", default=True)

        # === 分组 3：网络与隐私 ===
        self.AddConfigRow_GroupTitle(PanelLeft, "网络与隐私")
        self.AddConfigRow_SplitLine(PanelLeft, color="#4A4A4A", height=1, padx=8, pady=(0, 6))
        self.AddConfigRow_Checkbox(PanelLeft, "允许匿名统计", "allow_analytics", default=False)
        self.AddConfigRow_Entry(PanelLeft, "代理地址:", "proxy_addr", default="127.0.0.1:8080")

        # === 底部按钮区 ===
        Frame_Decision = Frame(PanelRight, bg="#3A3A3A")
        Frame_Decision.pack(side="bottom", fill="x", padx=10, pady=(15, 10))

        Button(
            Frame_Decision, text="取消", width=10,
            command=lambda: print("取消配置"),
            font=("Microsoft YaHei", 10, "bold"),
            bg="#6C757D", fg="white",
            relief="flat", activebackground="#5A6268"
        ).pack(side="right", padx=(0, 6))

        Button(
            Frame_Decision, text="应用", width=10,
            command=self._on_apply,
            font=("Microsoft YaHei", 10, "bold"),
            bg="#28A745", fg="white",
            relief="flat", activebackground="#218838"
        ).pack(side="right")

    def _on_apply(self):
        """应用配置(示例：打印所有值)"""
        print("\n=== 当前配置 ===")
        for key, var in self.config_vars.items():
            if hasattr(var, 'get'):
                print(f"{key}: {var.get()}")
            else:
                print(f"{key}: {var}")
        print("================\n")

    def DoPlace(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.Frame.configure(width=size[0], height=size[1])
        self.Frame.place(x=pos[0], y=pos[1])

    def AddConfigRow_GroupTitle(self, master, title: str):
        """添加分组标题(类似 Labelframe 的轻量替代)"""
        frame = Frame(master, height=30, bg="#3A3A3A")
        frame.pack(fill="x", padx=8, pady=(14, 6))
        Label(
            frame, text=title,
            bg="#3A3A3A", fg="#AAAAAA",
            font=("Microsoft YaHei", 10, "bold")
        ).pack(side="left")

    def AddConfigRow_SplitLine(self, master, color: str = None, height: int = None, padx: tuple[float, float] | float = None, pady: tuple[float, float] | float = None):
        kwargs = {trans[key] if key in (trans:={"color": "bg"}) else key: value for key, value in locals().items() if not key == "self" and not value is None}
        Frame(**{key: value for key, value in kwargs.items() if not key in ["padx", "pady"]}).pack(fill="x", **{key: value for key, value in kwargs.items() if key in ["padx", "pady"]})

    def AddConfigRow_Button(self, master, label_text="", button_text="", command=None):
        row = Frame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        Label(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)
        Button(row, text=button_text, width=12, font=("Microsoft YaHei", 10),
               bg="#4CAF50", fg="white", relief="flat", activebackground="#45a049",
               command=command or (lambda: None)).pack(side="right", padx=(6, 0))

    def AddConfigRow_Slider(self, master, label_text: str, key: str, from_=0, to=100, default=50, unit=""):
        """滑动条(自动绑定 IntVar)"""
        row = Frame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        # 标签 + 单位
        label_full = f"{label_text} {default}{unit}" if unit else label_text
        label_widget = Label(row, text=label_full, anchor="w", bg="#3A3A3A", fg="white",
                             font=("Microsoft YaHei", 10))
        label_widget.pack(side="left", fill="x", expand=True)

        var = IntVar(value=default)
        self.config_vars[key] = var

        def on_slider_change(val):
            val = int(float(val))
            text = f"{label_text} {val}{unit}" if unit else f"{label_text} {val}"
            label_widget.config(text=text)

        slider = Scale(row, from_=from_, to=to, orient="horizontal", length=120,
                       bg="#3A3A3A", fg="white", troughcolor="#555555",
                       highlightthickness=0, sliderrelief="flat",
                       font=("Microsoft YaHei", 9), variable=var,
                       command=on_slider_change)
        slider.pack(side="right", padx=(6, 0))

    def AddConfigRow_Checkbox(self, master, label_text: str, key: str, default=False):
        """复选框(自动绑定 BooleanVar)"""
        row = Frame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        var = BooleanVar(value=default)
        self.config_vars[key] = var

        cb = Checkbutton(row, text=label_text, variable=var,
                         bg="#3A3A3A", fg="white", selectcolor="#555555",
                         activebackground="#3A3A3A", activeforeground="white",
                         font=("Microsoft YaHei", 10), highlightthickness=0)
        cb.pack(side="left")

    def AddConfigRow_Entry(self, master, label_text: str, key: str, default=""):
        """文本输入框(自动绑定 StringVar)"""
        row = Frame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        Label(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)

        var = StringVar(value=default)
        self.config_vars[key] = var

        entry = Entry(row, textvariable=var, width=14,
                      font=("Microsoft YaHei", 10),
                      bg="#4A4A4A", fg="white", insertbackground="white",
                      relief="flat")
        entry.pack(side="right", padx=(6, 0))

    def AddConfigRow_Combobox(self, master, label_text: str, key: str, values: list, default: str = ""):
        """下拉框(自动绑定 StringVar)"""
        row = Frame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        Label(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)

        var = StringVar(value=default if default in values else (values[0] if values else ""))
        self.config_vars[key] = var

        combo = Combobox(row, textvariable=var, values=values, state="readonly", width=12, font=("Microsoft YaHei", 10))
        combo.pack(side="right", padx=(6, 0))

class Frame_1(ezFrame):
    def UIInit(self):
        self.Frame: Frame = Frame(master=self.master, name=self.name, bg="lightgreen")
        self.Frame.pack_propagate(False)

        Label(self.Frame, text="这是 Frame 1", font=("Arial", 16), bg="lightgreen").pack(pady=20)
        Button(self.Frame, text="切换到 Frame 2", command=lambda: self.master.Switch("frame_2")).pack(pady=10)
    
    def DoPlace(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.Frame.configure(width=size[0], height=size[1])
        self.Frame.place(x=pos[0], y=pos[1])

class Frame_2(ezFrame):
    def UIInit(self):
        self.Frame: Frame = Frame(master=self.master, name=self.name, bg="#448169")
        self.Frame.pack_propagate(False)

        Label(self.Frame, text="这是 Frame 2", font=("Arial", 16), bg="#448169").pack(pady=20)
        Button(self.Frame, text="切换到 Frame 1", command=lambda: self.master.Switch("frame_1")).pack(pady=10)
    
    def DoPlace(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.Frame.configure(width=size[0], height=size[1])
        self.Frame.place(x=pos[0], y=pos[1])

if __name__ == "__main__":
    Root = ezTk("ezTk 测试")
    Root.Geometry.Size(1280, 768)
    Root.Geometry.SizeLimit("min", 1024, 600)
    # Root.Geometry.SizeFix(True, True)

    FrameManager = ezFrameManager(Root)
    FrameManager.SwitchMode("redraw")
    FrameManager.frames_persisted = ["frame_LeftBar", "frame_Home", "frame_Config"]
    FrameManager.AddFrame([
        Frame_LeftBar(master=FrameManager, name="frame_LeftBar"),
        Frame_Home(master=FrameManager, name="frame_Home"),
        Frame_Config(master=FrameManager, name="frame_Config"),
        Frame_1(master=FrameManager, name="frame_1"),
        Frame_2(master=FrameManager, name="frame_2")
    ], "frame_Home")
    FrameManager["frame_Home"].frames_geomsync = {"frame_Config", "frame_1", "frame_2"}

    Root.mainloop()
