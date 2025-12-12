from EasyTk import ezTk
from tkinter import (
    Tk,
    Entry as tkEntry,
    Frame as tkFrame,
    Button as tkButton,
    BooleanVar as tkBooleanVar,
    StringVar as tkStringVar,
    Event as tkEvent
)
from tkinter.ttk import (
    Checkbutton as ttkCheckbutton
)
from typing import (
    Any,
    Callable
)

class ezCheckoxList(tkFrame):
    def __init__(
            self,
            master: Tk | ezTk,
            master_top: Tk | ezTk,
            options: tuple | list | dict = None,
            command: Callable = lambda index, item_state, selected_indexes, selected_values: None,
            **kwargs: dict
    ):
        super().__init__(master, **kwargs)

        self.master: Tk | ezTk = master
        self.master_top: Tk | ezTk = master_top if master_top else master

        self.COLOR_BACKGROUND: str = "#DDDDDD"
        self.ICON_BTN: tuple[str, str] = ("▼", "▲")
        self.PANEL_ITEM_HEIGHT: int = 100

        self.command: Callable = command

        self.kwargs: dict = kwargs

        self.panel_displayed: bool = False

        self._ui_init_(options=options)
        self._bind_()

    def _ui_init_(self, options: tuple | list | dict = None):
        self.entry_box_text: tkStringVar = tkStringVar(master=self)

        self.combo_box: ezCombobox = ezCombobox(
            master=self,
            ctrler=self,
            **self.kwargs
        )

        self.item_panel: ezItemsPanel = ezItemsPanel(
            master=self.master_top,
            ctrler=self,
            options=options,
            **self.kwargs
        )

        self.combo_box.pack(fill="both", expand=True)

    def _bind_(self):
        self.master_top.bind("<Configure>", lambda e: self.item_panel.place_panel(*self.combo_box.get_geom()))

    def show_panel(self, event: tkEvent = None):
        if self.panel_displayed:
            self.panel_displayed = False
            self.combo_box.trig_btn.configure(text=self.ICON_BTN[0])
            self.item_panel.place_forget()
        else:
            if not self.item_panel.options: return
            self.panel_displayed  = True
            self.combo_box.trig_btn.configure(text=self.ICON_BTN[1])
            self.item_panel.place_panel(*self.combo_box.get_geom())

    def hook_select_event(self, index: int, item_state: tkBooleanVar, selected_indexes: set, selected_values: tuple):
        self.command(index, item_state, selected_indexes, selected_values)

    def set_options(self, options: tuple | list | dict = None):
        self.item_panel.set_options(options)

    def get_options(self) -> dict:
        return self.item_panel.options

    def get_options_selected_values(self):
        return self.item_panel.selected_values

class ezCombobox(tkFrame):
    def __init__(
            self,
            master: Tk | ezTk = None,
            ctrler: ezCheckoxList = None,
            **kwargs: dict
    ):
        super().__init__(master=master, **kwargs)

        self.master: Tk | ezTk = master
        self.ctrler: ezCheckoxList = ctrler

        self._ui_init_()

        self._bind_()

    def _ui_init_(self):
        self.configure(bg=self.ctrler.COLOR_BACKGROUND)

        self.entry_box: tkEntry = tkEntry(
            master=self,
            bg=self.ctrler.COLOR_BACKGROUND,
            textvariable=self.ctrler.entry_box_text,
            state="readonly"
        )
        self.btn_frame: tkFrame = tkFrame(
            master=self,
            bg=self.ctrler.COLOR_BACKGROUND
        )
        self.btn_frame.pack_propagate(False)
        self.trig_btn: tkButton = tkButton(
            master=self.btn_frame,
            text=self.ctrler.ICON_BTN[0],
            anchor="center",
            command=self.ctrler.show_panel
        )

        self.entry_box.pack(fill="both", side="left", expand=True)
        self.btn_frame.pack(fill="both", side="right", expand=False)
        self.trig_btn.pack(fill="both", expand=True)

    def _bind_(self):
        self.btn_frame.bind("<Map>", self._sync_btn_frame_width_)

    def _sync_btn_frame_width_(self, event: tkEvent = None):
        self.btn_frame.configure(width=self.btn_frame.winfo_height())

    def get_geom(self):
        return self.winfo_rootx(), self.winfo_rooty(), self.winfo_width(), self.winfo_height()

class ezItemsPanel(tkFrame):
    def __init__(
            self,
            master: Tk | ezTk = None,
            ctrler: ezCheckoxList = None,
            options: tuple | list | dict = dict(),
            **kwargs: dict
    ):
        super().__init__(master=master, **kwargs)

        self.master: Tk | ezTk = master
        self.ctrler: ezCheckoxList = ctrler

        self.options: dict[Any, Any] = self._format_options_(options)
        self.options_item: dict[Any, tuple[tkBooleanVar, ttkCheckbutton]] = dict()

        self.selected_indexes: set = set()
        self.selected_values: tuple = tuple()

        self._ui_init_()

    def _ui_init_(self):
        self._items_register_()

    def _items_register_(self):
        for index, option in self.options.items():
            bool_var = tkBooleanVar()
            check_btn = ttkCheckbutton(
                master=self,
                text=str(option),
                variable=bool_var,
                style="Modern.TCheckbutton",
                command=lambda index=index, bool_var=bool_var: self._items_select_(index, bool_var.get())
            )
            check_btn.pack(fill="x", anchor="w", padx=2, pady=1)
            self.options_item.update({index: (bool_var, check_btn)})

    def _items_select_(self, index: int, item_state: tkBooleanVar):
        if item_state: self.selected_indexes.add(index)
        else: self.selected_indexes.discard(index)

        self.selected_values = (self.options[index] for index in self.selected_indexes)
        self.ctrler.entry_box_text.set("; ".join(self.selected_values))
        self.ctrler.hook_select_event(index, item_state, self.selected_indexes, self.selected_values)

    def cls_options(self):
        self.options.clear()
        for indexa, item in self.options_item.items(): item[1].destroy()
        self.options_item.clear()
        self.selected_indexes.clear()
        self.selected_values = tuple()

    def set_options(self, options: dict):
        self.cls_options()
        self.options = self._format_options_(options)
        self._items_register_()

    def _format_options_(self, options: tuple | dict | None) -> dict:
        if options is None:
            options = dict()
        elif isinstance(options, tuple) or isinstance(options, list) or isinstance(options, dict):
            options = {index: option for index, option in enumerate(options)}
        else:
            raise Exception()
        return options

    def place_panel(
            self,
            x: int,
            y: int,
            width: int,
            height: int
    ):
        if not self.ctrler.panel_displayed: return
        self.place(x=x-self.master.winfo_rootx(), y=y-self.master.winfo_rooty()+height, width=width)
        self.tkraise()

if __name__ == "__main__":
    from EasyTk import ezTk
    root = ezTk()
    root.Geometry.Pos(0, 0)
    root.Geometry.Size(400, 300)
    
    root.configure(bg="#B92A2A")

    options = [
        "Document Processing",
        "Data Analysis",
        "Image Recognition",
        "Natural Language Processing",
        "Predictive Modeling",
        "Network Security",
        "Cloud Integration",
        "Mobile Optimization"
    ]

    checkbox_list = ezCheckoxList(
        master=root,
        master_top=root,
        command=lambda a, b, c, d: print(b),
        bg="#929292",
        height=30,
    )
    checkbox_list.set_options(options)
    checkbox_list.pack()

    root.mainloop()