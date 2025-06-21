The `/Users/phaedrus/Development/codex/claude-commands` directory contains a collection of markdown files, each representing a distinct custom slash command designed for use with the Claude Code CLI. The primary purpose of these commands is to provide structured and standardized workflows for a variety of software development tasks, ensuring consistency and adherence to best practices across different development activities.

The architecture is template-based. Each command file serves as a blueprint, often referencing external documentation like the "leyline documents" (project principles and guidelines) and `glance.md` files (architectural insights). These commands typically involve several stages: context gathering, analysis, planning, execution, validation, and finalization. The commands often generate or modify files such as `TODO.md` (task lists), `PLAN.md` (implementation plans), and context files for specific tasks. Many commands also interact with the GitHub CLI (`gh`) to manage issues and pull requests.

Key files and their roles include:

*   **README.md:** Provides an overview of the directory's purpose, available commands, and development guidelines.
*   **\*.md (command files):** Each markdown file (e.g., `prime.md`, `setup.md`, `refactor.md`) defines a specific command. These files contain the logic, instructions, and often, embedded bash scripts to perform the desired task.
*   **BOARD.md:** Sets up a GitHub repository with standardized labels and issue templates.
*   **PRIME.md:** Gathers important context from key repository files.
*   **SETUP.md:** Initializes a project with opinionated defaults, links leyline documents, and creates a detailed TODO list.
*   **THINKTANK.md:** Creates a prompt for the `thinktank-wrapper` script, which leverages multiple AI models for code analysis and problem-solving.
*   **TODO.md:** (Generated or modified) Represents a task list for the project.
*   **PLAN.md:** (Generated) Contains detailed implementation plans for specific tasks.
*   **REVIEW.md:** Generates a code review based on a git diff.
*   **DEBUG.md:** Systematically identifies, analyzes, and creates a plan to fix bugs.
*   **EXECUTE.md:** Picks the next unblocked ticket from `TODO.md` and guides its completion.

Important dependencies and gotchas:

*   **GitHub CLI (`gh`):** Many commands rely on the GitHub CLI for interacting with GitHub repositories (e.g., creating issues, listing issues, creating pull requests).
*   **`thinktank-wrapper` script:** Some commands utilize a `thinktank-wrapper` script, which is assumed to be available in the environment. This script likely uses AI models to analyze code and generate solutions.
*   **Leyline documents:** A set of principles and guidelines that are crucial for many commands. The location of these documents is assumed to be in the `DEVELOPMENT/codex/docs/` directory, where `DEVELOPMENT` is an environment variable.
*   **Environment variables:** The `DEVELOPMENT` environment variable is critical for locating leyline documents and other project-specific resources.
*   **Conventional commits:** Enforced by pre-commit hooks.
*   **Project-specific context:** The effectiveness of these commands heavily relies on the specific context of the project they are being used in.
*   **File system operations:** The scripts within the command files perform file system operations (e.g., creating directories, creating files, linking files), which can have unintended consequences if not executed carefully.
*   **Bash scripting:** The commands heavily rely on bash scripting, so familiarity with bash syntax and best practices is necessary.
*   **Reliance on specific file names:** Many commands rely on specific file names (e.g., `BACKLOG.md`, `glance.md`) being present in the repository.
*   **Pre-commit hooks:** The commands often mention pre-commit hooks, which need to be properly configured for linting and formatting.
*   **Overengineering:** Several commands explicitly warn against overengineering.
*   **Context files:** Several commands create context files for other scripts.
*   **Testing Strategy:** Several commands discuss different testing strategies.
*   **The `obey.md` command:** This command indicates an expectation that instructions given to the user will be followed exactly.
*   **The `verify.md` command:** This command indicates an expectation that the `--no-verify` flag will only be used in exceptional circumstances and that these circumstances will be documented.
*   **The `multiline.md` command:** This command is a reminder to use multiline commit messages.
