Conduct rigorous root cause analysis using state-of-the-art techniques and multiple expert investigations to debug complex issues.

## GOAL

Execute the most comprehensive root cause analysis possible for the issue described in ISSUE.md by:
- Applying multiple proven RCA methodologies systematically
- Leveraging diverse expert perspectives through parallel investigations
- Synthesizing findings into concrete, actionable debug and fix plans
- Using state-of-the-art debugging techniques from 2024

## METHODOLOGY

This command implements a streamlined multi-phase approach combining:
- **Core RCA Techniques**: Five parallel specialist subagents applying Five Whys, Ishikawa Fishbone, Pareto Analysis, Fault Tree Analysis, and Bow Tie Analysis
- **Domain Analysis**: Systematic investigation across systems, security, performance, and user experience perspectives
- **Modern Debugging**: Integration of 2024 best practices including observability, chaos engineering, and SRE methodologies
- **Evidence-Based Synthesis**: Converging multiple analytical perspectives into concrete solutions

## EXECUTE

### Phase 1: Foundation Analysis

1. **Read and Understand ISSUE.md**
   - Parse the complete issue description, symptoms, and context
   - Identify affected systems, components, and user impact
   - Extract timeline information and reproduction steps
   - Note any previous debugging attempts or partial solutions

2. **Gather System Context**
   - Map out current codebase architecture and components
   - Identify system boundaries and dependencies
   - Check for relevant logs, monitoring data, or error traces
   - Review recent changes, deployments, or configuration updates
   - Search for similar historical issues or patterns

3. **Establish Investigation Baseline**
   - Define the problem scope and boundaries clearly
   - Identify what is working vs. what is broken
   - Document assumptions and known constraints
   - Set up the foundation for systematic investigation

### Phase 2: RCA Technique Specialists

Launch 5 parallel subagents using the Task tool, each specializing in a specific root cause analysis methodology. CRITICAL: All subagents operate in research mode only - they should NOT modify code, use plan mode, or create files. They must output all findings directly to chat.

**Task 1: Five Whys Investigator**
- Prompt: "As a Five Whys expert, conduct a systematic iterative investigation of the issue in ISSUE.md. Start with the primary symptom and ask 'Why?' repeatedly, drilling down through at least 5 levels to identify the true root cause. For each 'Why' question, provide specific evidence-based answers. Document your reasoning chain clearly and identify when you reach fundamental root causes vs. symptoms. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

**Task 2: Systems Analyst - Ishikawa Fishbone**
- Prompt: "As an Ishikawa Fishbone diagram expert, analyze the issue in ISSUE.md using cause-and-effect mapping. Create a comprehensive fishbone analysis covering all major cause categories: People (human factors), Process (procedures/workflows), Environment (context/conditions), Materials (data/inputs), Methods (techniques/approaches), and Machines (systems/tools). For each category, identify specific potential causes and sub-causes. Build a complete causal map from symptom to root causes. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

**Task 3: Data Detective - Pareto Analysis**
- Prompt: "As a Pareto Analysis expert, investigate the issue in ISSUE.md using statistical and data-driven approaches. Apply the 80/20 rule to identify the vital few causes that likely contribute to 80% of the problem impact. Search for patterns, frequencies, and quantifiable factors. Prioritize potential causes by their likelihood and impact. Use data mining techniques to uncover hidden correlations or trends. Focus on measurable evidence and statistical significance. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

**Task 4: Fault Tree Engineer**
- Prompt: "As a Fault Tree Analysis expert, investigate the issue in ISSUE.md using logical failure analysis. Create a top-down deductive analysis starting with the main failure event and systematically break it down into contributing causes using Boolean logic (AND/OR gates). Map all possible failure pathways and identify critical failure points. Analyze both immediate causes and underlying basic events. Calculate failure probabilities where possible and identify single points of failure. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

**Task 5: Risk Analyst - Bow Tie Analysis**
- Prompt: "As a Bow Tie Analysis expert, investigate the issue in ISSUE.md using comprehensive risk modeling. Create a bow-tie diagram with the main problem as the central knot. Analyze the left side (causes) using fault tree methodology to identify all pathways leading to the issue. Analyze the right side (consequences) using event tree methodology to map all potential impacts and escalations. Identify existing barriers/controls and their effectiveness. Assess both prevention and mitigation strategies. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### Phase 3: Domain Analysis

Conduct systematic investigation across key domain areas to complement the RCA findings:

1. **Systems Resilience Analysis**
   - Apply chaos engineering principles to understand failure modes
   - Identify brittleness, single points of failure, and cascade patterns
   - Evaluate system observability, monitoring gaps, and recovery mechanisms
   - Consider blast radius, fault isolation, and graceful degradation
   - Use systems thinking for emergent behaviors and complex interactions

2. **Operational Excellence Review**
   - Apply Four Golden Signals analysis (latency, traffic, errors, saturation)
   - Evaluate observability using MELT framework (Metrics, Events, Logs, Traces)
   - Assess SLO/SLI compliance and error budgets
   - Review incident response procedures and escalation paths
   - Analyze monitoring, alerting, and debugging workflows

3. **Security Implications Assessment**
   - Evaluate potential security-related causes (intrusion, vulnerabilities, breaches)
   - Assess attack surfaces, authentication/authorization gaps, data exposure risks
   - Consider internal and external threat actors
   - Review security logging and monitoring implications
   - Apply threat modeling and risk assessment methodologies

4. **Performance Investigation**
   - Analyze potential bottlenecks, resource constraints, and scaling issues
   - Evaluate CPU, memory, I/O, and network performance factors
   - Consider algorithmic complexity and architectural performance anti-patterns
   - Apply performance profiling and optimization techniques
   - Use binary search debugging and modern profiling approaches

5. **User Experience Impact**
   - Analyze effects on user workflows, productivity, and satisfaction
   - Consider accessibility implications and different user personas
   - Evaluate UI design, usability patterns, and interaction flows
   - Apply rubber duck debugging and user-centered design thinking
   - Assess communication, documentation, and user support implications

### Phase 4: Analysis Integration and Synthesis

1. **Technical Pattern Recognition**
   - Review all RCA specialist reports for converging technical evidence
   - Identify contradictions and synergies between different findings
   - Look for patterns where multiple methodologies point to same causes
   - Create unified technical hypothesis integrating strongest findings
   - Focus on actionable technical insights with concrete evidence

2. **Cross-Domain Correlation**
   - Integrate RCA findings with domain analysis results
   - Identify root causes spanning multiple domains (technical, operational, security, performance, UX)
   - Map cause-and-effect relationships across different system layers
   - Highlight areas of convergence vs. divergence in analysis

3. **Strategic Insight Development**
   - Identify high-level patterns, organizational factors, and systemic issues
   - Recognize process gaps, communication failures, and organizational anti-patterns
   - Consider long-term implications and prevention strategies
   - Develop strategic recommendations addressing root causes, not just symptoms

### Phase 5: Solution Planning and Final Synthesis

1. **Comprehensive Root Cause Identification**
   - Synthesize all specialist findings into a unified analysis
   - Identify the most likely root causes with supporting evidence
   - Distinguish between primary root causes and contributing factors
   - Validate findings against multiple methodologies and perspectives

2. **Impact and Priority Assessment**
   - Evaluate the severity and scope of identified root causes
   - Assess business impact, user impact, and technical debt implications
   - Prioritize causes by their contribution to the overall issue
   - Consider interdependencies and cascade effects

3. **Solution Strategy Development**
   - Design comprehensive fix strategy addressing all identified root causes
   - Create both immediate fixes and long-term preventive measures
   - Plan implementation phases with risk mitigation
   - Include validation and testing strategies

4. **Concrete Action Plan**
   - Document specific debugging steps and diagnostic procedures
   - Provide code changes, configuration updates, or architectural modifications
   - Include monitoring and alerting improvements
   - Create runbooks for future similar issues

5. **Prevention and Improvement Recommendations**
   - Identify process improvements and organizational changes
   - Recommend tooling, monitoring, and observability enhancements
   - Suggest training, documentation, or knowledge sharing initiatives
   - Provide metrics and success criteria for measuring improvement

## OUTPUT PROTOCOL

```
=== COMPREHENSIVE DEBUG ANALYSIS ===
Issue: [From ISSUE.md]
Analysis Date: [Current date]
Methodologies Applied: [List of all RCA techniques used]

--- PHASE 1: FOUNDATION ANALYSIS ---
🔍 ISSUE UNDERSTANDING
[Clear problem statement and scope]

🏗️ SYSTEM CONTEXT
[Architectural overview and component relationships]

📊 BASELINE ASSESSMENT
[Current state analysis and constraints]

--- PHASE 2: RCA TECHNIQUE ANALYSIS ---
🔄 FIVE WHYS INVESTIGATION
[Iterative root cause drilling results]

🐟 FISHBONE ANALYSIS
[Cause-and-effect mapping across all categories]

📈 PARETO ANALYSIS
[Statistical analysis and vital few identification]

🌳 FAULT TREE ANALYSIS
[Logical failure pathway mapping]

🎯 BOW TIE ANALYSIS
[Comprehensive risk modeling with causes and consequences]

--- PHASE 3: DOMAIN INVESTIGATION ---
⚡ CHAOS ENGINEERING PERSPECTIVE
[Systems resilience and failure mode analysis]

🔧 SRE OPERATIONAL ANALYSIS
[Observability, monitoring, and operational excellence review]

🔒 SECURITY IMPLICATIONS
[Attack vector and threat scenario analysis]

⚡ PERFORMANCE ENGINEERING
[Bottleneck and optimization analysis]

👥 USER EXPERIENCE IMPACT
[Human factors and user impact assessment]

--- PHASE 4: SYNTHESIS ---
🧠 TECHNICAL INTEGRATION
[Converging technical evidence and hypotheses]

🎯 STRATEGIC INSIGHTS
[High-level patterns and organizational factors]

--- PHASE 5: SOLUTION PLAN ---
🎯 ROOT CAUSE SUMMARY
[Primary root causes with confidence levels and evidence]

📋 IMMEDIATE ACTION PLAN
[Critical fixes and diagnostic procedures]

🏗️ LONG-TERM STRATEGY
[Architectural improvements and prevention measures]

📊 SUCCESS METRICS
[Validation criteria and monitoring recommendations]

⚠️ RISK MITIGATION
[Implementation risks and contingency plans]

🔮 FUTURE PREVENTION
[Process improvements and organizational recommendations]
```

## SUCCESS CRITERIA

- **Comprehensive Coverage**: All major RCA methodologies applied systematically
- **Multi-Methodology Validation**: Findings validated across 5 core RCA techniques plus domain analysis
- **Evidence-Based Conclusions**: All root causes supported by concrete evidence
- **Actionable Solutions**: Specific, implementable fixes and improvements
- **Prevention Focus**: Long-term solutions that prevent recurrence
- **Risk Assessment**: Clear understanding of implementation risks and mitigations

Execute this comprehensive multi-phase root cause analysis now, leveraging the full power of systematic debugging methodologies and diverse expert perspectives to solve the most challenging issues.
