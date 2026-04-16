import AppKit

class TimeWindowController: NSWindowController, NSWindowDelegate {
    private var timeView: TimeView!
    var onShowSettings: (() -> Void)?
    var onQuit: (() -> Void)?

    convenience init() {
        let window = TimeWindowController.createWindow()
        self.init(window: window)
        setupTimeView()
        setupContextMenu()
    }

    private static func createWindow() -> NSWindow {
        let screenFrame = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 1920, height: 1080)
        let contentRect = NSRect(x: screenFrame.origin.x + screenFrame.width - 300 - 50, y: screenFrame.origin.y + screenFrame.height - 80 - 50, width: 300, height: 80)

        let window = NSPanel(
            contentRect: contentRect,
            styleMask: [.borderless, .nonactivatingPanel],
            backing: .buffered,
            defer: false
        )

        window.level = .floating
        window.isOpaque = false
        window.backgroundColor = .clear
        window.hasShadow = true
        window.isMovableByWindowBackground = true
        window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .stationary]
        window.isReleasedWhenClosed = false
        window.hidesOnDeactivate = false
        window.isRestorable = false

        return window
    }

    private func setupTimeView() {
        let initialFrame = NSRect(x: 0, y: 0, width: 300, height: 80)
        timeView = TimeView(frame: initialFrame)
        window?.contentView = timeView
    }

    private func setupContextMenu() {
        let menu = NSMenu()

        let settingsItem = NSMenuItem(title: "设置...", action: #selector(showSettings), keyEquivalent: ",")
        settingsItem.target = self
        menu.addItem(settingsItem)

        menu.addItem(NSMenuItem.separator())

        let quitItem = NSMenuItem(title: "退出", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        timeView.menu = menu
    }

    @objc private func showSettings() {
        onShowSettings?()
    }

    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }

    func applySettings() {
        let settings = Settings.shared
        timeView.applySettings(
            textColor: settings.textColor,
            backgroundColor: settings.backgroundColor,
            backgroundOpacity: settings.backgroundOpacity,
            fontName: settings.fontName,
            fontSize: settings.fontSize
        )

        let newSize = timeView.frame.size
        window?.setContentSize(newSize)
    }

    func updatePreview(textColor: NSColor, backgroundColor: NSColor, backgroundOpacity: CGFloat, fontName: String, fontSize: CGFloat) {
        timeView.applySettings(
            textColor: textColor,
            backgroundColor: backgroundColor,
            backgroundOpacity: backgroundOpacity,
            fontName: fontName,
            fontSize: fontSize
        )

        let newSize = timeView.frame.size
        window?.setContentSize(newSize)
    }
}
