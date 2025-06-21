# SETUP

## GOAL
Initialize a project with opinionated defaults, link leyline documents, and create a detailed TODO list tailored to the project type.

## 1. Verify Environment
- Ensure the `DEVELOPMENT` environment variable is set and points to the root of your development directory.
- If `DEVELOPMENT` is unset or invalid, exit with an error:
  ```bash
  if [ -z "$DEVELOPMENT" ] || [ ! -d "$DEVELOPMENT" ]; then
    echo "Error: DEVELOPMENT variable not set or not a directory."
    exit 1
  fi
  ```

## 2. Detect Project Type
- Determine the project type by examining files:
  ```bash
  # Initialize variables
  IS_NODE=false
  IS_GO=false
  IS_RUST=false
  IS_FRONTEND=false
  PROJECT_NAME=$(basename "$(pwd)")

  # Create docs directory if it doesn't exist
  mkdir -p docs

  # Check for Node.js/TypeScript
  if [ -f "package.json" ]; then
    IS_NODE=true
    echo "Detected Node.js project"
    
    # Check if it's a frontend project
    if grep -q "\"react\"\|\"vue\"\|\"angular\"\|\"svelte\"" package.json; then
      IS_FRONTEND=true
      echo "Detected frontend framework"
    fi
  fi

  # Check for Go
  if [ -f "go.mod" ]; then
    IS_GO=true
    echo "Detected Go project"
  fi

  # Check for Rust
  if [ -f "Cargo.toml" ]; then
    IS_RUST=true
    echo "Detected Rust project"
  fi
  ```

## 3. Symlink Leyline Documents
- Link language-specific leyline documents based on detected project type:
  ```bash
  # Link TypeScript appendix if Node.js project
  if [ "$IS_NODE" = true ]; then
    ln -sfn "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md" docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_TYPESCRIPT.md
    echo "Linked TypeScript development philosophy appendix"
  fi

  # Link Go appendix if Go project
  if [ "$IS_GO" = true ]; then
    ln -sfn "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_GO.md" docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_GO.md
    echo "Linked Go development philosophy appendix"
  fi

  # Link Rust appendix if Rust project
  if [ "$IS_RUST" = true ]; then
    ln -sfn "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_RUST.md" docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_RUST.md
    echo "Linked Rust development philosophy appendix"
  fi

  # Link Frontend appendix if frontend project
  if [ "$IS_FRONTEND" = true ]; then
    ln -sfn "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_FRONTEND.md" docs/DEVELOPMENT_PHILOSOPHY_APPENDIX_FRONTEND.md
    echo "Linked Frontend development philosophy appendix"
  fi
  ```

## 4. Link Prompts Directory
- Link the prompts directory:
  ```bash
  ln -sfn "$DEVELOPMENT/codex/docs/prompts" docs/prompts
  echo "Linked prompts directory"
  ```

## 5. Create TODO.md
- Generate a comprehensive TODO.md file with project-specific tasks:
  ```bash
  cat > "TODO.md" << EOF
# Project Setup TODO List

## Infrastructure
- [ ] Set up GitHub Actions CI
  - [ ] Create .github/workflows directory
  - [ ] Create CI workflow for running on push and pull requests
  - [ ] Configure tests to run in CI
  - [ ] Configure linters and type checking
  - [ ] Set up test coverage reporting
  - [ ] Add badge to README.md

## Git Hooks
- [ ] Configure pre-commit hooks
  - [ ] Install pre-commit framework
  - [ ] Configure linting and formatting checks
  - [ ] Add type checking
  - [ ] Prevent commit of sensitive data and large files
  - [ ] Enforce conventional commit format
- [ ] Configure post-commit hooks
  - [ ] Set up \`glance ./\` to run async
  - [ ] Generate documentation updates if needed
- [ ] Configure pre-push hooks
  - [ ] Run complete test suite
  - [ ] Enforce branch naming conventions

## Quality Standards
- [ ] Implement file length enforcement
  - [ ] Configure warning at 500 lines
  - [ ] Configure error at 1000 lines
- [ ] Set up conventional commits
  - [ ] Add commitlint configuration
  - [ ] Document commit message standards
- [ ] Configure semantic versioning
  - [ ] Set up automated versioning based on commits
  - [ ] Configure CHANGELOG generation
EOF

  # Add Node.js specific tasks if detected
  if [ "$IS_NODE" = true ]; then
    cat >> "TODO.md" << EOF

## Node.js/TypeScript Setup
- [ ] Configure strict TypeScript compiler options
  - [ ] Enable strict mode in tsconfig.json
  - [ ] Set noImplicitAny to true
  - [ ] Configure strictNullChecks
- [ ] Set up ESLint with strict rules
  - [ ] Configure @typescript-eslint
  - [ ] Forbid \`any\` type
  - [ ] Enforce explicit return types
- [ ] Configure Prettier for consistent formatting
- [ ] Set up testing framework
  - [ ] Choose Jest or Vitest
  - [ ] Configure test coverage thresholds (>85%)
  - [ ] Set up consistent test patterns
- [ ] Implement structured logging
  - [ ] Add Winston or Pino
  - [ ] Configure JSON format for production
  - [ ] Set up context propagation
EOF
  fi

  # Add Go specific tasks if detected
  if [ "$IS_GO" = true ]; then
    cat >> "TODO.md" << EOF

## Go Setup
- [ ] Configure golangci-lint with strict rules
  - [ ] Create .golangci.yml
  - [ ] Enable errcheck, gosimple, govet, etc.
  - [ ] Set reasonable complexity thresholds
- [ ] Organize directory structure
  - [ ] Follow standard Go project layout
  - [ ] Set up cmd, internal, pkg directories
- [ ] Configure testing
  - [ ] Set up table-driven tests
  - [ ] Configure integration tests
  - [ ] Set up test coverage tooling
- [ ] Implement structured logging
  - [ ] Configure log/slog (Go 1.21+)
  - [ ] Set up JSON formatter
  - [ ] Implement correlation ID tracking
EOF
  fi

  # Add Rust specific tasks if detected
  if [ "$IS_RUST" = true ]; then
    cat >> "TODO.md" << EOF

## Rust Setup
- [ ] Configure Clippy with strict lints
  - [ ] Create clippy.toml
  - [ ] Set reasonable complexity thresholds
- [ ] Configure rustfmt for consistent formatting
- [ ] Set up comprehensive testing
  - [ ] Configure unit tests
  - [ ] Set up integration tests
  - [ ] Add doc tests
- [ ] Implement error handling strategy
  - [ ] Set up custom error types
  - [ ] Use thiserror/anyhow appropriately
- [ ] Configure structured logging
  - [ ] Add tracing or log crate
  - [ ] Set up JSON formatter
  - [ ] Implement span hierarchy
EOF
  fi

  # Add frontend specific tasks if detected
  if [ "$IS_FRONTEND" = true ]; then
    cat >> "TODO.md" << EOF

## Frontend Setup
- [ ] Set up Storybook
  - [ ] Initialize Storybook
  - [ ] Configure component documentation
  - [ ] Add accessibility plugin
  - [ ] Set up visual testing
- [ ] Configure component testing
  - [ ] Set up React Testing Library or Vue Test Utils
  - [ ] Create test patterns for components
  - [ ] Add snapshot testing
- [ ] Implement styling strategy
  - [ ] Choose and configure CSS approach
  - [ ] Set up design tokens
  - [ ] Add responsive design utilities
- [ ] Configure state management
  - [ ] Choose appropriate solution
  - [ ] Set up dev tools
- [ ] Set up accessibility standards
  - [ ] Configure axe-core for testing
  - [ ] Add eslint-plugin-jsx-a11y
  - [ ] Implement keyboard navigation utilities
EOF
  fi

  # Add documentation tasks
  cat >> "TODO.md" << EOF

## Documentation
- [ ] Create comprehensive README.md
  - [ ] Project description and purpose
  - [ ] Features list
  - [ ] Installation instructions
  - [ ] Usage examples with code
  - [ ] Development setup guide
  - [ ] Contribution guidelines
- [ ] Add MIT LICENSE file
  - [ ] Update year and copyright holder
- [ ] Create CONTRIBUTING.md
  - [ ] Document development workflow
  - [ ] Explain branch and PR conventions
  - [ ] Add code style and testing requirements
EOF

  echo "Created detailed TODO.md with project-specific tasks"
  ```

## 6. Verify Setup
- Confirm that all links were created properly:
  ```bash
  echo "Verifying setup..."
  ls -l docs/DEVELOPMENT_PHILOSOPHY.md docs/prompts
  
  echo "Setup complete! A detailed TODO.md file has been created."
  echo "Review TODO.md and start implementing the recommended configurations."
  ```
