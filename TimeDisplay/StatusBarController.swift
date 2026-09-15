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
            button.image = Self.brandStatusImage()
            button.imagePosition = .imageOnly
        }
    }

    /// 菜单栏图标：使用与 App Icon 同源的品牌图形（模板图，随菜单栏明暗自动反色）。
    /// 资产缺失时回落到系统时钟符号，保证不会出现空白按钮。
    private static func brandStatusImage() -> NSImage? {
        guard let brand = NSImage(named: "MenuBarIcon") else {
            return NSImage(systemSymbolName: "clock.fill", accessibilityDescription: "Time Display")
        }
        brand.isTemplate = true
        brand.size = NSSize(width: 18, height: 18)
        brand.accessibilityDescription = "Time Display"
        return brand
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
