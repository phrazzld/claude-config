# Multi-Mind - Subagent-Based Collaborative Analysis

Execute a multi-specialist collaborative analysis using independent subagents.

**Usage**: `/project:multi-mind topic [rounds=3]`

## Implementation

Execute this multi-specialist analysis using the Task tool to create independent subagents:

### Phase 1: Specialist Assignment & Research

First, analyze the topic and determine 4-6 specialist roles needed. Then launch parallel subagents using the Task tool:

**Example Implementation**:
```
// Launch parallel specialist subagents
Task 1: "Technical Specialist"
- Prompt: "As a technical specialist, research [topic] focusing on implementation details, architecture, performance considerations, and technical challenges. Use WebSearch to find latest technical documentation and case studies."

Task 2: "Business Strategy Specialist"
- Prompt: "As a business strategy specialist, analyze [topic] from market dynamics, competitive landscape, ROI, and strategic positioning perspectives. Search for market reports and business analyses."

Task 3: "User Experience Specialist"
- Prompt: "As a UX specialist, investigate [topic] focusing on user needs, usability concerns, adoption barriers, and human factors. Find user studies and experience reports."

[Additional specialists as needed...]
```

Each subagent operates independently with access to WebSearch, Read, and analysis tools.

**Specialist Selection Criteria**:
- Unique domain expertise relevant to the topic
- Different methodological approaches (quantitative/qualitative, theoretical/practical, etc.)
- Varied temporal perspectives (historical, current, future-focused)
- Distinct risk/opportunity sensitivities
- Independent information sources and knowledge bases

### Phase 2: Cross-Pollination Round

After receiving all specialist reports, launch a second round of subagents:

```
Use the Task tool to launch subagents that:
1. Review all other specialists' findings
2. Identify intersections with their domain
3. Challenge assumptions from their perspective
4. Build on insights while maintaining distinct viewpoint
5. Flag blind spots in other analyses
```

### Phase 3: Synthesis & Iteration

For each round (default 3, user-configurable):
- Collect all subagent outputs
- Synthesize without homogenizing perspectives
- Identify emerging patterns
- Determine focus areas for next round
- Launch new subagent tasks with refined prompts

## Anti-Repetition Mechanisms

**Moderator Responsibilities**:
- Track what has been thoroughly covered vs. what needs deeper exploration
- Redirect specialists away from rehashing previous points
- Push for new angles, deeper analysis, or broader implications
- Synthesize without homogenizing distinct specialist perspectives

**Specialist Guidelines**:
- Build on previous round insights rather than restating them
- Focus on what your unique expertise adds to the collective understanding
- Search for information others likely missed due to their different focus areas
- Challenge the group's emerging consensus from your specialist perspective

## Output Protocol

```
=== MULTI-MIND ANALYSIS: [Topic] ===
Rounds: [X] | Specialists: [Dynamic assignment based on topic]

--- ROUND 1 ---
🔍 KNOWLEDGE ACQUISITION
[Each specialist's web research findings in their domain]

🎯 SPECIALIST ANALYSIS
[Each specialist's unique perspective and insights]

🔄 CROSS-POLLINATION
[Specialists engage with each other's findings]

⚖️ MODERATOR SYNTHESIS
[Progress assessment, key insights, next round focus]

--- ROUND 2 ---
[Repeat structure with deeper analysis building on Round 1]

--- FINAL SYNTHESIS ---
🧠 COLLECTIVE INTELLIGENCE OUTCOME
[Comprehensive insights from all specialist perspectives]

🎯 KEY INSIGHTS
[Most valuable discoveries from the multi-mind process]

⚠️ REMAINING UNCERTAINTIES
[What the collective analysis couldn't resolve]

🔮 IMPLICATIONS
[Forward-looking insights for decision-making]
```

## Success Metrics
- Each round produces genuinely new insights (not repetition)
- Specialists maintain distinct valuable perspectives throughout
- Web research continuously introduces fresh information
- Cross-pollination generates insights no single specialist would reach
- Collective outcome exceeds sum of individual specialist contributions
- Different error types are caught by different specialists' approaches

Execute the multi-mind analysis starting with dynamic specialist assignment based on topic complexity and domain requirements.
