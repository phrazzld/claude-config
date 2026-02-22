import Foundation
import Sentry

enum SentrySetup {
    /// Initialize Sentry SDK. Call in AppDelegate or @main App init.
    /// Requires SENTRY_DSN in environment or Info.plist.
    static func start() {
        guard let dsn = ProcessInfo.processInfo.environment["SENTRY_DSN"]
            ?? Bundle.main.infoDictionary?["SENTRY_DSN"] as? String,
            !dsn.isEmpty
        else {
            return
        }

        SentrySDK.start { options in
            options.dsn = dsn
            options.tracesSampleRate = 0.1
            options.enableAutoSessionTracking = true
            options.sendDefaultPii = false

            #if DEBUG
            options.environment = "development"
            options.debug = true
            #else
            options.environment = "production"
            #endif
        }
    }
}
