// app/test-error/route.ts
// Test route for verifying Sentry integration
// Access: GET /test-error or /test-error?type=async

import { NextRequest } from 'next/server';
import * as Sentry from '@sentry/nextjs';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const type = searchParams.get('type') || 'generic';

  // Add context for debugging in Sentry
  Sentry.setContext('test_error', {
    type,
    timestamp: new Date().toISOString(),
    environment: process.env.VERCEL_ENV || process.env.NODE_ENV || 'development',
    triggered_by: 'test-error-route',
  });

  // Add a breadcrumb
  Sentry.addBreadcrumb({
    category: 'test',
    message: `Test error triggered: ${type}`,
    level: 'info',
  });

  switch (type) {
    case 'generic':
      // Standard thrown error - tests basic error capture
      throw new Error('Test error - Sentry integration check');

    case 'async':
      // Async error - tests promise rejection handling
      await Promise.reject(new Error('Test async error - Promise rejection'));
      break;

    case 'handled':
      // Manually captured error - tests captureException
      try {
        throw new Error('Test handled error - Manual capture');
      } catch (error) {
        Sentry.captureException(error, {
          tags: { error_type: 'handled' },
          extra: { test_info: 'This error was manually captured' },
        });
        return Response.json(
          {
            success: true,
            message: 'Handled error sent to Sentry',
            type: 'handled',
          },
          { status: 200 }
        );
      }

    case 'message':
      // Capture message (not an error)
      Sentry.captureMessage('Test message - Info level', 'info');
      return Response.json(
        {
          success: true,
          message: 'Test message sent to Sentry',
          type: 'message',
        },
        { status: 200 }
      );

    case 'warning':
      // Capture warning
      Sentry.captureMessage('Test warning message', 'warning');
      return Response.json(
        {
          success: true,
          message: 'Warning sent to Sentry',
          type: 'warning',
        },
        { status: 200 }
      );

    default:
      throw new Error(`Test error - Unknown type: ${type}`);
  }
}

// Also handle POST for more realistic testing
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    Sentry.setContext('test_error_post', {
      body_keys: Object.keys(body),
      timestamp: new Date().toISOString(),
    });

    if (body.shouldFail) {
      throw new Error('Test POST error - Intentional failure');
    }

    return Response.json({ success: true, received: body });
  } catch (error) {
    if (error instanceof SyntaxError) {
      // JSON parse error
      Sentry.captureException(error, { tags: { error_type: 'json_parse' } });
      return Response.json({ error: 'Invalid JSON' }, { status: 400 });
    }
    throw error;
  }
}
