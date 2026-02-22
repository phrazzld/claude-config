use sentry::ClientInitGuard;

/// Initialize Sentry. Returns a guard that must be held for the program lifetime.
///
/// ```rust
/// fn main() {
///     let _sentry = sentry_init::init();
///     // ... your program ...
/// }
/// ```
pub fn init() -> Option<ClientInitGuard> {
    let dsn = std::env::var("SENTRY_DSN").ok()?;
    if dsn.is_empty() {
        return None;
    }

    let env = std::env::var("SENTRY_ENVIRONMENT").unwrap_or_else(|_| "development".into());
    let release = std::env::var("SENTRY_RELEASE").ok();

    let guard = sentry::init((
        dsn,
        sentry::ClientOptions {
            environment: Some(env.into()),
            release: release.map(Into::into),
            traces_sample_rate: 0.1,
            send_default_pii: false,
            ..Default::default()
        },
    ));

    Some(guard)
}
