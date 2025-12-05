# 🎨 EasyTk - 优雅的 Python GUI 开发框架

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/EasyTk.svg)](https://pypi.org/project/EasyTk/)
[![Downloads](https://static.pepy.tech/badge/easytk)](https://pepy.tech/project/easytk)
[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/NuhilLucas/EasyTk)
</div>

---

## 🚀 特性亮点

<div align="center">

| 特性 | 描述 | 图标 |
|------|------|------|
| **🎯 简化窗口管理** | 通过 `ezTk` 类轻松创建和管理应用程序窗口 | 🪟 |
| **🧩 模块化框架系统** | 使用 `ezFrame` 和 `ezFrameManager` 实现灵活的界面组织 | 🧱 |
| **💬 智能消息系统** | 内置 `MsgBox` 系统，支持多种消息类型和交互模式 | 📢 |
| **📐 智能几何管理** | 提供窗口位置、大小和限制的便捷操作方法 | 📏 |
| **🌙 现代化界面** | 支持深色主题和现代化 UI 设计 | 🎨 |
| **⚡ 高性能** | 轻量级实现，启动快速，资源占用低 | ⚡ |

</div>

## 📦 安装指南

### 方式一：使用 Poetry（推荐）
```bash
poetry add EasyTk
```

### 方式二：使用 pip
```bash
pip install EasyTk
```

### 系统要求
- **Python**: 3.12 或更高版本
- **依赖项**: Pillow >= 11.3.0

---

## 🎮 快速入门

### 基础窗口创建 - 只需 3 行代码！

```python
from EasyTk import ezTk

# 创建你的第一个 EasyTk 窗口
app = ezTk("我的第一个 EasyTk 应用")
app.Geometry.Size(800, 600)  # 设置窗口大小
app.Run()  # 启动应用！
```

### 多框架架构示例

```python
from EasyTk import ezTk, ezFrame, ezFrameManager
from tkinter import Label, Button, Frame
import tkinter as tk

class HomePage(ezFrame):
    """主页框架示例"""
    
    def UIInit(self):
        # 创建主框架
        self.Frame = Frame(master=self.master, name=self.name, bg="#f0f0f0")
        
        # 添加内容
        Label(self.Frame, text="🚀 欢迎使用 EasyTk！", 
              font=("Arial", 24, "bold"), fg="#2c3e50").pack(pady=40)
        
        Label(self.Frame, text="一个让 tkinter 开发更简单的 Python 框架",
              font=("Arial", 14), fg="#7f8c8d").pack(pady=10)
        
        Button(self.Frame, text="👉 开始探索", 
               font=("Arial", 12), bg="#3498db", fg="white",
               padx=20, pady=10).pack(pady=20)
    
    def DoPlace(self):
        self.Frame.pack(fill="both", expand=True)

# 创建主窗口
app = ezTk("多框架应用示例")
app.Geometry.Size(1000, 700)

# 创建框架管理器
frame_manager = ezFrameManager(app)

# 添加框架并设置主页
frame_manager.AddFrame([
    HomePage(master=frame_manager, name="home")
], "home")

# 运行应用
app.Run()
```

---

## 📚 EasyTk 核心组件详解

### 概述

EasyTk 是一个基于 tkinter 的 Python GUI 框架，旨在简化桌面应用程序的开发。其核心组件提供了窗口管理、框架系统和消息框功能，让开发者能够更高效地构建复杂的用户界面。
### 1. ezTk 窗口管理器

#### 核心功能

[`ezTk`](src/EasyTk/ezTk.py#L7) 类是整个框架的窗口管理核心，继承自 `tkinter.Tk`：

```python
class ezTk(Tk):
    def __init__(self, title: str = "Window"):
        super().__init__()
        self.wm_title(title)
        self.protocol("WM_DELETE_WINDOW", lambda: self.Exit("All"))
        self.Geometry: ezTk_Geometry = ezTk_Geometry(self)
```

#### 特性亮点

1. **自动窗口关闭处理**：通过 [`protocol("WM_DELETE_WINDOW")`](src/EasyTk/ezTk.py#L11) 统一处理窗口关闭事件
2. **几何管理封装**：[`ezTk_Geometry`](src/EasyTk/ezTk.py#L26) 类提供简洁的窗口尺寸和位置控制

##### 几何管理API

[`ezTk_Geometry`](src/EasyTk/ezTk.py#L26) 类提供了四个主要方法：

- **`Pos(x, y, update)`**：控制窗口位置，支持相对坐标设置
- **`Size(width, height, update)`**：设置窗口尺寸
- **`SizeFix(width, height)`**：固定窗口大小
- **`SizeLimit(mode, width, height)`**：设置最小/最大尺寸限制

### 2. ezFrame 框架架构

#### 抽象基类设计

[`ezFrame`](src/EasyTk/ezFrame.py#L10) 是一个抽象基类，采用模板方法模式：

```python
class ezFrame(ABC):
    def __init__(self, master: ezFrameManager = None, name: str = "ezFrame", **kwargs):
        self.master = master
        self.name = name
        self.kwargs = kwargs
        self.Frame = None
    
    @abstractmethod
    def UIInit(self):
        """必须在子类中实现，用于初始化UI组件"""
        pass
```

#### 钩子方法体系

提供了三个生命周期钩子：

1. **[`UIInit()`](src/EasyTk/ezFrame.py#L22)**：必需的抽象方法，初始化UI组件
2. **[`DoPlace()`](src/EasyTk/ezFrame.py#L28)**：可选的布局方法
3. **[`OtherHook()`](src/EasyTk/ezFrame.py#L31)**：自定义扩展钩子

#### 绘制流程

[`draw()`](src/EasyTk/ezFrame.py#L34) 方法按顺序执行三个钩子，确保组件正确渲染。

### 3. ezFrameManager 框架管理系统

#### 双模式切换机制

[`ezFrameManager`](src/EasyTk/ezFrame.py#L85) 支持两种框架切换模式：

```python
self._SwitchMode_: Literal["tkraise", "redraw"] = "tkraise"
```

- **tkraise 模式**：所有框架预先绘制，通过 `tkraise()` 方法切换显示
- **redraw 模式**：按需绘制框架，切换时销毁旧框架并绘制新框架

#### 框架列表管理

[`ezFrameList`](src/EasyTk/ezFrame.py#L40) 类提供了灵活的框架索引管理：

- **双索引系统**：同时支持名称索引和数字索引
- **便捷访问**：支持 `[0]` 访问第一个，`[1]` 访问最后一个
- **迭代器支持**：可遍历所有框架

#### 持久化框架

[`frames_persisted`](src/EasyTk/ezFrame.py#L102) 列表维护常驻内存的框架，在切换模式下不会被销毁。

### 4. ezMsgBox 消息框系统

#### 类型安全设计

[`ezMsgBox`](src/EasyTk/ezMsgBox.py#L44) 使用 Literal 类型确保参数类型安全：

```python
ICONS = Literal["error", "info", "question", "warning"]
TYPES = Literal["abortretryignore", "ok", "okcancel", "retrycancel", "yesno", "yesnocancel"]
REPLIES = Literal["abort", "retry", "ignore", "ok", "cancel", "yes", "no"]
```

#### 预设模式

提供四种预设模式：

- **info**：信息提示（info图标 + OK按钮）
- **warn**：警告提示（warning图标 + OK按钮）  
- **error**：错误提示（error图标 + OK按钮）
- **query**：询问提示（question图标 + YESNO按钮）

#### 临时根窗口管理

使用 [`get_temp_root()`](src/EasyTk/ezMsgBox.py#L8) 和 [`destroy_temp_root()`](src/EasyTk/ezMsgBox.py#L32) 自动管理临时Tk实例，避免根窗口冲突。

### 核心设计模式

#### 1. 模板方法模式
`ezFrame` 通过抽象的 `UIInit()` 方法定义了框架创建的标准流程。

#### 2. 策略模式  
`ezFrameManager` 的两种切换模式体现了策略模式，允许运行时选择不同的渲染策略。

#### 3. 工厂方法模式
`ezMsgBox` 的预设模式提供了便捷的消息框创建方式。

#### 4. 组合模式
`ezFrameList` 将多个框架统一管理，提供了类似集合的接口。

### 使用建议

1. **简单应用**：直接使用 `ezTk` + 传统tkinter组件
2. **多页面应用**：结合 `ezFrameManager` 和 `ezFrame` 实现页面切换
3. **模态对话框**：使用 `ezMsgBox` 处理用户交互反馈
4. **复杂布局**：继承 `ezFrame` 创建可复用的UI组件

通过这些核心组件，EasyTk 提供了一套完整的桌面应用开发解决方案，既保持了 tkinter 的灵活性，又提供了更高级的抽象和更便捷的API。

### 示例特性
- ✅ 现代化深色主题界面
- ✅ 多框架切换导航
- ✅ 响应式布局设计
- ✅ 配置面板演示
- ✅ 实时状态显示

---

## 📁 项目结构

```
EasyTk/
├── src/EasyTk/          # 源代码目录
│   ├── __init__.py     # 模块入口
│   ├── ezTk.py        # 核心窗口类
│   ├── ezFrame.py     # 框架系统
│   └── ezMsgBox.py    # 消息系统
├── example/           # 示例应用
│   ├── main.py       # 主示例
│   └── assets/       # 资源文件
├── tests/            # 测试代码
├── pyproject.toml    # 项目配置
└── README.md         # 项目说明
```

## 🎯 为什么选择 EasyTk？

| 特性 | EasyTk | 原生 tkinter |
|------|--------|-------------|
| **窗口管理** | ✅ 一行代码创建窗口 | ❌ 需要多步配置 |
| **框架系统** | ✅ 内置模块化管理 | ❌ 手动管理框架 |
| **消息对话框** | ✅ 统一简洁的 API | ❌ 多种不同接口 |
| **几何管理** | ✅ 链式调用，语义清晰 | ❌ 字符串格式复杂 |
| **学习曲线** | ✅ 平缓易上手 | ❌ 陡峭复杂 |
| **代码量** | ✅ 减少 40-60% | ❌ 冗长重复 |

## 🤝 贡献指南

我们欢迎各种形式的贡献！无论是发现 Bug、提出新功能建议，还是提交 Pull Request，都是对我们的帮助。

### 如何贡献：
1. **Fork** 本项目
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 开发环境设置：
```bash
# 克隆项目
git clone https://github.com/NuhilLucas/EasyTk.git

# 安装开发依赖
cd EasyTk
poetry install

# 运行测试
pytest tests/
```

## 📄 许可证

本项目基于 **MIT 许可证** 开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

- 📧 **问题反馈**: [GitHub Issues](https://github.com/NuhilLucas/EasyTk/issues)
- 💬 **讨论交流**: [GitHub Discussions](https://github.com/NuhilLucas/EasyTk/discussions)
- 📚 **文档更新**: [项目 Wiki](https://github.com/NuhilLucas/EasyTk/wiki)

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=NuhilLucas/EasyTk&type=Date)](https://star-history.com/#NuhilLucas/EasyTk&Date)

---

