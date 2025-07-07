# CARMACK

Take a step back and ultrathink: what would John Carmack do?

## The Carmack Framework for Technical Problem-Solving

### 1. **First Principles Reset**
- **Strip away assumptions**: What is the *actual* problem, divorced from implementation details?
- **Understand the physics**: What are the fundamental constraints (hardware, performance, user needs)?
- **Question everything**: Is this complexity necessary, or is it accumulated technical debt?

### 2. **The Deep Stare Phase** 
- **Mandatory pause**: Before writing code, stare at the problem and existing code
- **Trace execution mentally**: Follow data flow and control paths without debugger
- **Ask the hard questions**:
  - What is the simplest thing that could possibly work?
  - What would this look like if I built it from scratch today?
  - Which abstractions are helping vs. hiding complexity?

### 3. **Gradient Descent Implementation**
- **Start with the spike**: Build the most direct, inelegant solution first
- **Measure everything**: Performance, memory, actual user impact
- **Immediate refactoring**: Don't move on until the spike is cleaned up
- **Make error impossible**: Design APIs and data flows to prevent misuse

### 4. **Carmack's Decision Tree**
For any technical choice, evaluate in this order:
1. **User value**: Does this directly improve the end-user experience?
2. **Simplicity**: Is this the most direct path to the solution?
3. **Constraints**: Does this work within hardware/system limitations?
4. **Maintenance**: Will this make sense to future developers?
5. **Measurable**: Can I prove this works better than alternatives?

### 5. **Implementation Principles**
- **No unnecessary abstractions**: If you can't trace code to hardware, it's too abstract
- **Pure functions preferred**: Minimize side effects and global state
- **Always shippable**: Every commit should leave the codebase in a working state
- **Tools over heroics**: Invest in static analysis, linting, and automation
- **Delete code aggressively**: The best code is code you don't have to maintain

### 6. **When Stuck - The Carmack Debug Loop**
1. **Isolate**: Create the minimal reproduction of the problem
2. **Understand**: What specifically is happening vs. what you expected?
3. **Hypothesize**: What is the most likely root cause?
4. **Test**: Build the smallest possible test of your hypothesis
5. **Measure**: Did it work? What did you learn?
6. **Iterate**: Use the new information to refine understanding

### 7. **Red Flags That Would Make Carmack Cringe**
- Adding frameworks before understanding the problem
- "We might need this later" code
- Abstractions that don't simplify the common case
- Performance assumptions without measurement
- Complex architectures for simple problems
- Technical debt that compounds instead of being fixed immediately

**Remember**: Carmack's superpower isn't just technical skill - it's the discipline to step back, think deeply, and choose the direct path over the clever one.