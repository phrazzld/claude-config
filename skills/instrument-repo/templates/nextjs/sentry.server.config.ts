import * as Sentry from "@sentry/nextjs";

import { createSentryOptions } from "./lib/sentry";

const options = createSentryOptions("server");

Sentry.init(options);
