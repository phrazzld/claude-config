# LOGGING

Establish a centralized local development logging subsystem, directing all client-side and server-side application event streams to a single, structured log file; implement a pre-execution log rotation policy that archives the prior session's log and initiates a new one, coupled with an automated cleanup routine to enforce a one-week log retention period, with all logs located in a designated, version-control-ignored directory.

Ultrathink about the best way to do this. Conduct a thorough and comprehensive investigation of the codebase to grok the landscape. Brainstorm different approaches, solutions, and tools for achieving this. Use the `gemini` cli tool with the `--prompt` flag, use web search, use the Context7 MCP server. Evaluate the tradeoffs of the most compelling approaches. Then propose a clear and detailed implementation plan for your strongly opinionated recommendation for the best design and best path forward.
