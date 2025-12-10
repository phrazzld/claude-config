// next.config.ts with Sentry integration
// This shows how to wrap your Next.js config with Sentry

import { withSentryConfig } from '@sentry/nextjs';
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Your existing Next.js configuration
  reactStrictMode: true,

  // Example: Enable experimental features
  // experimental: {
  //   serverActions: true,
  // },
};

// Sentry configuration options for the Next.js plugin
const sentryNextConfigOptions = {
  // Suppress build logs in CI
  silent: !process.env.CI,

  // SECURITY: Hide source maps from client bundles
  // Source maps are uploaded to Sentry separately
  hideSourceMaps: true,

  // Reduce bundle size by removing Sentry logger in production
  disableLogger: true,

  // Automatically wrap API routes and page components
  autoInstrumentAppRouter: true,
  autoInstrumentServerFunctions: true,
};

// Sentry Webpack plugin options
const sentryWebpackPluginOptions = {
  // Upload source maps to Sentry during build
  authToken: process.env.SENTRY_AUTH_TOKEN,
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,

  // Enable monitoring of Vercel Cron jobs
  automaticVercelMonitors: true,

  // Release options (automatic with Vercel Integration)
  // release: process.env.VERCEL_GIT_COMMIT_SHA,
};

// Export with Sentry wrapper
export default withSentryConfig(
  nextConfig,
  sentryNextConfigOptions,
  sentryWebpackPluginOptions
);
