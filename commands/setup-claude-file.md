# Setup Claude File Command - Generate Comprehensive Project-Specific CLAUDE.md

Generate a deeply analyzed, project-specific CLAUDE.md file that provides Claude with comprehensive context, patterns, and guidance for working effectively within the project.

**Usage**: `/user:setup-claude-file`

## Implementation Instructions

Create a comprehensive CLAUDE.md file through exhaustive project analysis, parallel expert consultation, web research, and intelligent synthesis of findings into actionable guidance.

### Command Generation Process

This command operates through several coordinated phases to create the most effective CLAUDE.md possible:

## Phase 1: Foundation Discovery & Context Mapping

**Analyze Project Architecture**
1. **Technology Stack Detection**
   - Scan package.json, Cargo.toml, go.mod, requirements.txt, etc.
   - Identify primary languages, frameworks, and build tools
   - Detect architectural patterns (MVC, microservices, monolith, etc.)
   - Map dependency relationships and critical libraries
   - Understand deployment and infrastructure patterns

2. **Codebase Structure Analysis**
   - Map directory structure and naming conventions
   - Identify entry points, core modules, and data flow patterns
   - Analyze test structure and testing frameworks
   - Detect CI/CD configuration and automation
   - Find configuration management patterns

3. **Development Workflow Detection**
   - Check for existing documentation (README, CONTRIBUTING, etc.)
   - Identify version control patterns and branching strategies
   - Detect quality gates (linting, formatting, pre-commit hooks)
   - Analyze issue tracking and project management integration
   - Understand release and deployment processes

4. **Leyline Integration Assessment**
   - Check for existing leyline documents in `./docs/leyline/`
   - Identify which leyline tenets and bindings are most relevant
   - Assess current adherence to leyline principles
   - Map project patterns to leyline binding recommendations

## Phase 2: Multi-Expert Parallel Analysis

Launch parallel subagents using the Task tool for comprehensive expert analysis. Each subagent should run independently and in parallel for maximum efficiency. All subagents must operate in research/investigation mode only - they should NOT modify code, use plan mode, or create files. They should output all thoughts, findings, and analysis directly to chat.

### **Task 1: John Carmack - Systems Architecture Expert**
**Prompt**: "As John Carmack, analyze this project's codebase focusing on architectural decisions, performance characteristics, and system design patterns. What are the core algorithms and data structures? How is complexity managed? What would be the most efficient approaches for extending this system? Consider computational complexity, memory management, and elegant mathematical solutions. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### **Task 2: Martin Fowler - Software Architecture & Design Patterns**
**Prompt**: "As Martin Fowler, analyze this project's architecture and design patterns. What architectural styles are being used? How is the code organized for maintainability? What refactoring opportunities exist? How well does the current design support testing and evolution? Focus on enterprise patterns, domain modeling, and architectural decision records. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### **Task 3: Kelsey Hightower - DevOps & Infrastructure**
**Prompt**: "As Kelsey Hightower, analyze this project's infrastructure, deployment, and operational characteristics. How is the application built, tested, and deployed? What are the infrastructure requirements? How would you optimize the development and deployment pipeline? Consider containerization, cloud-native patterns, and operational excellence. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### **Task 4: DHH (David Heinemeier Hansson) - Developer Experience & Productivity**
**Prompt**: "As DHH, analyze this project from a developer productivity and experience perspective. What makes this codebase easy or difficult to work with? How could developer ergonomics be improved? What conventions and patterns make the code more or less accessible? Focus on developer happiness, convention over configuration, and practical productivity. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### **Task 5: Brendan Eich - Language & Framework Expertise**
**Prompt**: "As a language and framework expert, analyze the specific technologies used in this project. What are the idiomatic patterns for this tech stack? What are common pitfalls and best practices? How should someone work effectively within these technology constraints? Focus on language-specific patterns, framework conventions, and ecosystem best practices. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

### **Task 6: Linus Torvalds - Pragmatic Engineering Excellence**
**Prompt**: "As Linus Torvalds, analyze this project with a focus on practical engineering excellence. What works well and what doesn't? How would you improve the maintainability and reliability? What are the most important things to get right when working on this codebase? Focus on no-nonsense engineering, scalability, and robust system design. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your analysis directly to chat."

## Phase 3: Research & Documentation Discovery

### **External Research Phase**
1. **Web Research for Best Practices**
   - Research best practices for the detected technology stack
   - Find architectural patterns and common pitfalls for the framework
   - Discover testing strategies and tooling recommendations
   - Identify security considerations and performance optimization techniques

2. **Context7 Documentation Research**
   - Use mcp__context7__resolve-library-id for detected frameworks and libraries
   - Fetch comprehensive documentation for major dependencies
   - Research integration patterns and configuration best practices
   - Understand API usage patterns and recommended approaches

3. **Leyline Principle Mapping**
   - Map detected patterns to relevant leyline tenets and bindings
   - Identify which leyline principles are most applicable
   - Suggest specific binding implementations for this project
   - Recommend leyline-based improvements and practices

## Phase 4: Project Context Integration

### **Task 7: Integration Synthesis Agent**
**Prompt**: "You are a senior technical lead responsible for synthesizing all expert analysis into coherent project guidance. Review all expert analyses, research findings, and project characteristics. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your synthesis directly to chat. Create an integrated understanding of:

1. **Core Project Identity**: What this project is, its purpose, and unique characteristics
2. **Technical Architecture**: Key architectural decisions and their implications
3. **Development Patterns**: How code should be written and organized
4. **Critical Constraints**: Technical, business, and operational limitations
5. **Success Patterns**: What approaches work best for this specific project
6. **Risk Areas**: Common pitfalls and areas requiring special attention

Synthesize these into clear, actionable guidance for Claude when working on this project."

## Phase 5: CLAUDE.md Generation & Synthesis

### **Final CLAUDE.md Structure**

Generate a comprehensive CLAUDE.md file with the following structure:

```markdown
# Claude's Guide to [Project Name]

## What is [Project Name]?

[Comprehensive project description synthesized from all analysis]

## Your Role

[Clear definition of Claude's role based on project type and needs]

## Project Architecture & Technology Stack

### Core Technologies
[Detected technologies with context about their usage]

### Architectural Patterns
[Key architectural decisions and their implications]

### Critical Dependencies
[Important libraries/frameworks and how they're used]

## Development Workflow

### Getting Started
[How to set up the development environment]

### Key Files and Directories
[Important files Claude should know about]

### Testing Strategy
[How testing is organized and executed]

### Quality Gates
[Linting, formatting, and other quality checks]

## Coding Style & Conventions

### Language-Specific Patterns
[Idiomatic patterns for the primary language(s)]

### Project-Specific Conventions
[Naming, organization, and structural conventions]

### Architecture Guidelines
[How to structure new code and modifications]

## Common Tasks & Patterns

### [Task Category 1]
[How to approach common development tasks]

### [Task Category 2]
[Patterns for typical operations]

## Critical Constraints & Requirements

### Technical Constraints
[Performance, compatibility, and technical limitations]

### Business Requirements
[Domain-specific rules and requirements]

### Security Considerations
[Security patterns and requirements]

## Warning Signs & Pitfalls

### Common Mistakes
[Typical errors when working with this stack]

### Anti-Patterns
[What to avoid in this specific project]

### Performance Considerations
[Performance-sensitive areas and optimization guidance]

## Debugging & Troubleshooting

### Common Issues
[Frequent problems and their solutions]

### Debugging Tools
[Available debugging tools and techniques]

### Log Analysis
[How to interpret logs and error messages]

## Testing & Validation

### Test Structure
[How tests are organized]

### Testing Best Practices
[Effective testing patterns for this project]

### Validation Strategies
[How to ensure changes work correctly]

## Deployment & Operations

### Build Process
[How the project is built and packaged]

### Deployment Strategy
[How changes are deployed]

### Monitoring & Observability
[How to monitor the application]

## Collaboration & Communication

### Code Review Guidelines
[How code reviews work in this project]

### Documentation Standards
[Documentation expectations and patterns]

### Issue Management
[How to handle bugs and feature requests]

## Leyline Integration

### Applicable Tenets
[Relevant leyline tenets for this project]

### Recommended Bindings
[Specific leyline bindings to implement]

### Improvement Opportunities
[Areas where leyline principles could enhance the project]

## Extended Context

### Domain Knowledge
[Business domain context and terminology]

### Historical Context
[Important architectural decisions and their rationale]

### Future Considerations
[Planned improvements and strategic direction]
```

## Phase 6: Quality Assurance & Validation

### **Task 8: Quality Review Agent**
**Prompt**: "Review the generated CLAUDE.md file for completeness, accuracy, and usefulness. IMPORTANT: You are in research mode only - do not modify any code, do not use plan mode, and output all your review findings directly to chat. Ensure that:

1. **Completeness**: All critical project aspects are covered
2. **Accuracy**: Technical details match the actual codebase
3. **Actionability**: Guidance is specific and immediately useful
4. **Clarity**: Instructions are clear and unambiguous
5. **Relevance**: Content focuses on what Claude actually needs to know
6. **Integration**: All expert insights are properly synthesized

Provide specific recommendations for improvements and ensure the final CLAUDE.md will make Claude maximally effective when working on this project."

### **Final Output Generation**

1. **Create the CLAUDE.md file** in the project root
2. **Validate completeness** against all analysis findings
3. **Ensure actionability** of all guidance provided
4. **Confirm integration** of all expert perspectives
5. **Test practicality** by reviewing against common project tasks

## Success Criteria

The generated CLAUDE.md file should:

- **Provide comprehensive project context** that enables Claude to understand the project's purpose, architecture, and constraints immediately
- **Include specific, actionable guidance** for common development tasks and decisions
- **Integrate all expert perspectives** into coherent, non-contradictory advice
- **Reference actual project patterns** rather than generic best practices
- **Enable effective collaboration** by establishing clear conventions and expectations
- **Anticipate common issues** and provide preventive guidance
- **Support long-term maintenance** by documenting architectural decisions and their rationale
- **Align with leyline principles** while respecting project-specific constraints
- **Serve as a living document** that can evolve with the project

## Execution Instructions

1. **Begin with comprehensive project analysis** using all available tools (Glob, Grep, Read, etc.)
2. **Launch all expert subagents in parallel using the Task tool** to maximize analysis efficiency - each subagent operates independently in research mode only
3. **Conduct thorough external research** using WebSearch and Context7 MCP
4. **Synthesize findings through integration agents** to create coherent guidance
5. **Generate the CLAUDE.md file** using the structured template above
6. **Validate the output** through quality review processes
7. **Present the final CLAUDE.md** with a summary of key insights and recommendations

Execute this comprehensive analysis and generation process now, creating a CLAUDE.md file that makes Claude maximally effective when working on this specific project.