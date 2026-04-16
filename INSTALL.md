# TimeDisplay 安装指南

## 📦 下载应用

下载 `TimeDisplay-v1.0.0.zip` 文件（约 35KB）

## 🔧 安装步骤

### 方法一：解压直接使用（推荐）

1. **解压 ZIP 文件**
   ```bash
   # 在 Finder 中双击 TimeDisplay-v1.0.0.zip
   # 或使用命令行：
   unzip TimeDisplay-v1.0.0.zip
   ```

2. **运行应用**
   - 双击 `TimeDisplay.app`
   - 首次运行可能会提示"无法打开，因为来着不明开发者"
   - 如果出现此提示，请见下方"解决无法打开的问题"

### 方法二：安装到应用程序文件夹

1. **解压 ZIP 文件**
   ```bash
   unzip TimeDisplay-v1.0.0.zip
   ```

2. **移动到应用程序**
   ```bash
   # 方法 A：命令行
   mv TimeDisplay.app /Applications/

   # 方法 B：手动
   # 将 TimeDisplay.app 拖拽到 Finder 的"应用程序"文件夹
   ```

3. **从启动台运行**
   - 打开 Finder → 应用程序
   - 找到 TimeDisplay 并点击运行

## ⚠️ 常见问题

### 无法打开应用（来着不明开发者）

macOS 默认只允许运行来自 App Store 和认证开发者的应用。

**解决方法：**

1. **方法一：系统偏好设置**
   - 打开"系统偏好设置" → "安全性与隐私" → "通用"
   - 点击左下角的锁图标，输入密码解锁
   - 在"允许从以下位置下载的应用"下方选择"任何来源"
   - 如果没有"任何来源"选项，运行以下命令：
     ```bash
     sudo spctl --master-enable
     ```

2. **方法二：右键打开（推荐）**
   - 在 Finder 中找到 `TimeDisplay.app`
   - **不要双击**，而是**右键点击**（或 Control+点击）
   - 选择"打开"
   - 在弹出窗口中点击"打开"按钮

3. **方法三：终端命令**
   ```bash
   xattr -rd com.apple.quarantine /Applications/TimeDisplay.app
   ```

### 应用没有在 Dock 中显示

这是**正常现象**！

TimeDisplay 设计为菜单栏应用（LSUIElement = true）：
- 应用运行时**不会在 Dock 中显示图标**
- 只会在**菜单栏（屏幕顶部）**显示一个时钟图标
- 如需退出应用，点击菜单栏图标 → "退出"

### 菜单栏没有显示图标

1. 确认应用正在运行（检查菜单栏右侧）
2. 如果菜单栏空间不足，可能需要调整：
   - 拖动其他菜单栏项让出空间
   - 或调整系统设置

## 🚀 使用方法

1. **查看时间**
   - 点击菜单栏的时钟图标
   - 选择"显示时间"
   - 屏幕上会显示当前时间（HH:mm:ss）

2. **自定义外观**
   - 点击菜单栏的时钟图标
   - 选择"设置..."
   - 调整颜色、字体、透明度等

3. **退出应用**
   - 点击菜单栏的时钟图标
   - 选择"退出"

## 🔄 更新应用

1. 关闭当前运行的应用
2. 用新的 `TimeDisplay.app` 替换旧版本
   ```bash
   # 替换命令
   rm -rf /Applications/TimeDisplay.app
   cp -R ./TimeDisplay.app /Applications/
   ```

## 🗑️ 卸载应用

1. **关闭应用**
2. **删除应用**
   ```bash
   rm -rf /Applications/TimeDisplay.app
   ```
   或将 Finder 中"应用程序"文件夹的 TimeDisplay 拖到废纸篓

3. **清除配置（可选）**
   ```bash
   rm -rf ~/Library/Preferences/com.timedisplay.TimeDisplay.plist
   rm -rf ~/Library/Application\ Support/TimeDisplay
   ```

## 📋 系统要求

- macOS 12.0 Monterey 或更高版本
- Apple Silicon 或 Intel 处理器
- 约 10MB 磁盘空间

## 🐛 问题反馈

如遇问题，请访问：
- GitHub Issues: https://github.com/kennyxiongxy/TIMEDIS/issues

## 📄 许可证

本应用采用 MIT 许可证开源。
