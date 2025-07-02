Perform a comprehensive security audit of the codebase, identifying vulnerabilities and creating remediation plans.

# AUDIT

## GOAL
Perform a comprehensive security audit of the codebase, identifying potential vulnerabilities and creating a remediation plan.

## 1. Init Workspace
- Create `SECURITY_AUDIT.md` (Sections: Scope & Goals, Methodology Notes, Exploratory Log, Deep Dive Log).
- Create `SECURITY_PLAN.md` (Sections: Summary, Findings & Recommendations).
- !git add SECURITY_AUDIT.md SECURITY_PLAN.md

## 2. Exploratory Review
- **Goal:** Scan codebase/artifacts for potential weaknesses.
- **Methodology:** Use multiple techniques (Keyword Search, Data Flow Analysis, Component Review [Auth, Session, Input, Crypto, Errors, Deps, Config], Pattern Recognition [OWASP Top 10]). Log approach notes in `SECURITY_AUDIT.MD` -> `Methodology Notes`.
- **Action:** Log potential issues (description, path:line, thoughts) in `SECURITY_AUDIT.md` -> `Exploratory Findings Log`.

## 3. Deep-Dive Analysis
- **Goal:** Investigate exploratory findings to confirm vulnerabilities and assess impact.
- **Actions:**
    - Prioritize findings from Exploratory Log.
    - For each item:
        - Think hard: Analyze code logic.
        - Use security tools (SAST, dependency checkers) if available.
        - Document detailed findings, evidence, impact, confidence level in `SECURITY_AUDIT.MD` -> `Deep Dive Analysis Log`.
        - Assign preliminary severity (Low, Medium, High).

## 4. Create Remediation Plan
- **Goal:** Generate a structured, actionable plan from deep-dive findings.
- **Actions:**
    - Create `AUDIT-CONTEXT.md` with the findings from the security audit:
      ```markdown
      # Security Audit Findings
      
      [Include a summary of the findings from SECURITY_AUDIT.md]
      
      ## Critical Issues
      [List critical security vulnerabilities]
      
      ## High Priority Issues
      [List high priority security issues]
      
      ## Medium/Low Priority Issues
      [List less severe issues]
      ```
    - Think very hard about creating a comprehensive remediation plan:
      - Prioritize findings by risk severity and exploitation likelihood
      - Consider implementation complexity and resource requirements
      - Develop specific, actionable remediation steps for each vulnerability
      - Include security testing and validation procedures
      - Plan for security regression prevention
      - Consider defense-in-depth strategies
      - Identify quick wins vs long-term security improvements
    - Create `SECURITY_PLAN.md` with:
      - Executive summary of security posture
      - Detailed findings with evidence and impact analysis
      - Prioritized remediation roadmap
      - Specific code changes and security controls needed
      - Testing and validation requirements
      - Timeline and resource estimates