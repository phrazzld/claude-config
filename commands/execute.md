# Execute the next task

## ACQUISITION

Select the next available ticket from the `TODO.md` queue that is not blocked. Prioritize in progress `[~]` tickets. If none are available, grab the next unblocked unstarted `[ ]` ticket. If all tickets in `TODO.md` are completed, immediately halt execution and say something witty and relevant.

## CONTEXT GATHERING

Conduct a comprehensive review of all relevant materials. This must include, but is not limited to, the primary codebase, associated Leyline documentation, and external web resources via the Context7 MCP. Think hard about them, particularly in the context of the task.

If the task's complexity warrants it, invoke the `thinktank` CLI for advanced analysis.

## STRATEGIC PLANNING

Think very hard about what John Carmack would do, and construct a formal plan of execution.

## IMPLEMENTATION

Execute the approved plan until the task is fully resolved. If, at any point during execution, you encounter unexpected information, hiccups, blockers, or circumstances that you think might meaningfully change what the best course of action is, halt and report back to the user what the situation is and what new information we need to consider before we proceed.

## CLEANUP

Upon successful completion, update the ticket's status to [x] in TODO.md.
