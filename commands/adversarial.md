---
description: Adversarial multi-model review until genuine consensus
argument-hint: <file|issue|text>
---

# ADVERSARIAL

> **The goal isn't agreement—it's disagreement that survives scrutiny.**

One model reviewing a document will miss things. It'll gloss over gaps, accept vague requirements, and let edge cases slide. Multiple models arguing about it surfaces what one would miss.

## The Core Question

**"What problems would surface if five skeptical architects reviewed this independently?"**

## Your Role

You're orchestrating a review by hostile experts. Not hostile to the author—hostile to defects. Their job is to find problems before they become production incidents. Your job is to keep pressing until they've genuinely engaged, or until they've proven there's nothing left to find.

## Process

### 1. Load the Artifact

Read what you're reviewing:
- Issue number → `gh issue view $1 --comments`
- File path → read the file
- Quoted text → use directly

Understand what this artifact claims to specify. Note the scope and boundaries.

### 2. First Round: Skeptical Review

Write thinktank instructions that frame reviewers as skeptics:

**The prompt should convey:**
- You're reviewing something the team thinks is ready
- Your job is to find what they missed
- Generic approval is useless—cite specific evidence
- If you approve, prove you actually read it

Run thinktank with `--synthesis`. Read every model's output.

### 3. Challenge Shallow Responses

Some models will rubber-stamp. They'll say "looks good" without engagement. This is the failure mode the adversarial pattern exists to fix.

**Signs of rubber-stamping:**
- Brief responses without specific citations
- Generic praise: "comprehensive", "well-thought-out", "no major issues"
- No quotes from the actual artifact
- Suggestions that are tangential rather than targeted

When you see this, don't accept it. Write a challenge prompt that forces engagement:
- "Your response didn't cite any specific passages. Quote something problematic."
- "You said 'looks good'—what specific evidence supports this claim?"
- "Name three edge cases you tested mentally. What happens when they fail?"

Re-run with the challenge. Keep pressing until the model either finds real issues or demonstrates genuine engagement with the material.

### 4. Surface Disagreements

The interesting part isn't where models agree—it's where they disagree.

- Model A thinks the auth flow is fine; Model B sees a race condition
- Model A wants more abstraction; Model B thinks it's already over-engineered
- Model A missed something Model B caught

**Don't resolve these artificially.** Present them as open questions for the user. The disagreement itself is valuable signal.

### 5. User Review

After each round, pause. Present what you've learned:
- Where the models agree (high confidence findings)
- Where they disagree (needs human judgment)
- What's still unclear

Ask the user: continue, accept, inject feedback, or abort?

If they inject feedback ("focus on the database layer" or "ignore the UI stuff"), incorporate it into the next round's prompts.

### 6. Convergence

Keep going until:
- Models genuinely converge (citing same issues with evidence)
- User accepts the current state
- User decides the artifact needs revision before more review is useful

There's no fixed round limit. Stop when the review has produced actionable insight, not when you've hit an arbitrary number.

## What Good Looks Like

A successful adversarial review surfaces:
- Specific gaps with citations ("Section 3 says X but doesn't address Y")
- Edge cases the author didn't consider
- Requirements that conflict with each other
- Assumptions that aren't explicitly stated
- Where experts disagree and why

A failed review produces:
- Generic approval from all models
- Suggestions that could apply to any document
- No quotes from the actual artifact
- Consensus that wasn't earned through scrutiny

## Output

When done, report:
- Issues where all models agreed (high confidence)
- Issues where some models disagreed (flag for user)
- Conflicts that weren't resolved (user decides)
- What the artifact needs before it's ready to implement

Don't manufacture false confidence. If the review didn't converge, say so. If models disagreed on something important, surface it. The user needs to know what's solid and what's still uncertain.
