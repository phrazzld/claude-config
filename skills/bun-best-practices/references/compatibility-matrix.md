# Bun Compatibility Matrix

Last updated: 2025-02

## Package Managers & Build Tools

| Tool | Bun Support | Notes |
|------|-------------|-------|
| Turborepo | ✅ Full | Works as drop-in replacement |
| Nx | ✅ Full | Supports Bun executors |
| Lerna | ⚠️ Partial | Some commands may not work |
| npm scripts | ✅ Full | `bun run` compatible |

## Frameworks

| Framework | Bun Runtime | Bun Package Manager | Notes |
|-----------|-------------|---------------------|-------|
| Next.js | ⚠️ Experimental | ✅ Full | Use `--bun` flag for runtime |
| Remix | ✅ Full | ✅ Full | Good support |
| Astro | ✅ Full | ✅ Full | Good support |
| SvelteKit | ⚠️ Partial | ✅ Full | Some adapters may not work |
| Nuxt | ⚠️ Partial | ✅ Full | Limited runtime support |
| Vite | ✅ Full | ✅ Full | Excellent support |
| Expo/EAS | ❌ No | ❌ No | Requires Node.js |

## Testing

| Tool | Bun Support | Notes |
|------|-------------|-------|
| Bun Test | ✅ Native | Jest-compatible API |
| Vitest | ✅ Full | Bun runner available |
| Jest | ⚠️ Partial | Use Bun test instead |
| Playwright | ✅ Full | Works well |
| Cypress | ✅ Full | Works well |

## Databases & ORMs

| Tool | Bun Support | Notes |
|------|-------------|-------|
| Drizzle ORM | ✅ Full | Excellent support |
| Prisma | ⚠️ Partial | Some features limited |
| Convex | ❓ Verify | Check current docs |
| better-sqlite3 | ✅ Native | Bun has built-in SQLite |
| pg (PostgreSQL) | ✅ Full | Works well |

## Deployment Platforms

| Platform | Bun Runtime | Notes |
|----------|-------------|-------|
| Fly.io | ✅ Full | Excellent support |
| Railway | ✅ Full | Good support |
| Render | ✅ Full | Good support |
| Vercel | ⚠️ Experimental | Limited to Edge runtime |
| Netlify | ❌ No | Node.js only |
| AWS Lambda | ⚠️ Custom | Requires custom runtime |
| Cloudflare Workers | ✅ Full | Good support |

## Native Modules

| Module Type | Bun Support | Notes |
|-------------|-------------|-------|
| Pure JS | ✅ Full | No issues |
| WASM | ✅ Full | Good support |
| N-API | ⚠️ Partial | Check specific module |
| node-gyp | ⚠️ Partial | Some modules work |

## Common Problem Packages

These packages are known to have issues with Bun:

| Package | Issue | Workaround |
|---------|-------|------------|
| `sharp` | Native bindings | Usually works, test first |
| `bcrypt` | Native bindings | Use `bcryptjs` instead |
| `canvas` | Native bindings | May not work |
| `puppeteer` | Chrome downloads | Use `playwright` |

## Checking Compatibility

Before migration:

```bash
# List all dependencies
bun pm ls

# Check for known issues
npx bunx bun-check # (hypothetical tool)

# Test critical paths
bun test
bun run build
bun run start
```

## Resources

- [Bun Node.js Compatibility](https://bun.sh/docs/runtime/nodejs-apis)
- [Bun GitHub Issues](https://github.com/oven-sh/bun/issues)
