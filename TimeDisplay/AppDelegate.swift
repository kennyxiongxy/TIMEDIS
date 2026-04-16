import AppKit

class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusBarController: StatusBarController?
    private var timeWindowController: TimeWindowController?
    private var settingsWindowController: SettingsWindowController?

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusBar()
        setupTimeWindow()
        applySettings()
    }

    private func setupStatusBar() {
        statusBarController = StatusBarController()
        statusBarController?.onShowTimeWindow = { [weak self] in
            self?.timeWindowController?.showWindow(nil)
        }
        statusBarController?.onShowSettings = { [weak self] in
            self?.showSettings()
        }
        statusBarController?.onQuit = {
            NSApplication.shared.terminate(nil)
        }
    }

    private func setupTimeWindow() {
        timeWindowController = TimeWindowController()
        timeWindowController?.onShowSettings = { [weak self] in
            self?.showSettings()
        }
        timeWindowController?.onQuit = {
            NSApplication.shared.terminate(nil)
        }
        timeWindowController?.showWindow(nil)
    }

    private func applySettings() {
        timeWindowController?.applySettings()
    }

    func showSettings() {
        if settingsWindowController == nil {
            settingsWindowController = SettingsWindowController()
        }
        settingsWindowController?.onSettingsChanged = { [weak self] in
            self?.timeWindowController?.applySettings()
        }
        settingsWindowController?.onPreviewSettings = { [weak self] (textColor, bgColor, opacity, fontName, fontSize) in
            self?.timeWindowController?.updatePreview(
                textColor: textColor,
                backgroundColor: bgColor,
                backgroundOpacity: opacity,
                fontName: fontName,
                fontSize: fontSize
            )
        }
        settingsWindowController?.showWindow(nil)
        settingsWindowController?.window?.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }

    func applicationWillTerminate(_ notification: Notification) {
        Settings.shared.save()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return false
    }
}
