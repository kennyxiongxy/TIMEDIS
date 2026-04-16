# TimeDisplay

<p align="center">
  <img src="https://img.shields.io/badge/macOS-12.0%2B-blue?style=for-the-badge" alt="macOS">
  <img src="https://img.shields.io/badge/Swift-5.9-orange?style=for-the-badge" alt="Swift">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 🌟 一款简洁优雅的 macOS 菜单栏时间显示应用

## ✨ 特性

- 📋 **菜单栏显示**: 无 Dock 图标，直接在菜单栏显示当前时间
- ⏱️ **实时更新**: 每秒自动更新，显示精确到秒的时间 (HH:mm:ss)
- 🎨 **完全可定制**:
  - 自定义文本颜色
  - 自定义背景颜色和透明度
  - 多种字体选择
  - 可调节字体大小
- 💾 **智能记忆**: 自动保存所有设置，重启后保持配置
- 🪟 **窗口管理**: 记住窗口位置，下次打开自动定位
- 🌍 **中文界面**: 简洁的中文菜单，易于使用

## 📥 安装

### 方法一：从源码编译

#### 前置要求

- macOS 12.0 或更高版本
- Xcode 15.0 或更高版本
- XcodeGen

#### 编译步骤

1. 克隆仓库

```bash
git clone https://github.com/kennyxiongxy/TIMEDIS.git
cd TIMEDIS
```

2. 生成 Xcode 项目

```bash
xcodegen generate
```

3. 打开项目并编译

```bash
open TimeDisplay.xcodeproj
```

4. 在 Xcode 中，选择 **Product → Build** (或按 ⌘B)

5. 编译完成后，在 `DerivedData` 目录找到 `TimeDisplay.app`

### 方法二：使用 CocoaPods (待实现)

```bash
# 即将支持
```

## 🚀 使用

1. 启动应用后，菜单栏会显示时钟图标
2. 点击时钟图标，选择"显示时间"打开时间窗口
3. 点击"设置..."自定义外观和行为
4. 所有设置自动保存

## ⚙️ 配置

### 默认设置

| 选项 | 默认值 |
|------|--------|
| 文本颜色 | 白色 (#FFFFFF) |
| 背景颜色 | 黑色 (#000000) |
| 背景透明度 | 70% |
| 字体 | Helvetica Neue |
| 字体大小 | 48pt |

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| ⌘T | 显示时间窗口 |
| ⌘, | 打开设置 |
| ⌘Q | 退出应用 |

## 📁 项目结构

```
TIMEDIS/
├── TimeDisplay/
│   ├── main.swift              # 应用入口点
│   ├── AppDelegate.swift        # 应用代理
│   ├── TimeView.swift          # 时间显示视图
│   ├── TimeWindowController.swift # 时间窗口控制器
│   ├── StatusBarController.swift # 菜单栏控制器
│   ├── Settings.swift          # 设置管理
│   ├── SettingsWindowController.swift # 设置窗口控制器
│   ├── Info.plist             # 应用配置
│   └── Assets.xcassets/       # 应用资源
├── project.yml                 # XcodeGen 配置
├── .gitignore                  # Git 忽略规则
└── README.md                   # 项目文档
```

## 🛠 技术栈

- **语言**: Swift 5.9
- **框架**: AppKit
- **构建工具**: XcodeGen
- **最低系统**: macOS 12.0 Monterey

## 🔧 开发

### 环境要求

- Xcode 15.0+
- Swift 5.9+
- macOS Developer Tools

### 编译

```bash
# 生成项目
xcodegen generate

# 编译
xcodebuild -project TimeDisplay.xcodeproj -scheme TimeDisplay -configuration Release build

# 或在 Xcode 中编译
open TimeDisplay.xcodeproj
```

### 代码规范

- 遵循 Swift 官方代码规范
- 使用 ARC 进行内存管理
- 所有视图使用 Auto Layout

## 📝 更新日志

### v1.0.0 (2026-04-16)

- ✨ 初始版本发布
- ⏱️ 实现菜单栏时间显示
- 🎨 支持自定义颜色和字体
- 💾 实现设置持久化
- 🪟 支持窗口位置记忆

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

**熊尛雄 (kennyxiongxy)**

- GitHub: [@kennyxiongxy](https://github.com/kennyxiongxy)

## 🙏 致谢

- [XcodeGen](https://github.com/yonaskolb/XcodeGen) - Xcode 项目生成器
- [Apple Developer Documentation](https://developer.apple.com/documentation/) - macOS 开发文档

---

<p align="center">
  ⭐️ 如果这个项目对你有帮助，请给我一个星标！
</p>
