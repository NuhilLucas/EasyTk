from tkinter import Tk
from typing import Literal
from EasyTk.core.function import get_temp_root, destroy_temp_root

# icons
ICONS = Literal["error", "info", "question", "warning"]
ERROR = "error"
INFO = "info"
QUESTION = "question"
WARNING = "warning"

# types
TYPES = Literal["abortretryignore", "ok", "okcancel", "retrycancel", "yesno", "yesnocancel"]
ABORTRETRYIGNORE = "abortretryignore"
OK = "ok"
OKCANCEL = "okcancel"
RETRYCANCEL = "retrycancel"
YESNO = "yesno"
YESNOCANCEL = "yesnocancel"

# replies
REPLIES = Literal["abort", "retry", "ignore", "ok", "cancel", "yes", "no"]
ABORT = "abort"
RETRY = "retry"
IGNORE = "ignore"
OK = "ok"
CANCEL = "cancel"
YES = "yes"
NO = "no"

def MsgBox(
        master: Tk | None = None,
        title: str = "MsgBox",
        message: str = "",
        icon: ICONS = "",
        type: TYPES = "",
        mode: Literal["info", "warn", "error", "query"] = "",
        **options
    ):
    master: Tk = master
    _options: dict = {
        "title": title,
        "message": message
    }

    match mode:
        case "info":
            _options.update({
                "icon": INFO,
                "type": OK
            })
        case "warn":
            _options.update({
                "icon": WARNING,
                "type": OK
            })
        case "error":
            _options.update({
                "icon": ERROR,
                "type": OK
            })
        case "query":
            _options.update({
                "icon": "question",
                "type": YESNO
            })
        case _:
            _options.update({
                "icon": icon,
                "type": type
            })
    _options.update(options)

    master: Tk = get_temp_root() if master is None else master
    result = "NoResult"
    try:
        result = master.tk.call("tk_messageBox", *master._options(_options))
    finally:
        destroy_temp_root(master)

    return result

# --------------------------------------------------------------------
# test stuff

if __name__ == "__main__":
    print(MsgBox(title="asd", message="asdasd", icon="info", type="yesnocancel"))
