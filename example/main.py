from tkinter import (
    Frame as tkFrame, Label as tkLabel, Button as tkButton, Scale as tkScale, Checkbutton as tkCheckbutton, Entry as tkEntry,
    PhotoImage as tkPhotoImage,
    StringVar, BooleanVar, IntVar
)
from tkinter.ttk import (
    Combobox as ttkCombobox
)
from PIL import Image, ImageTk, ImageFile
from EasyTk import ezTk, ezFrame, ezFrameHub
from typing import Literal, Callable

class Frame_LeftBar(ezFrame):
    def _ui_init_(self):
        """初始化左侧功能菜单的UI"""
        self.configure(width=200, bg="#242424")
        self.pack_propagate(False)

        tkLabel(
            self,
            text="功能选单",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#242424",
            fg="#FFFFFF"
        ).pack(fill="x", pady=(20, 25))

        self.btn_register("退出", "", self.master.master.Exit, "bottom")
        self.btn_register("设置", "frame_Config", "", "bottom")

    def _do_place_(self):
        self.pack(side="left", fill="y")

    def btn_register(
            self,
            text: str,
            frame_name: str = None,
            command: Callable = "",
            side: Literal["left", "right", "top", "bottom"] = None
    ):
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
        command = command or (lambda: self.master.switch(frame_name, lambda frame: frame._do_place_()) if frame_name else "")
        btn = tkButton(self, text=text, command=command, **btn_style)

        btn.bind("<Enter>", lambda e: btn.config(bg="#4A4A4A"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3A3A3A"))

        btn.pack(side=side, padx=7, pady=(0, 10))

class Frame_Home(ezFrame):
    def _ui_init_(self):
        self.configure(bg="#2D2D2D")
        self.pack_propagate(False)
        
        Path_Img: str = "./example/Logo.png"

        # 居中容器(整体略偏上)
        Frame_Center = tkFrame(self, bg="#2D2D2D")
        Frame_Center.place(relx=0.5, rely=0.45, anchor="center")

        # Logo
        self.LogoImg_Source: ImageFile = None
        self.LogoImg_Zoomed: tkPhotoImage = None
        self.Label_Logo = tkLabel(Frame_Center, bg="#2D2D2D")
        self.Label_Logo.pack(pady=(0, 20))

        try:
            self.LogoImg_Source = Image.open(Path_Img)
        except Exception as E:
            print(str(E))

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
        tkLabel(
            Frame_Center,
            text="Example Application",
            font=("Microsoft YaHei", 25, "bold"),
            bg="#2D2D2D",
            fg="#FFFFFF"
        ).pack(pady=(0, 12))

        tkLabel(
            Frame_Center,
            text="请选择左侧功能开始操作",
            font=("Microsoft YaHei", 11),
            bg="#2D2D2D",
            fg="#A0A0A0"
        ).pack(pady=(0, 0))

        self.geomsync()

    def _do_place_(self):
        self.pack(side="right", fill="both", expand=True)

    def geomsync(self):
        # Frame_Home 尺寸变化时给当前激活框架同步尺寸
        def _syncfunc_(_):
            if self.master.frame_reg.activated is None: return
            frame: ezFrame = self.master[self.master.frame_reg.activated]
            if not getattr(frame, "sync_geom_with_home", False): return
            self.master[self.master.frame_reg.activated].configure(width=self.winfo_width(), height=self.winfo_height())

        self.bind("<Configure>", _syncfunc_)

    @property
    def Pos(self):
        return self.winfo_x(), self.winfo_y()

    @property
    def Size(self):
        return self.winfo_width(), self.winfo_height()

class Frame_Config(ezFrame):
    def _ui_init_(self):
        self.sync_geom_with_home: bool = True

        """初始化所有UI控件和样式 —— 深色现代化配置面板"""
        # 主容器(深灰背景)
        self.configure(bg="#2D2D2D")
        self.pack_propagate(False)

        PanelLeft = tkFrame(master=self, bg="#3A3A3A")
        PanelLeft.pack(side="left", fill="both", expand=True, padx=(5, 2.5), pady=5)
        PanelLeft.pack_propagate(False)

        PanelRight = tkFrame(master=self, bg="#3A3A3A")
        PanelRight.pack(side="right", fill="both", expand=True, padx=(2.5, 5), pady=5)
        PanelRight.pack_propagate(False)

        # === 储存所有变量，便于后续读取 ===
        self.config_vars = {}

        # === 主标题 ===
        tkLabel(
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
        Frame_Decision = tkFrame(PanelRight, bg="#3A3A3A")
        Frame_Decision.pack(side="bottom", fill="x", padx=10, pady=(15, 10))

        tkButton(
            Frame_Decision, text="取消", width=10,
            command=lambda: print("取消配置"),
            font=("Microsoft YaHei", 10, "bold"),
            bg="#6C757D", fg="white",
            relief="flat", activebackground="#5A6268"
        ).pack(side="right", padx=(0, 6))

        tkButton(
            Frame_Decision, text="应用", width=10,
            command=self._on_apply,
            font=("Microsoft YaHei", 10, "bold"),
            bg="#28A745", fg="white",
            relief="flat", activebackground="#218838"
        ).pack(side="right")

    def _do_place_(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.configure(width=size[0], height=size[1])
        self.place(x=pos[0], y=pos[1])

    def _on_apply(self):
        """应用配置(示例：打印所有值)"""
        print("\n=== 当前配置 ===")
        for key, var in self.config_vars.items():
            if hasattr(var, 'get'):
                print(f"{key}: {var.get()}")
            else:
                print(f"{key}: {var}")
        print("================\n")

    def AddConfigRow_GroupTitle(self, master, title: str):
        """添加分组标题(类似 Labelframe 的轻量替代)"""
        frame = tkFrame(master, height=30, bg="#3A3A3A")
        frame.pack(fill="x", padx=8, pady=(14, 6))
        tkLabel(
            frame, text=title,
            bg="#3A3A3A", fg="#AAAAAA",
            font=("Microsoft YaHei", 10, "bold")
        ).pack(side="left")

    def AddConfigRow_SplitLine(self, master, color: str = None, height: int = None, padx: tuple[float, float] | float = None, pady: tuple[float, float] | float = None):
        kwargs = {trans[key] if key in (trans:={"color": "bg"}) else key: value for key, value in locals().items() if not key == "self" and not value is None}
        tkFrame(**{key: value for key, value in kwargs.items() if not key in ["padx", "pady"]}).pack(fill="x", **{key: value for key, value in kwargs.items() if key in ["padx", "pady"]})

    def AddConfigRow_Button(self, master, label_text="", button_text="", command=None):
        row = tkFrame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        tkLabel(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)
        tkButton(row, text=button_text, width=12, font=("Microsoft YaHei", 10),
               bg="#4CAF50", fg="white", relief="flat", activebackground="#45a049",
               command=command or (lambda: None)).pack(side="right", padx=(6, 0))

    def AddConfigRow_Slider(self, master, label_text: str, key: str, from_=0, to=100, default=50, unit=""):
        """滑动条(自动绑定 IntVar)"""
        row = tkFrame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        # 标签 + 单位
        label_full = f"{label_text} {default}{unit}" if unit else label_text
        label_widget = tkLabel(row, text=label_full, anchor="w", bg="#3A3A3A", fg="white",
                             font=("Microsoft YaHei", 10))
        label_widget.pack(side="left", fill="x", expand=True)

        var = IntVar(value=default)
        self.config_vars[key] = var

        def on_slider_change(val):
            val = int(float(val))
            text = f"{label_text} {val}{unit}" if unit else f"{label_text} {val}"
            label_widget.config(text=text)

        slider = tkScale(row, from_=from_, to=to, orient="horizontal", length=120,
                       bg="#3A3A3A", fg="white", troughcolor="#555555",
                       highlightthickness=0, sliderrelief="flat",
                       font=("Microsoft YaHei", 9), variable=var,
                       command=on_slider_change)
        slider.pack(side="right", padx=(6, 0))

    def AddConfigRow_Checkbox(self, master, label_text: str, key: str, default=False):
        """复选框(自动绑定 BooleanVar)"""
        row = tkFrame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        var = BooleanVar(value=default)
        self.config_vars[key] = var

        cb = tkCheckbutton(row, text=label_text, variable=var,
                         bg="#3A3A3A", fg="white", selectcolor="#555555",
                         activebackground="#3A3A3A", activeforeground="white",
                         font=("Microsoft YaHei", 10), highlightthickness=0)
        cb.pack(side="left")

    def AddConfigRow_Entry(self, master, label_text: str, key: str, default=""):
        """文本输入框(自动绑定 StringVar)"""
        row = tkFrame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        tkLabel(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)

        var = StringVar(value=default)
        self.config_vars[key] = var

        entry = tkEntry(row, textvariable=var, width=14,
                      font=("Microsoft YaHei", 10),
                      bg="#4A4A4A", fg="white", insertbackground="white",
                      relief="flat")
        entry.pack(side="right", padx=(6, 0))

    def AddConfigRow_Combobox(self, master, label_text: str, key: str, values: list, default: str = ""):
        """下拉框(自动绑定 StringVar)"""
        row = tkFrame(master, height=36, bg="#3A3A3A")
        row.pack(fill="x", padx=10, pady=4)
        row.pack_propagate(False)

        tkLabel(row, text=label_text, anchor="w", bg="#3A3A3A", fg="white",
              font=("Microsoft YaHei", 10)).pack(side="left", fill="x", expand=True)

        var = StringVar(value=default if default in values else (values[0] if values else ""))
        self.config_vars[key] = var

        combo = ttkCombobox(row, textvariable=var, values=values, state="readonly", width=12, font=("Microsoft YaHei", 10))
        combo.pack(side="right", padx=(6, 0))

class Frame_1(ezFrame):
    def _ui_init_(self):
        self.sync_geom_with_home: bool = True

        self.configure(bg="lightgreen")
        self.pack_propagate(False)

        tkLabel(self, text="这是 tkFrame 1", font=("Arial", 16), bg="lightgreen").pack(pady=20)
        tkButton(self, text="切换到 tkFrame 2", command=lambda: self.master.switch("frame_2", lambda frame: frame._do_place_())).pack(pady=10)
    
    def _do_place_(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.configure(width=size[0], height=size[1])
        self.place(x=pos[0], y=pos[1])

class Frame_2(ezFrame):
    def _ui_init_(self):
        self.sync_geom_with_home: bool = True

        self.configure(bg="#448169")
        self.pack_propagate(False)

        tkLabel(self, text="这是 tkFrame 2", font=("Arial", 16), bg="#448169").pack(pady=20)
        tkButton(self, text="切换到 tkFrame 1", command=lambda: self.master.switch("frame_1", lambda frame: frame._do_place_())).pack(pady=10)
    
    def _do_place_(self):
        pos: tuple[int, int] = self.master["frame_Home"].Pos
        size: tuple[int, int] = self.master["frame_Home"].Size
        self.configure(width=size[0], height=size[1])
        self.place(x=pos[0], y=pos[1])

if __name__ == "__main__":
    Root = ezTk("ezTk 测试")
    Root.Geometry.Size(1280, 768)
    Root.Geometry.SizeLimit("min", 1024, 600)
    # Root.Geometry.SizeFix(True, True)

    FrameHub = ezFrameHub(Root)
    FrameHub.configure(switch_mode="redraw")
    FrameHub.add_frame([
        Frame_LeftBar(master=FrameHub, name="frame_LeftBar"),
        Frame_Home(master=FrameHub, name="frame_Home"),
        Frame_Config(master=FrameHub, name="frame_Config"),
        Frame_1(master=FrameHub, name="frame_1"),
        Frame_2(master=FrameHub, name="frame_2")
    ], "frame_Home")
    FrameHub.persist_frame(["frame_LeftBar", "frame_Home", "frame_Config"])

    frame_LeftBar: Frame_LeftBar = FrameHub["frame_LeftBar"]
    frame_Home: Frame_Home = FrameHub["frame_Home"]

    frame_LeftBar.btn_register("主页", "frame_Home")
    frame_LeftBar.btn_register("tkFrame 1", "frame_1")
    frame_LeftBar.btn_register("tkFrame 2", "frame_2")

    Root.mainloop()
