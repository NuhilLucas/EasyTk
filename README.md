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
app.Geometry.Center()  # 窗口居中显示

# 创建框架管理器
frame_manager = ezFrameManager(app)

# 添加框架并设置主页
frame_manager.AddFrame([
    HomePage(master=frame_manager, name="home")
], "home")

# 运行应用
app.Run()
```

### 智能消息对话框

```python
from EasyTk import MsgBox

# 信息提示
MsgBox(mode="info", 
       title="🎉 操作成功", 
       message="文件已成功保存！")

# 确认对话框
if MsgBox(mode="query", 
          title="⚠️ 确认操作",
          message="确定要删除这个项目吗？") == "yes":
    print("用户确认删除")
    
# 警告消息
MsgBox(mode="warn",
       title="⚠️ 警告",
       message="磁盘空间不足！")
```

## 📚 核心组件详解

### 🪟 ezTk - 智能窗口管理

```python
app = ezTk("我的应用", theme="dark")  # 支持深色主题

# 几何管理
app.Geometry.Size(1280, 720)      # 设置窗口大小
app.Geometry.Pos(100, 100)        # 设置窗口位置
app.Geometry.Center()              # 窗口居中
app.Geometry.SizeLimit("min", 400, 300)  # 设置最小尺寸
app.Geometry.SizeFix(False, True)  # 允许水平调整，禁止垂直调整

# 窗口行为
app.SetIcon("icon.ico")  # 设置窗口图标
app.OnClose(callback)    # 设置关闭回调
```

### 🧩 ezFrame - 模块化框架系统

```python
class SettingsPage(ezFrame):
    """设置页面框架"""
    
    def __init__(self, master, name, config):
        super().__init__(master, name)
        self.config = config  # 自定义参数
    
    def UIInit(self):
        self.Frame = Frame(master=self.master, bg="white")
        
        # 构建你的 UI 组件
        Label(self.Frame, text="设置面板", font=("Arial", 16)).pack()
        # ... 更多组件
    
    def DoPlace(self):
        self.Frame.pack(fill="both", expand=True)
    
    def OtherHook(self):
        # 额外的初始化逻辑
        print(f"框架 {self.name} 已初始化")
```

### 🔄 ezFrameManager - 框架管理器

```python
# 创建管理器
manager = ezFrameManager(app)

# 配置管理器
manager.SwitchMode("redraw")  # 切换模式：redraw 或 tkraise
manager.frames_persisted = ["sidebar", "header"]  # 持久化框架

# 添加多个框架
frames = [
    HomePage(master=manager, name="home"),
    SettingsPage(master=manager, name="settings"),
    AboutPage(master=manager, name="about")
]

manager.AddFrame(frames, initial_frame="home")

# 切换框架
manager.Switch("settings")  # 切换到设置页面
```

### 📢 MsgBox - 优雅的消息系统

```python
from EasyTk import MsgBox

# 多种消息类型
MsgBox.info("操作成功", "文件已保存")
MsgBox.warn("警告", "磁盘空间不足")
MsgBox.error("错误", "无法连接到服务器")

# 自定义对话框
result = MsgBox(
    mode="query",
    title="确认删除",
    message="确定要永久删除此文件吗？",
    buttons={"yes": "确定删除", "no": "取消"},
    default_button="no"
)

if result == "yes":
    # 执行删除操作
    pass
```

## 🎨 示例应用展示

我们提供了一个完整的示例应用，展示了 EasyTk 的所有特性：

```bash
# 克隆仓库
git clone https://github.com/NuhilLucas/EasyTk.git

# 运行示例
cd EasyTk/example
python main.py
```

### 示例特性
- ✅ 现代化深色主题界面
- ✅ 多框架切换导航
- ✅ 响应式布局设计
- ✅ 配置面板演示
- ✅ 实时状态显示

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
