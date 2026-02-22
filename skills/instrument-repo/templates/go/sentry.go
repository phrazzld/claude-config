package observability

import (
	"fmt"
	"os"
	"time"

	"github.com/getsentry/sentry-go"
)

// InitSentry initializes the Sentry SDK. Call FlushSentry before program exit.
func InitSentry() error {
	dsn := os.Getenv("SENTRY_DSN")
	if dsn == "" {
		return nil // Sentry disabled when DSN not set
	}

	env := os.Getenv("SENTRY_ENVIRONMENT")
	if env == "" {
		env = "development"
	}

	return sentry.Init(sentry.ClientOptions{
		Dsn:              dsn,
		Environment:      env,
		Release:          os.Getenv("SENTRY_RELEASE"),
		TracesSampleRate: 0.1,
		BeforeSend: func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
			// Strip PII
			if event.User.Email != "" {
				event.User.Email = "[REDACTED]"
			}
			event.User.IPAddress = ""
			return event
		},
	})
}

// FlushSentry flushes buffered events. Call with defer in main().
func FlushSentry() {
	sentry.Flush(2 * time.Second)
}

// CaptureError reports an error to Sentry with optional context.
func CaptureError(err error, tags map[string]string) {
	if err == nil {
		return
	}
	sentry.WithScope(func(scope *sentry.Scope) {
		for k, v := range tags {
			scope.SetTag(k, v)
		}
		sentry.CaptureException(err)
	})
}

// RecoverAndReport captures panics and reports them to Sentry.
// Use: defer observability.RecoverAndReport()
func RecoverAndReport() {
	if r := recover(); r != nil {
		var err error
		switch v := r.(type) {
		case error:
			err = v
		default:
			err = fmt.Errorf("panic: %v", v)
		}
		sentry.CaptureException(err)
		sentry.Flush(2 * time.Second)
		panic(r) // Re-panic after reporting
	}
}
