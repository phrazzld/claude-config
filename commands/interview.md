Master FAANG interview patterns through targeted practice based on your code analysis.

# INTERVIEW

Generate personalized interview preparation plan by analyzing your code for classic interview patterns, identifying gaps, and creating targeted practice problems with mock interview scenarios.

**Pure Focus**: Pattern recognition speed + algorithm muscle memory for technical interviews

## Process

Launch three interview-specialized subagents in parallel to create comprehensive interview readiness assessment:

1. **Pattern Analysis**: What classic interview patterns appear in my code? What gaps exist?
2. **Problem Generation**: Create custom LeetCode-style problems targeting my weak areas  
3. **Interview Simulation**: Practice communication and time pressure scenarios

## Implementation

**Launch the three interview subagents**:

Use Task tool to launch these subagents in parallel:

```
Task 1: "Interview Pattern Expert - Act as interview-pattern-scout from /Users/phaedrus/.claude/agents/interview/interview-pattern-scout.md. Analyze the codebase to identify which of the ~20 core interview patterns are present and which are missing. Focus on pattern recognition gaps for FAANG interview preparation."

Task 2: "LeetCode Problem Generator - Act as leetcode-problem-generator from /Users/phaedrus/.claude/agents/interview/leetcode-problem-generator.md. Based on identified pattern gaps and code context, generate custom practice problems that drill weak areas. Focus on targeted skill development."

Task 3: "Interview Coach - Act as interview-coach from /Users/phaedrus/.claude/agents/interview/interview-coach.md. Create mock interview scenarios and communication practice based on code analysis. Focus on explanation skills and time pressure performance."
```

## Synthesis

After all three subagents complete their analysis:

1. **Pattern Mastery Status**: Current proficiency across core interview patterns
2. **Targeted Practice Plan**: Custom problems prioritized by impact on interview success
3. **Mock Interview Scenarios**: Communication drills and time pressure simulations
4. **Weekly Focus Recommendation**: Specific pattern to master this week

**Output**: Create `interview-readiness.md` with comprehensive prep plan.

## Core Interview Patterns Tracked

- **Two Pointers**: Fast/slow, opposite direction, sliding window
- **Hash Tables**: Counting, mapping, fast lookup
- **Trees**: Traversal, BST operations, tree construction  
- **Dynamic Programming**: 1D, 2D, knapsack variants
- **Binary Search**: Classic, rotated arrays, search space
- **Graphs**: BFS, DFS, shortest paths, topological sort
- **Arrays**: Sorting, merging, partitioning
- **Strings**: Pattern matching, manipulation, parsing
- **Heaps**: Top-K problems, merge operations
- **Backtracking**: Permutations, combinations, constraint satisfaction

## Success Criteria

✓ Pattern gap analysis identifies critical missing skills
✓ Generated problems target specific interview pattern weaknesses  
✓ Mock scenarios practice communication under time pressure
✓ Weekly focus plan provides clear path to interview readiness
✓ Progress tracking enables mastery measurement