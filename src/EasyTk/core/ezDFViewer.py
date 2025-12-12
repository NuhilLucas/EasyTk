from tkinter import (
    Event as tkEvent,
    Frame as tkFrame,
    Label as tkLabel,
    Menu as tkMenu
)
from tkinter.filedialog import askopenfilename
from tkinter import Entry as tkEntry
from tkinter.ttk import (
    Treeview as ttkTreeview,
    Scrollbar as ttkScrollbar
)
from pandas import (
    read_excel,
    DataFrame,
    Series
)
from os.path import (
    exists as osp_exists
)
from typing import (
    Callable,
    Literal,
    Any
)
from time import time as timestamp

class ezDFViewer(tkFrame):
    def __init__(
            self,
            master = None,
            filter_enable: bool = False,
            sorter_enable: bool = True,
            row_count_limit: int = -1,
            cols_hidden: list[str] | tuple[str] = []
    ):
        super().__init__(master=master)

        self.table: ezTable = ezTable(master=self, filter_enable=filter_enable, sorter_enable=sorter_enable, row_count_limit=row_count_limit, cols_hidden=cols_hidden)
        self.scrollbar_v: ttkScrollbar = self.table.scrollbar_v
        self.scrollbar_h: ttkScrollbar = self.table.scrollbar_h

        self.UIInit()

    def UIInit(self):
        self.table.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_v.grid(row=0, column=1, sticky="ns")
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    @property
    def table_configure(self):
        return self.table

class ezTable(ttkTreeview):
    def __init__(
            self,
            master = None,
            filter_enable: bool = False,
            sorter_enable: bool = True,
            row_count_limit: int = -1,
            cols_hidden: tuple[str] = tuple()
    ):
        super().__init__(master, show="headings", selectmode="none")

        self.current_cell_info: dict[str, tkLabel | str | float] = {
            "current_cell": None,
            "item_id_row": None,
            "item_id_col": None,
            "timestamp": None
        }

        self.edit_cell_info: dict[str, tkEntry | str | int] = {
            "entry_cell": None,
            "item_id_row": None,
            "df_col_index": None
        }

        self.row_count_limit: int = row_count_limit
        self.FILTER_ROW_IID: str = "filter"
        self.BACKGROUND_COLOR: str = "#FFFFFF"
        self.CALL_FROM_CELL_LABEL: str = "call_from_label"
        self.DEFAULT_COL_WIDTH: int = 100

        self.df_origin: DataFrame = None
        self.df_filtered: DataFrame = None
        self.df_display: DataFrame = None

        self.df_size: tuple[int, int] = (0, 0) # (row_count, col_count)
        self.cols_tag: dict[str, int] = dict()
        self.cols_hidden: tuple[str] = cols_hidden
        self.table_row_items: tuple[str] = tuple()

        self.copyer_mode: Literal["ignore", "include", None] = None
        self.copyer_rules: tuple[str] = tuple()

        self.filter_enable: bool = filter_enable
        self.filter_rules: tuple[str] = tuple()

        self.sorter_enable: bool = sorter_enable
        self.sorter_rules: tuple[str, int] = tuple()
        self.sorter_rules_last: tuple[str, int] = tuple()

        self.tagmenu_selected_tag: str = None

        self.scrollbar_v: ttkScrollbar = None
        self.scrollbar_h: ttkScrollbar = None

        self._original_yview: Callable = self.yview
        self._original_xview: Callable = self.xview

        self.event_callback: dict[
            Literal["<OpenFile>", "<DFDataClean>"],
            Callable
        ] = {
            "<OpenFile>": lambda e: None,
            "<DFDataClean>": lambda e: None
        }

        self._ui_init_()

        self._bind_()

        self._register_()

# --------------------------------------------------

    @property
    def columns(self) -> tuple[str]:
        return self["columns"]

# --------------------------------------------------

    def _ui_init_(self):
        self.tagmenu: tkMenu = tkMenu(self, tearoff=0)

    def _bind_(self):
        def scroll_ctrl_take_over():
            self.yview = self._wrapped_yview
            self.xview = self._wrapped_xview
            # self.after(200, scroll_ctrl_give_back)
        def scroll_ctrl_give_back():
            self.yview = self._original_yview
            self.xview = self._original_xview
            self.after(200, scroll_ctrl_take_over)
        scroll_ctrl_take_over()

        self.bind("<Button-1>", self._table_click_callback_)
        self.bind("<Button-3>", self._table_click_callback_)
        self.bind("<Double-1>", self._table_dbclick_callback_)

        def _(e):
            self.unbind("<MouseWheel>")
            self.after(10, lambda: self.bind("<MouseWheel>", _))
            self.after(30, self._edit_save_)
            self.after(30, self._current_cell_pos_sync_)
        self.bind("<MouseWheel>", _)

        self.bind("<Return>", lambda e: (self._edit_cell_(self.CALL_FROM_CELL_LABEL), self.focus_set()))

        # 绑定方向键
        self.bind("<Up>", self._table_arrow_key_callback_)
        self.bind("<Down>", self._table_arrow_key_callback_)
        self.bind("<Left>", self._table_arrow_key_callback_)
        self.bind("<Right>", self._table_arrow_key_callback_)

        # 可选：也绑定小键盘方向键（如果需要）
        self.bind("<KP_Up>", self._table_arrow_key_callback_)
        self.bind("<KP_Down>", self._table_arrow_key_callback_)
        self.bind("<KP_Left>", self._table_arrow_key_callback_)
        self.bind("<KP_Right>", self._table_arrow_key_callback_)

        self.bind("<Control-c>", self._table_shortcuts_callback_)

    def _register_(self):
        self.scrollbar_register()
        if self.sorter_enable: self._sorter_register_()

    def _table_click_callback_(self, event: tkEvent = None):
        match self.identify("region", event.x, event.y):
            case "cell":
                if event.num == 1: self._select_cell_(event)
            case "heading":
                if event.num == 3: self._show_tagmenu_(event)

    def _table_dbclick_callback_(self, event: tkEvent = None):
        match self.identify("region", event.x, event.y):
            case "nothing":
                if self.df_origin is None: self._open_file_(event)

    def _table_arrow_key_callback_(self, event: tkEvent = None):
        if event.keycode in [37, 38, 39, 40]:
            self._move_cell_cursor_(event)

    def _table_shortcuts_callback_(self, event: tkEvent = None):
        match event.state, event.keysym:
            case 4, "c":
                self.copyer()

# --------------------------------------------------

    def _wrapped_yview(self, *args: tuple, **kwargs: dict):
        result: Any = self._original_yview(*args, **kwargs)

        self.after(30, self._edit_save_)
        self.after(30, self._current_cell_pos_sync_)

        return result

    def _wrapped_xview(self, *args: tuple, **kwargs: dict):
        result: Any =  self._original_xview(*args, **kwargs)

        self.after(30, self._edit_save_)
        self.after(30, self._current_cell_pos_sync_)

        return result

    def _open_file_(self, event: tkEvent = None):
        path_file = askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls")]
        )

        if not osp_exists(path_file): return

        try:
            df_origin: DataFrame = read_excel(io=path_file)
            if formated_df:=self.event_callback["<DFDataClean>"](df_origin) is None:
                df_origin =  df_origin.fillna("")
            else:
                df_origin = formated_df
        
            self.df_origin: DataFrame = df_origin
            self.df_filtered = self.df_origin.copy()
            self.df_display = self.df_filtered if self.row_count_limit < 0 else self.df_filtered[: self.row_count_limit]
            self.df_size = self.df_display.shape
            self.cols_tag = {col_tag: col_index for col_index, col_tag in enumerate(self.df_display.columns.to_list())}
        except Exception as E:
            print(str(E))
        else:
            self.event_callback["<OpenFile>"](None)
            self.display()

    def _select_cell_(self, event: tkEvent = None):
        # 单击单元格后的 150ms 内单击标签
        if event == self.CALL_FROM_CELL_LABEL:
            if (
                not self.current_cell_info["timestamp"] is None and
                not self.current_cell_info["current_cell"] is None and
                timestamp()-self.current_cell_info["timestamp"] < 0.150
            ):
                self._edit_cell_(self.CALL_FROM_CELL_LABEL)
            return
        
        self.current_cell_info["timestamp"] = timestamp()

        item_id_row: str = self.identify_row(event.y)
        item_id_col: str = self.identify_column(event.x)
        if not item_id_row or not item_id_col: return
        # tree_item_pos: tuple[str, str] = (item_id_row, item_id_col)

        # df_row_index: int = item_id_row
        df_col_index: int = int(item_id_col[1:]) - 1
        # df_cell_pos: tuple[int, int] = (df_row_index, df_col_index)

        if not (current_cell:=self.current_cell_info["current_cell"]) is None:
            current_cell.destroy()
            self.current_cell_info.update({
                "current_cell": None,
                "item_id_row": None,
                "item_id_col": None
            })

        current_cell: tkLabel = tkLabel(
            self,
            bg=self.BACKGROUND_COLOR,
            text=self.item(item_id_row, "values")[df_col_index],
            relief="solid",
            borderwidth=1,
            anchor="w",
            padx=3
        )
        x, y, w, h = self.bbox(item_id_row, item_id_col)
        current_cell.place(x=x, y=y, width=w, height=h)

        current_cell.bind("<Button-1>", lambda e: self._select_cell_(self.CALL_FROM_CELL_LABEL))
        current_cell.bind("<Double-1>", lambda e: self._edit_cell_(self.CALL_FROM_CELL_LABEL))

        self.current_cell_info.update({
            "current_cell": current_cell,
            "item_id_row": item_id_row,
            "item_id_col": item_id_col
        })

    def _edit_cell_(self, event: tkEvent = None):
        # 从当前单元格的单击事件创建出的 Label 而来的双击事件.
        item_id_row: str = self.current_cell_info["item_id_row"]
        item_id_col: str = self.current_cell_info["item_id_col"]
        if not item_id_row or not item_id_col: return
        # tree_item_pos: tuple[str, str] = (item_id_row, item_id_col)

        # df_row_index: int = item_id_row
        df_col_index: int = int(item_id_col[1:]) - 1
        # df_cell_pos: tuple[int, int] = (df_row_index, df_col_index)

        entry_cell: tkEntry = tkEntry(
            self,
            bg="#D9D9D9",
            fg="#000000",
            insertbackground="white",
            relief="flat",
            borderwidth=0
        )
        x, y, w, h = self.bbox(item_id_row, item_id_col)
        entry_cell.place(x=x, y=y, width=w, height=h)
        entry_cell.insert(0, self.item(item_id_row, "values")[df_col_index])
        entry_cell.select_range(0, "end")
        entry_cell.focus()

        entry_cell.bind("<Return>", self._edit_save_)
        entry_cell.bind("<FocusOut>", self._edit_save_)

        self.edit_cell_info = {
            "entry_cell": entry_cell,
            "item_id_row": item_id_row,
            "df_col_index": df_col_index
        }

    def _edit_save_(self, event: tkEvent = None):
        if self.edit_cell_info["entry_cell"] is None: return

        entry_cell: tkEntry = self.edit_cell_info["entry_cell"]
        item_id_row: str = self.edit_cell_info["item_id_row"]
        df_col_index: int = self.edit_cell_info["df_col_index"]

        entry_value: str = entry_cell.get()

        self.current_cell_info["current_cell"].configure(text=entry_value)

        tree_colvalue_list = list(self.item(item_id_row, "values"))
        tree_colvalue_list[df_col_index] = entry_value
        self.item(item_id_row, values=tree_colvalue_list)

        entry_cell.destroy()

        self.edit_cell_info = {
            "entry_cell": None,
            "item_id_row": None,
            "df_col_index": None
        }

        if item_id_row == self.FILTER_ROW_IID: self.display()

        self.focus_set()

    def _move_cell_cursor_(self, event: tkEvent = None):
        if self.current_cell_info["current_cell"] is None: return

        item_id_row: str = self.current_cell_info["item_id_row"]
        item_id_col: str = self.current_cell_info["item_id_col"]

        match event.keycode:
            case 38: # <Up>
                if (row_item_index_above:=self.table_row_items.index(item_id_row)-1) < 0: return
                item_id_row = self.table_row_items[row_item_index_above]
            case 40: # <Down>
                if (row_item_index_below:=self.table_row_items.index(item_id_row)+1) >= self.table_row_items.__len__(): return
                item_id_row = self.table_row_items[row_item_index_below]
            case 37: # <Left>
                for col_item in reversed(self.columns[: self.columns.index(item_id_col)]):
                    if self.column(col_item, "width") == 0: continue
                    item_id_col = col_item
                    break
                else: return
            case 39: # <Right>
                for col_item in self.columns[self.columns.index(item_id_col)+1:]:
                    if self.column(col_item, "width") == 0: continue
                    item_id_col = col_item
                    break
                else: return
        self.current_cell_info["item_id_col"] = item_id_col
        self.current_cell_info["item_id_row"] = item_id_row
        self._move_cell_view_follow_()

    def _move_cell_view_follow_(self, event: tkEvent = None):
        if not self.current_cell_info["current_cell"]: return

        item_id_row: str = self.current_cell_info["item_id_row"]
        item_id_col: str = self.current_cell_info["item_id_col"]

        xywh: tuple[int, int, int, int] | str = self.bbox(item_id_row, item_id_col)
        if xywh == "":
            if item_id_row and item_id_col: self.after(10, self._current_cell_pos_sync_)
            return
        x, y, w, h = self.bbox(item_id_row, item_id_col)

        cell_t, cell_b, cell_l, cell_r = y, y+h, x, x+w

        # 上超限 | 下超限 控件本身支持视口跟随
        # 左超限
        if cell_l < 0:
            scroll_x: float = self.xview()[0]
            table_w: int = sum([self.column(col_item, "width") for col_item in self.columns])
            self.xview_moveto(scroll_x + cell_l / table_w)
        # 右超限
        elif cell_r > (table_view_w:=self.winfo_width()):
            scroll_x: float = self.xview()[0]
            table_w: int = sum([self.column(col_item, "width") for col_item in self.columns])
            self.xview_moveto(scroll_x + (cell_r - table_view_w) / table_w)
        self.after(10, self._current_cell_pos_sync_)

    def _current_cell_pos_sync_(self, event: tkEvent = None):
        if not self.current_cell_info["current_cell"]: return

        item_id_row: str = self.current_cell_info["item_id_row"]
        item_id_col: str = self.current_cell_info["item_id_col"]
        df_col_index: int = int(item_id_col[1:]) - 1

        xywh: tuple[int, int, int, int] | str = self.bbox(item_id_row, item_id_col)
        # 超出视口区域, 无法定位到单元格坐标
        if xywh == "":
            self.current_cell_info["current_cell"].place_forget()
            return
        x, y, w, h = xywh

        self.current_cell_info["current_cell"].place(x=x, y=y, width=w, height=h)
        self.current_cell_info["current_cell"].configure(text=self.item(item_id_row, "values")[df_col_index])

    def _show_tagmenu_(self, event: tkEvent = None):
        self.tagmenu.post(event.x_root, event.y_root)
        self.tagmenu_selected_tag = list(self.cols_tag)[self.columns.index(self.identify_column(event.x))]
        self.tagmenu.grab_release()

    def set_row_count_limit(self, limit: int = -1):
        if not isinstance(limit, int): return
        self.row_count_limit = limit
        self.display()

    def add_hidden_cols(self, cols_name: list[str] | tuple[str] | str):
        if isinstance(cols_name, str):
            cols_name = (cols_name,)
        elif isinstance(cols_name, list):
            cols_name = tuple(cols_name)
        elif isinstance(cols_name, tuple):
            pass
        else:
            return

        self.cols_hidden = tuple(set(self.cols_hidden + cols_name))
        for col_name in cols_name:
            self.column("#"+str(self.cols_tag[col_name]+1), width=0, stretch=False)

    def cls_hidden_cols(self):
        self.cols_hidden = tuple()
        for col_tag, col_index in self.cols_tag.items():
            self.column("#"+str(col_index+1), width=self.DEFAULT_COL_WIDTH, stretch=False)

    def display(self):
        # Clear Current Treeview Data
        if self.get_children():
            do_refresh: list[bool, bool] = [True, True]
            if self.filter_enable:
                if not self.filter(): do_refresh[0] = False
            if self.sorter_enable:
                if not self.sorter(): do_refresh[1] = False
            if not any(do_refresh): return

        self.clear("display")

        # Set Cols Tag
        self["columns"] = ["#"+str(col_index+1) for _, col_index in self.cols_tag.items()]
        for col_tag, col_index in self.cols_tag.items():
            self.heading("#"+str(col_index+1), text=col_tag)
            self.column("#"+str(col_index+1), width=0 if col_tag in self.cols_hidden else self.DEFAULT_COL_WIDTH, stretch=False)

        # Data Display
        if self.filter_enable: self._filter_register_()
        for row_index, row_df in self.df_display.iterrows():
            self.insert("", "end", iid=row_index, values=list(row_df.astype(str)))

        self.table_row_items = self.get_children()

        # 重新设置因为刷新表格而丢失的焦点行
        if self.current_cell_info["item_id_row"]: self.focus(self.current_cell_info["item_id_row"])

    def clear(self, mode: Literal["all", "display"]):
        for item in self.get_children(): self.delete(item)
        
        if mode == "display": return

        self.current_cell_info: dict[str, tkLabel | str | float] = {
            "current_cell": None,
            "item_id_row": None,
            "item_id_col": None,
            "timestamp": None
        }

        self.edit_cell_info: dict[str, tkEntry | str | int] = {
            "entry_cell": None,
            "item_id_row": None,
            "df_col_index": None
        }

        self.df_size: tuple[int, int] = (0, 0)
        self.cols_tag: dict[str, int] = dict()
        self.cols_hidden: tuple[str] = tuple()
        self.table_row_items: tuple[str] = tuple()

        self.copyer_rules: tuple[str] = tuple()
        self.filter_rules: tuple[str] = tuple()
        self.sorter_rules: tuple[str, int] = tuple()
        self.sorter_rules_last: tuple[str, int] = tuple()

    def tagmenu_add_command(self, label: str, command: Callable = lambda: None):
        def _(*args, **kwargs):
            result: Any = command(*args, **kwargs)
            self.tagmenu_selected_tag = None
            return result
        self.tagmenu.add_command(label=label, command=_)

    def scrollbar_register(self, mode: bool = True):
        self.scrollbar_v = ttkScrollbar(self.master, orient="vertical", command=self.yview)
        self.scrollbar_h = ttkScrollbar(self.master, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)

    def copyer(self):
        if self.copyer_mode is None:
            self._copy_current_cell_()
        else:
            self._copy_cell_with_rule_()

    def copyer_config(self, mode: Literal["ignore", "include", None] = None, rules: tuple[str] = tuple()):
        self.copyer_mode = mode
        self.copyer_rules = rules

    def _copy_current_cell_(self):
        if not self.current_cell_info["current_cell"]: return

        self.clipboard_clear()
        self.clipboard_append(self.current_cell_info["current_cell"]["text"])

    def _copy_cell_with_rule_(self):
        values: list[str] = []
        if self.copyer_mode == "ignore":
            for col_tag, col_index in self.cols_tag.items():
                if col_tag in self.copyer_rules: continue
                values.append(self.set(self.current_cell_info["item_id_row"], "#"+str(col_index+1)))
        if self.copyer_mode == "include":
            for col_tag, col_index in self.cols_tag.items():
                if not col_tag in self.copyer_rules: continue
                values.append(self.set(self.current_cell_info["item_id_row"], "#"+str(col_index+1)))
        self.clipboard_clear()
        self.clipboard_append("\t".join(values))

    def filter(self, invert: bool = False) -> bool:
        # return a state, indicate is it necessary to refresh.
        filter_rules: tuple[str] = self.item(self.FILTER_ROW_IID, 'values')
        
        if filter_rules == self.filter_rules:
            return False
        elif not any(filter_rules) and filter_rules != self.filter_rules:
            self.df_filtered = self.df_origin.copy()
            self.df_display = self.df_filtered if self.row_count_limit < 0 else self.df_filtered[: self.row_count_limit]
            self.df_size = self.df_display.shape
            self.filter_rules = filter_rules
            return True
        else:
            columns: list[int] = [col_index for col_tag, col_index in self.cols_tag.items()]
            mask = Series([True] * len(self.df_origin))
            for index, filter_text in enumerate(filter_rules):
                col_index = columns[index]
                if filter_text == "": continue
                col_series = self.df_origin.iloc[:, col_index]
                mask &= col_series.astype(str).str.contains(filter_text, case=False, na=False)
            if invert:
                mask = ~mask
            self.df_filtered = self.df_origin.copy()[mask]
            self.df_display = self.df_filtered if self.row_count_limit < 0 else self.df_filtered[: self.row_count_limit]
            self.df_size = self.df_display.shape
            self.filter_rules = filter_rules
            return True

    def _filter_register_(self, mode: bool = True):
        match mode:
            case True:
                if self.exists(self.FILTER_ROW_IID): return
                self.insert("", 0, iid=self.FILTER_ROW_IID, values=self.filter_rules if self.filter_rules else [""]*self.df_size[1])
            case False:
                if not self.exists(self.FILTER_ROW_IID): return
                self.delete(self.FILTER_ROW_IID)

    def switch_filter(self, mode: Literal["enable", "disable", True, False]):
        filter_enable = True if mode == "enable" or mode is True else False
        if self.filter_enable == filter_enable: return
        self.filter_enable = filter_enable
        self._filter_register_(filter_enable)

    def sorter(self):
        # return a state, indicate is it necessary to refresh.
        if self.sorter_rules == self.sorter_rules_last: return False

        if not self.sorter_rules:
            self.df_display = self.df_filtered if self.row_count_limit < 0 else self.df_filtered[: self.row_count_limit]
        else:
            if not self.sorter_rules[0] in self.cols_tag: return False
            self.df_display = (df_filtered:=self.df_filtered.sort_values(by=self.sorter_rules[0], ascending=self.sorter_rules[1])) if self.row_count_limit < 0 else df_filtered[: self.row_count_limit]

        self.sorter_rules_last = self.sorter_rules

        return True

    def _sorter_register_(self, mode: bool = True):
        def _(mode: Literal[True, False, None]):
            """ mode: Literal[True, False, None] -> [ascending, descending, unsort]
            """
            self.sorter_rules = () if mode is None else (self.tagmenu_selected_tag, mode)
            self.display()
        self.tagmenu_add_command(label="升序", command=lambda: _(True))
        self.tagmenu_add_command(label="降序", command=lambda: _(False))
        self.tagmenu_add_command(label="取消排序", command=lambda: _(None))
        self.tagmenu_add_command(label="隐藏此列", command=lambda: self.add_hidden_cols(cols_name=self.tagmenu_selected_tag))
        self.tagmenu_add_command(label="取消隐藏", command=self.cls_hidden_cols)

    def switch_sorter(self, mode: Literal["enable", "disable", True, False]):
        sorter_enable = True if mode == "enable" or mode is True else False
        if self.sorter_enable == sorter_enable: return
        self.sorter_enable = sorter_enable
        self._sorter_register_(self.sorter_enable)

    def bind(
            self,
            sequence: Literal["<OpenFile>", "<DFDataClean>"] = None,
            func = None,
            add = None
    ) -> str | None:
        match sequence:
            case "<OpenFile>":
                self.event_callback["<OpenFile>"] = func
            case "<DFDataClean>":
                self.event_callback["<DFDataClean>"] = func
            case _:
                return super().bind(sequence=sequence, func=func, add=add)

    def unbind(
            self,
            sequence: Literal["<OpenFile>", "<DFDataClean>"],
            funcid = None
    ) -> None:
        match sequence:
            case "<OpenFile>":
                self.event_callback["<OpenFile>"] = lambda e: None
            case "<DFDataClean>":
                self.event_callback["<DFDataClean>"] = lambda e: None
            case _:
                return super().unbind(sequence, funcid)

    def debug(self, mode: Literal[
        "print_focus",
        "print_mouse_pos"
    ]):
        match mode:
            case "print_focus":
                def _():
                    print(root.focus_get())
                    root.after(1000, _)
                root.after(1000, _)
            case "print_mouse_pos":
                def _(event: tkEvent):
                    print(event.x, event.y)
                root.bind("<Motion>", _)

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.geometry("800x600")
    df_viewer = ezDFViewer(
        master=root,
        filter_enable=True,
        sorter_enable=True,
        row_count_limit=-1,
        cols_hidden=("仓库名称", "货品中类", "期初正品", "转入正品", "转出正品", "盈亏正品")
    )
    df_viewer.pack(fill=tk.BOTH, expand=True)
    df_viewer.table_configure.copyer_config(mode="ignore", rules=("仓库名称", "货品中类", "期初正品", "转入正品", "转出正品", "盈亏正品"))
    root.mainloop()
