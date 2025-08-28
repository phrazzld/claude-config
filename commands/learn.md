Master computer science fundamentals through deep analysis of your actual code and implementation decisions.

# LEARN

Generate comprehensive CS learning analysis by examining your code through three specialized educational lenses: recent algorithmic decisions, performance optimization opportunities, and theoretical connections to CS principles.

**Pure Focus**: Deep algorithmic understanding + architectural decision-making

## Process

Launch three CS-education subagents in parallel to analyze different aspects of your code for learning:

1. **Algorithm Analysis**: What choices did I make and why? What are the alternatives?
2. **Performance Analysis**: Where can I optimize and what CS concepts does that teach?
3. **Concept Analysis**: How do my implementations connect to fundamental CS theory?

## Implementation

**Launch the three learning subagents**:

Use Task tool to launch these subagents in parallel:

```
Task 1: "Algorithm Archaeologist - Act as algorithm-archaeologist from /Users/phaedrus/.claude/agents/learning/algorithm-archaeologist.md. Analyze recent code changes to understand algorithmic choices, alternatives, and trade-offs. Focus on decision analysis and CS concept learning."

Task 2: "Performance Professor - Act as performance-professor from /Users/phaedrus/.claude/agents/learning/performance-professor.md. Identify performance bottlenecks and optimization opportunities that teach CS concepts. Focus on complexity analysis and algorithmic improvements."

Task 3: "CS Concept Connector - Act as cs-concept-connector from /Users/phaedrus/.claude/agents/learning/cs-concept-connector.md. Connect code implementations to fundamental CS theory and principles. Focus on bridging practice to theoretical understanding."
```

## Synthesis

After all three subagents complete their analysis:

1. **Algorithmic Decision Analysis**: Recent choices and their alternatives
2. **Performance Learning Opportunities**: Bottlenecks that teach optimization
3. **CS Theory Connections**: How code relates to fundamental principles
4. **Deep Learning Guide**: Comprehensive understanding of CS concepts in context

**Output**: Create `cs-learning-analysis.md` with deep educational insights.

## Learning Focus Areas

- **Algorithmic Trade-offs**: Understanding why certain choices were made
- **Complexity Analysis**: Real-world performance implications of algorithmic decisions
- **Data Structure Selection**: When and why to choose specific structures  
- **Optimization Strategies**: Performance improvements that teach CS principles
- **Architectural Patterns**: How algorithms support system design
- **Theory-Practice Bridge**: Connecting implementations to CS fundamentals

## Success Criteria

✓ Algorithm analysis explains decision rationale and alternatives
✓ Performance analysis finds optimization opportunities with learning value
✓ Concept analysis connects code to fundamental CS theory
✓ Synthesis creates deep understanding of CS principles in context
✓ Learning guide enables better architectural decision-making