# Claude Commands

This directory contains custom slash commands for use with Claude Code CLI, providing structured workflows for various software development tasks.

## Purpose

These commands provide standardized templates and workflows that help maintain consistency across development activities. Each command is designed to follow best practices and ensure comprehensive coverage of critical aspects of the task at hand.

## Available Commands

- **audit.md** - Create security audit documentation for codebases
- **breathe.md** - Promote reflection and mindfulness during development
- **chill.md** - Reduce development stress and maintain perspective
- **consult.md** - Document problems and request architectural assistance
- **debug.md** - Structured approach to diagnosing and fixing bugs
- **execute.md** - Implement tasks from TODO lists with best practices
- **ideate.md** - Generate and explore creative solution alternatives
- **plan.md** - Create detailed technical plans for backlog items
- **prime.md** - Gather context from key repository files
- **push.md** - Quality assurance steps before committing code
- **refactor.md** - Create structured plans for improving code quality
- **resolve.md** - Troubleshoot and fix specific issues
- **review.md** - Establish code review processes and documentation
- **ticket.md** - Convert plans into prioritized task tickets

## Relationship to Prompts

Each command in this directory corresponds to a template in the `/docs/prompts/` directory. The commands are the executable implementations that leverage the templates to provide standardized workflows.

## Usage

These commands are installed by the main `install.sh` script which creates the necessary symbolic links. Once installed, they can be invoked directly from the Claude Code CLI with the corresponding slash command.

Example:
```
/prime
```

This will run the prime command to gather important context from key repository files.

## Development

When creating new commands or modifying existing ones:
1. Follow the established format for consistency
2. Ensure command structure is clear and focused on a specific workflow
3. Include appropriate sections for preparation, execution, and follow-up actions
4. Create or update the corresponding prompt template in `/docs/prompts/`
5. Update this README to document any new commands