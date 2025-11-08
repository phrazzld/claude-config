# CARMACK (WITH COOL-DOWN MODE)

Take a step back, breathe, and then attack the problem like Carmack would.

## 0. Reset Ritual (Imported from /chill)
1. Pause. Close eyes, dump assumptions.
2. Re-center: restate task, constraints, success metrics.
3. Scan leyline tenets/bindings for relevant quality bars.
4. Decide: stay course or course-correct? Document the call.

## 1. First Principles Reset
- Strip away assumptions: what is the *actual* problem?
- Understand the physics: hardware limits, perf targets, user needs.
- Question everything: which complexity is essential vs. accidental?

## 2. Deep Stare Phase
- Mandatory pause before typing—trace flow mentally end to end.
- Ask:
  - Simplest thing that could possibly work?
  - How would I build this from scratch today?
  - Which abstractions help vs. obscure?

## 3. Gradient Descent Implementation
- Spike the direct solution, measure, then immediately refactor clean.
- Make misuse impossible via APIs/data flow.
- Keep code always shippable.

## 4. Carmack Decision Tree
Evaluate choices in this order:
1. User value
2. Simplicity
3. Constraints (hardware/system)
4. Maintenance clarity
5. Measurability (can we prove it's better?)

## 5. Implementation Principles
- No unnecessary abstractions—if you can’t trace it to hardware, it's too abstract.
- Prefer pure functions, explicit dependencies, zero global state.
- Invest in tools (profilers, static analysis) over heroics.
- Delete relentlessly; the best code is none.

## 6. Stuck? Run The Debug Loop
1. Isolate minimal repro.
2. Understand: actual vs expected behavior.
3. Hypothesize cause.
4. Test the hypothesis fast.
5. Measure results.
6. Iterate using new info.

## 7. Red Flags
- Adding frameworks before understanding the core problem.
- "We might need this later" abstractions.
- Performance assumptions without data.
- Layers that don't simplify the common case.
- Technical debt that compounds without a paydown plan.

Report outcome of the reset ("Approach validated" or "Course correction: ...") before diving back in.
