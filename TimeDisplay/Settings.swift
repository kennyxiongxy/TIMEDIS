import AppKit

class Settings {
    static let shared = Settings()

    private let defaults = UserDefaults.standard

    private enum Keys {
        static let textColor = "textColor"
        static let backgroundColor = "backgroundColor"
        static let backgroundOpacity = "backgroundOpacity"
        static let fontName = "fontName"
        static let fontSize = "fontSize"
        static let windowX = "windowX"
        static let windowY = "windowY"
    }

    var textColor: NSColor {
        get {
            if let data = defaults.data(forKey: Keys.textColor),
               let color = try? NSKeyedUnarchiver.unarchivedObject(ofClass: NSColor.self, from: data) {
                return color
            }
            return NSColor.white
        }
        set {
            if let data = try? NSKeyedArchiver.archivedData(withRootObject: newValue, requiringSecureCoding: true) {
                defaults.set(data, forKey: Keys.textColor)
            }
        }
    }

    var backgroundColor: NSColor {
        get {
            if let data = defaults.data(forKey: Keys.backgroundColor),
               let color = try? NSKeyedUnarchiver.unarchivedObject(ofClass: NSColor.self, from: data) {
                return color
            }
            return NSColor.black
        }
        set {
            if let data = try? NSKeyedArchiver.archivedData(withRootObject: newValue, requiringSecureCoding: true) {
                defaults.set(data, forKey: Keys.backgroundColor)
            }
        }
    }

    var backgroundOpacity: CGFloat {
        get {
            let value = defaults.double(forKey: Keys.backgroundOpacity)
            return value > 0 ? CGFloat(value) : 0.7
        }
        set {
            defaults.set(Double(newValue), forKey: Keys.backgroundOpacity)
        }
    }

    var fontName: String {
        get {
            return defaults.string(forKey: Keys.fontName) ?? "Helvetica Neue"
        }
        set {
            defaults.set(newValue, forKey: Keys.fontName)
        }
    }

    var fontSize: CGFloat {
        get {
            let value = defaults.double(forKey: Keys.fontSize)
            return value > 0 ? CGFloat(value) : 48
        }
        set {
            defaults.set(Double(newValue), forKey: Keys.fontSize)
        }
    }

    var windowX: CGFloat {
        get {
            return CGFloat(defaults.double(forKey: Keys.windowX))
        }
        set {
            defaults.set(Double(newValue), forKey: Keys.windowX)
        }
    }

    var windowY: CGFloat {
        get {
            return CGFloat(defaults.double(forKey: Keys.windowY))
        }
        set {
            defaults.set(Double(newValue), forKey: Keys.windowY)
        }
    }

    func save() {
        defaults.synchronize()
    }

    func reset() {
        textColor = NSColor.white
        backgroundColor = NSColor.black
        backgroundOpacity = 0.7
        fontName = "Helvetica Neue"
        fontSize = 48
    }

    private init() {}
}
