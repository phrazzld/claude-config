# README Templates

## Application README

```markdown
# Project Name

Brief description (1-2 sentences).

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start

```bash
git clone https://github.com/user/repo
cd repo
pnpm install
cp .env.example .env.local
# Edit .env.local with your values
pnpm dev
```

Open http://localhost:3000

## Prerequisites

- Node.js 22+
- pnpm 9+
- [Other requirements]

## Configuration

Copy `.env.example` to `.env.local` and configure:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `NEXT_PUBLIC_API_URL` | API base URL | Yes |

## Development

```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm test         # Run tests
pnpm lint         # Run linter
```

## Architecture

See [docs/CODEBASE_MAP.md](docs/CODEBASE_MAP.md) for detailed architecture.

## License

MIT
```

## Library README

```markdown
# library-name

[![npm version](https://img.shields.io/npm/v/library-name.svg)](https://www.npmjs.com/package/library-name)
[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](https://github.com/user/repo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Brief description of what the library does.

## Installation

```bash
npm install library-name
# or
pnpm add library-name
```

## Quick Start

```typescript
import { feature } from 'library-name'

const result = feature({ option: 'value' })
console.log(result)
```

## API

### `feature(options)`

Description of the main function.

**Parameters:**
- `options.setting` (string, required): What this does
- `options.flag` (boolean, optional): Enable/disable feature

**Returns:** `Result` - The result object

**Example:**
```typescript
const result = feature({
  setting: 'value',
  flag: true
})
```

### `otherFunction()`

[Repeat for each public API]

## Examples

### Basic Usage

```typescript
// Simple example
```

### Advanced Usage

```typescript
// Complex example with multiple features
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
```

## CLI Tool README

```markdown
# cli-name

Command-line tool for [purpose].

## Installation

```bash
# With npm
npm install -g cli-name

# With Homebrew
brew install cli-name

# From source
cargo install --path .
```

## Usage

```bash
cli-name <command> [options]
```

### Commands

#### `init`

Initialize a new project.

```bash
cli-name init my-project
cli-name init my-project --template typescript
```

**Options:**
- `--template, -t`: Project template to use
- `--force, -f`: Overwrite existing files

#### `build`

Build the project.

```bash
cli-name build
cli-name build --watch
```

**Options:**
- `--watch, -w`: Watch for changes
- `--output, -o`: Output directory

### Global Options

- `--help, -h`: Show help
- `--version, -v`: Show version
- `--verbose`: Verbose output

## Configuration

Create `cli-name.config.js` in your project root:

```javascript
module.exports = {
  setting: 'value',
  features: {
    enabled: true
  }
}
```

## Examples

### Example 1

```bash
# Description of what this example does
cli-name command --option value
```

### Example 2

```bash
# Another example
cli-name other-command
```

## License

MIT
```

## Monorepo README

```markdown
# Project Name

Monorepo for [project description].

## Packages

| Package | Description | Version |
|---------|-------------|---------|
| [@scope/app](packages/app) | Main application | ![npm](https://img.shields.io/npm/v/@scope/app.svg) |
| [@scope/ui](packages/ui) | UI component library | ![npm](https://img.shields.io/npm/v/@scope/ui.svg) |
| [@scope/utils](packages/utils) | Shared utilities | ![npm](https://img.shields.io/npm/v/@scope/utils.svg) |

## Quick Start

```bash
git clone https://github.com/user/repo
cd repo
pnpm install
pnpm dev
```

## Development

```bash
pnpm dev              # Start all packages in dev mode
pnpm build            # Build all packages
pnpm test             # Run all tests
pnpm lint             # Lint all packages
```

### Working with specific packages

```bash
pnpm --filter @scope/app dev     # Run specific package
pnpm --filter @scope/ui build    # Build specific package
```

## Project Structure

```
.
├── apps/
│   └── web/              # Main web application
├── packages/
│   ├── ui/               # Shared UI components
│   └── utils/            # Shared utilities
├── tools/                # Build and dev tools
└── turbo.json           # Turborepo configuration
```

## Adding a New Package

1. Create directory in `packages/`
2. Add `package.json` with `"name": "@scope/package-name"`
3. Update root `pnpm-workspace.yaml` if needed
4. Run `pnpm install`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
```
