from tkinter import Tk
from tkinter import _get_temp_root, _destroy_temp_root

def get_temp_root() -> Tk:
    """_用于创建一个临时的不可见 Tk 实例 ( root.withdraw() )._
    #### 要求:
    - 当前全局不存在任何 Tk 默认根实例, 即满足 tkinter.init.py 中的
    ```
    _default_root is None # Tk 实例创建后 _default_root 会被指定为实例本身
    _support_default_root is Ture
    ```
    - 否则会因 _support_default_root 的错误状态抛出 RuntimeError
    ```
    if not _support_default_root:
        raise RuntimeError("No master specified and tkinter is "
                           "configured to not support default root")
    ```
    - 或是会因以下断言抛出 AssertionError 异常
    ```
    assert _support_default_root
    assert _default_root is None
    ```
    - 创建的 root 不可见且被标记为 _temporary
    ```
    root.withdraw()
    root._temporary = True
    ```
        
    Returns:
        Tk: _创建的 Tk 实例._
    """
    return _get_temp_root()

def destroy_temp_root(master: Tk |None) -> None:
    """_用于移除传入的临时Tk根实例_
    #### 要求:
    - 当前传入的 Tk 实例具有属性 _temporary 且为 False
    ```
    getattr(master, '_temporary', False)
    ```
    """

    return _destroy_temp_root(master)
