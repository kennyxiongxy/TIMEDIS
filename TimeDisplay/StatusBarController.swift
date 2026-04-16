import AppKit

class StatusBarController {
    private var statusItem: NSStatusItem
    private var menu: NSMenu

    var onShowTimeWindow: (() -> Void)?
    var onShowSettings: (() -> Void)?
    var onQuit: (() -> Void)?

    init() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        menu = NSMenu()

        setupStatusButton()
        setupMenu()
    }

    private func setupStatusButton() {
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "clock.fill", accessibilityDescription: "Time Display")
            button.imagePosition = .imageOnly
        }
    }

    private func setupMenu() {
        let showTimeItem = NSMenuItem(title: "显示时间", action: #selector(showTimeWindow), keyEquivalent: "t")
        showTimeItem.target = self
        menu.addItem(showTimeItem)

        menu.addItem(NSMenuItem.separator())

        let settingsItem = NSMenuItem(title: "设置...", action: #selector(showSettings), keyEquivalent: ",")
        settingsItem.target = self
        menu.addItem(settingsItem)

        menu.addItem(NSMenuItem.separator())

        let quitItem = NSMenuItem(title: "退出", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        statusItem.menu = menu
    }

    @objc private func showTimeWindow() {
        onShowTimeWindow?()
    }

    @objc private func showSettings() {
        onShowSettings?()
    }

    @objc private func quit() {
        onQuit?()
    }
}
