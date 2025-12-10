#!/bin/bash
# Initialize Sentry in a Next.js project
# This script automates the Sentry setup process

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"
source "$SCRIPT_DIR/_common.sh"

# Default options
FRAMEWORK=""
PROJECT_SLUG=""
SKIP_VERCEL=false
DRY_RUN=false

HELP_TEXT="Usage: $(basename "$0") [OPTIONS]

Initialize Sentry error tracking in the current project.

Options:
  --framework FRAMEWORK  Framework type: nextjs, react, node (default: auto-detect)
  --project SLUG         Sentry project slug to use
  --skip-vercel          Skip Vercel Integration prompts
  --dry-run              Show what would be done without making changes
  --help                 Show this help message

Examples:
  $(basename "$0")                    # Auto-detect and set up
  $(basename "$0") --framework nextjs # Force Next.js setup
  $(basename "$0") --dry-run          # Preview changes"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --framework)
      FRAMEWORK="$2"
      shift 2
      ;;
    --project)
      PROJECT_SLUG="$2"
      shift 2
      ;;
    --skip-vercel)
      SKIP_VERCEL=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      show_help "$HELP_TEXT"
      exit 0
      ;;
    *)
      die "Unknown option: $1. Use --help for usage."
      ;;
  esac
done

# Detect framework if not specified
detect_framework() {
  if [ -n "$FRAMEWORK" ]; then
    echo "$FRAMEWORK"
    return
  fi

  if [ -f "package.json" ]; then
    # Check for Next.js
    if grep -q '"next"' package.json 2>/dev/null; then
      echo "nextjs"
      return
    fi
    # Check for React
    if grep -q '"react"' package.json 2>/dev/null; then
      echo "react"
      return
    fi
  fi

  # Default to Node.js
  echo "node"
}

# Detect package manager
detect_package_manager() {
  if [ -f "pnpm-lock.yaml" ]; then
    echo "pnpm"
  elif [ -f "yarn.lock" ]; then
    echo "yarn"
  elif [ -f "bun.lockb" ]; then
    echo "bun"
  else
    echo "npm"
  fi
}

# Run a command (or print if dry run)
run_cmd() {
  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN]${NC} $*"
  else
    info "Running: $*"
    "$@"
  fi
}

# Copy template file
copy_template() {
  local src="$1"
  local dest="$2"

  if [ ! -f "$src" ]; then
    warn "Template not found: $src"
    return 1
  fi

  if [ -f "$dest" ]; then
    warn "File already exists: $dest (skipping)"
    return 0
  fi

  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN]${NC} Copy $src → $dest"
  else
    info "Creating $dest"
    cp "$src" "$dest"
  fi
}

# Main setup
main() {
  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║             Sentry Initialization Script                      ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""

  # Check if already configured
  if "$SCRIPT_DIR/detect_sentry.sh" --json 2>/dev/null | grep -q '"status": "configured"'; then
    warn "Sentry appears to already be configured in this project."
    echo "Run verify_setup.sh to check the configuration."
    exit 0
  fi

  # Detect environment
  DETECTED_FRAMEWORK=$(detect_framework)
  PKG_MANAGER=$(detect_package_manager)

  info "Detected framework: $DETECTED_FRAMEWORK"
  info "Detected package manager: $PKG_MANAGER"
  echo ""

  # Step 1: Install packages
  echo "Step 1: Installing Sentry packages"
  echo "-----------------------------------"

  case $DETECTED_FRAMEWORK in
    nextjs)
      case $PKG_MANAGER in
        pnpm)
          run_cmd pnpm add @sentry/nextjs
          ;;
        yarn)
          run_cmd yarn add @sentry/nextjs
          ;;
        bun)
          run_cmd bun add @sentry/nextjs
          ;;
        *)
          run_cmd npm install @sentry/nextjs
          ;;
      esac
      ;;
    react)
      case $PKG_MANAGER in
        pnpm)
          run_cmd pnpm add @sentry/react
          ;;
        *)
          run_cmd npm install @sentry/react
          ;;
      esac
      ;;
    node)
      case $PKG_MANAGER in
        pnpm)
          run_cmd pnpm add @sentry/node
          ;;
        *)
          run_cmd npm install @sentry/node
          ;;
      esac
      ;;
  esac

  echo ""

  # Step 2: Run Sentry wizard (for Next.js)
  if [ "$DETECTED_FRAMEWORK" = "nextjs" ]; then
    echo "Step 2: Running Sentry setup wizard"
    echo "------------------------------------"
    echo "The wizard will guide you through the configuration."
    echo ""

    if [ "$DRY_RUN" = true ]; then
      echo -e "${YELLOW}[DRY RUN]${NC} npx @sentry/wizard@latest -i nextjs"
    else
      echo "Running: npx @sentry/wizard@latest -i nextjs"
      echo ""
      npx @sentry/wizard@latest -i nextjs || true
    fi

    echo ""
  fi

  # Step 3: Create config files from templates (if wizard didn't create them)
  echo "Step 3: Ensuring configuration files exist"
  echo "-------------------------------------------"

  if [ "$DETECTED_FRAMEWORK" = "nextjs" ]; then
    copy_template "$TEMPLATES_DIR/sentry.client.config.ts" "sentry.client.config.ts"
    copy_template "$TEMPLATES_DIR/sentry.server.config.ts" "sentry.server.config.ts"
  fi

  echo ""

  # Step 4: Create test error route
  echo "Step 4: Creating test error route"
  echo "----------------------------------"

  if [ "$DETECTED_FRAMEWORK" = "nextjs" ]; then
    if [ -d "app" ]; then
      if [ ! -d "app/test-error" ]; then
        if [ "$DRY_RUN" = true ]; then
          echo -e "${YELLOW}[DRY RUN]${NC} mkdir -p app/test-error"
        else
          mkdir -p app/test-error
        fi
      fi
      copy_template "$TEMPLATES_DIR/test-error-route.ts" "app/test-error/route.ts"
    else
      warn "No 'app' directory found. Skipping test error route."
    fi
  fi

  echo ""

  # Step 5: Add environment variable placeholders
  echo "Step 5: Environment variables"
  echo "-----------------------------"

  if [ -f ".env.local.example" ] || [ -f ".env.example" ]; then
    info "Adding Sentry env vars to example file"
    local env_example="${env_file:-.env.local.example}"

    if [ "$DRY_RUN" = false ] && [ -f "$env_example" ]; then
      if ! grep -q "SENTRY_DSN" "$env_example" 2>/dev/null; then
        cat >> "$env_example" << 'EOF'

# Sentry
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_DSN=
# Optional: Override auto-detected values
# SENTRY_ORG=
# SENTRY_PROJECT=
# SENTRY_AUTH_TOKEN=
EOF
        success "Added Sentry variables to $env_example"
      fi
    fi
  else
    copy_template "$TEMPLATES_DIR/env.sentry.example" ".env.sentry.example"
    info "Created .env.sentry.example - merge with your .env.local"
  fi

  echo ""

  # Final instructions
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║                    Setup Complete!                           ║"
  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
  echo "Next steps:"
  echo ""

  if [ "$SKIP_VERCEL" = false ]; then
    echo "  1. Install Vercel Integration (recommended):"
    echo "     https://vercel.com/integrations/sentry"
    echo ""
    echo "  2. Or manually set environment variables:"
    echo "     - NEXT_PUBLIC_SENTRY_DSN"
    echo "     - SENTRY_DSN"
    echo "     - SENTRY_AUTH_TOKEN"
    echo "     - SENTRY_ORG"
    echo "     - SENTRY_PROJECT"
    echo ""
  fi

  echo "  3. Test the setup:"
  echo "     curl http://localhost:3000/test-error"
  echo ""
  echo "  4. Verify in Sentry dashboard:"
  echo "     https://sentry.io"
  echo ""
  echo "  5. Verify configuration:"
  echo "     ~/.claude/skills/sentry-observability/scripts/verify_setup.sh"
  echo ""
}

main "$@"
