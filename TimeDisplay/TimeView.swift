import AppKit

class TimeView: NSView {
    private var backgroundLayer: CALayer!
    private var timeLabel: NSTextField!
    private var timer: Timer?

    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupView()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupView()
    }

    private func setupView() {
        wantsLayer = true

        backgroundLayer = CALayer()
        backgroundLayer.cornerRadius = 10
        backgroundLayer.masksToBounds = true
        layer?.addSublayer(backgroundLayer)

        timeLabel = NSTextField(labelWithString: "")
        timeLabel.isEditable = false
        timeLabel.isSelectable = false
        timeLabel.isBezeled = false
        timeLabel.drawsBackground = false
        timeLabel.alignment = .center
        timeLabel.font = NSFont(name: "Helvetica Neue", size: 48)
        timeLabel.textColor = .white
        addSubview(timeLabel)

        startTimer()
        updateTime()
        updateLayoutImmediate()
    }

    func applySettings(textColor: NSColor, backgroundColor: NSColor, backgroundOpacity: CGFloat, fontName: String, fontSize: CGFloat) {
        timeLabel.textColor = textColor
        timeLabel.font = NSFont(name: fontName, size: fontSize) ?? NSFont.systemFont(ofSize: fontSize)

        let bgColor = backgroundColor.withAlphaComponent(backgroundOpacity)
        backgroundLayer.backgroundColor = bgColor.cgColor

        updateLayoutImmediate()
    }

    private func updateLayoutImmediate() {
        timeLabel.sizeToFit()

        let timeSize = timeLabel.frame.size
        let padding: CGFloat = 12

        let width = timeSize.width + padding * 2
        let height = timeSize.height + padding * 2

        frame = NSRect(
            x: frame.origin.x,
            y: frame.origin.y,
            width: width,
            height: height
        )
        backgroundLayer.frame = bounds

        let centerX = width / 2
        let centerY = height / 2

        timeLabel.frame = NSRect(
            x: centerX - timeSize.width / 2,
            y: centerY - timeSize.height / 2,
            width: timeSize.width,
            height: timeSize.height
        )
    }

    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.updateTime()
        }
        RunLoop.current.add(timer!, forMode: .common)
    }

    private func updateTime() {
        let now = Date()
        let timeFormatter = DateFormatter()
        timeFormatter.dateFormat = "HH:mm:ss"
        timeLabel.stringValue = timeFormatter.string(from: now)
    }

    deinit {
        timer?.invalidate()
    }
}
