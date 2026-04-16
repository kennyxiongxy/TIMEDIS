import AppKit

class SettingsWindowController: NSWindowController {
    var onSettingsChanged: (() -> Void)?
    var onPreviewSettings: ((NSColor, NSColor, CGFloat, String, CGFloat) -> Void)?

    private var textColorWell: NSColorWell!
    private var backgroundColorWell: NSColorWell!
    private var opacitySlider: NSSlider!
    private var opacityLabel: NSTextField!
    private var fontSizeSlider: NSSlider!
    private var fontSizeLabel: NSTextField!
    private var fontPopUp: NSPopUpButton!

    convenience init() {
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 400, height: 300),
            styleMask: [.titled, .closable],
            backing: .buffered,
            defer: false
        )
        window.title = "时间显示设置"
        window.center()

        self.init(window: window)
        setupUI()
        loadSettings()
    }

    private func setupUI() {
        guard let contentView = window?.contentView else { return }

        let labels = ["文字颜色:", "背景颜色:", "背景透明度:", "字体:", "字体大小:"]

        for (index, labelText) in labels.enumerated() {
            let label = NSTextField(labelWithString: labelText)
            label.frame = NSRect(x: 20, y: 240 - CGFloat(index * 45), width: 100, height: 20)
            label.alignment = .right
            contentView.addSubview(label)
        }

        textColorWell = NSColorWell(frame: NSRect(x: 130, y: 240 - 0 * 45, width: 50, height: 25))
        textColorWell.target = self
        textColorWell.action = #selector(settingsChanged)
        contentView.addSubview(textColorWell)

        backgroundColorWell = NSColorWell(frame: NSRect(x: 130, y: 240 - 1 * 45, width: 50, height: 25))
        backgroundColorWell.target = self
        backgroundColorWell.action = #selector(settingsChanged)
        contentView.addSubview(backgroundColorWell)

        opacitySlider = NSSlider(frame: NSRect(x: 130, y: 240 - 2 * 45, width: 200, height: 25))
        opacitySlider.minValue = 0.1
        opacitySlider.maxValue = 1.0
        opacitySlider.isContinuous = true
        opacitySlider.target = self
        opacitySlider.action = #selector(opacityChanged)
        contentView.addSubview(opacitySlider)

        opacityLabel = NSTextField(labelWithString: "70%")
        opacityLabel.frame = NSRect(x: 340, y: 240 - 2 * 45, width: 40, height: 20)
        contentView.addSubview(opacityLabel)

        let fonts = ["Helvetica Neue", "Arial", "Menlo", "SF Mono", "Monaco", "Courier New", "System Font"]
        fontPopUp = NSPopUpButton(frame: NSRect(x: 130, y: 240 - 3 * 45, width: 200, height: 25))
        fontPopUp.addItems(withTitles: fonts)
        fontPopUp.target = self
        fontPopUp.action = #selector(settingsChanged)
        contentView.addSubview(fontPopUp)

        fontSizeSlider = NSSlider(frame: NSRect(x: 130, y: 240 - 4 * 45, width: 200, height: 25))
        fontSizeSlider.minValue = 20
        fontSizeSlider.maxValue = 100
        fontSizeSlider.isContinuous = true
        fontSizeSlider.target = self
        fontSizeSlider.action = #selector(fontSizeChanged)
        contentView.addSubview(fontSizeSlider)

        fontSizeLabel = NSTextField(labelWithString: "48")
        fontSizeLabel.frame = NSRect(x: 340, y: 240 - 4 * 45, width: 40, height: 20)
        contentView.addSubview(fontSizeLabel)

        let resetButton = NSButton(frame: NSRect(x: 130, y: 20, width: 80, height: 30))
        resetButton.title = "重置"
        resetButton.bezelStyle = .rounded
        resetButton.target = self
        resetButton.action = #selector(resetSettings)
        contentView.addSubview(resetButton)

        let saveButton = NSButton(frame: NSRect(x: 220, y: 20, width: 80, height: 30))
        saveButton.title = "保存"
        saveButton.bezelStyle = .rounded
        saveButton.target = self
        saveButton.action = #selector(saveSettings)
        contentView.addSubview(saveButton)
    }

    private func loadSettings() {
        let settings = Settings.shared
        textColorWell.color = settings.textColor
        backgroundColorWell.color = settings.backgroundColor
        opacitySlider.doubleValue = Double(settings.backgroundOpacity)
        opacityLabel.stringValue = "\(Int(settings.backgroundOpacity * 100))%"
        fontPopUp.selectItem(withTitle: settings.fontName)
        fontSizeSlider.doubleValue = Double(settings.fontSize)
        fontSizeLabel.stringValue = "\(Int(settings.fontSize))"
    }

    @objc private func settingsChanged() {
        let settings = Settings.shared
        settings.textColor = textColorWell.color
        settings.backgroundColor = backgroundColorWell.color
        settings.fontName = fontPopUp.titleOfSelectedItem ?? "Helvetica Neue"
        settings.fontSize = CGFloat(fontSizeSlider.doubleValue)

        previewSettings()
    }

    @objc private func opacityChanged() {
        opacityLabel.stringValue = "\(Int(opacitySlider.doubleValue * 100))%"
        Settings.shared.backgroundOpacity = CGFloat(opacitySlider.doubleValue)

        previewSettings()
    }

    @objc private func fontSizeChanged() {
        fontSizeLabel.stringValue = "\(Int(fontSizeSlider.doubleValue))"
        Settings.shared.fontSize = CGFloat(fontSizeSlider.doubleValue)

        previewSettings()
    }

    private func previewSettings() {
        let textColor = textColorWell.color
        let bgColor = backgroundColorWell.color
        let opacity = CGFloat(opacitySlider.doubleValue)
        let fontName = fontPopUp.titleOfSelectedItem ?? "Helvetica Neue"
        let fontSize = CGFloat(fontSizeSlider.doubleValue)

        onPreviewSettings?(textColor, bgColor, opacity, fontName, fontSize)
    }

    @objc private func saveSettings() {
        Settings.shared.save()
        onSettingsChanged?()
        window?.close()
    }

    @objc private func resetSettings() {
        Settings.shared.reset()
        loadSettings()
        previewSettings()
    }
}
