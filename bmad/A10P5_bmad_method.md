# BMAD-METHOD™ Guide

## Introduction

Welcome to the BMAD-METHOD™ practical guide! This document will walk you through the complete BMAD™ workflow using various specialized agents. BMAD-METHOD™ (Breakthrough Method for Agile AI Driven Development) is a comprehensive framework for software development that emphasizes structured documentation, clear workflows, and quality checkpoints.

**Reference Material:** 
- [The Official BMad-Method Masterclass (The Complete IDE Workflow)](https://www.youtube.com/watch?v=LorEJPrALcg)
- [BMAD-METHOD™ Repository](https://github.com/bmad-code-org/BMAD-METHOD/)
- [BMAD-AISG-AIML](https://github.com/aisingapore/bmad-aisg-aiml)

## Installation Guide

### Prerequisites
Before installing BMAD-METHOD™, ensure you have:
- Node.js v20+ installed on your system
- npx v9+ installed on your system
- npm v9+ installed on your system
- VS Code
- Claude Code installed on your system
- `Claude Code for VSCode` installed in VS Code.

### Install version 4.40.0
Install at project level
```bash
npx bmad-method@4.40.0 install
```

## Overview of BMAD™ Agents

BMAD™ utilizes specialized agents, each with specific expertise and use cases:

- **Analyst Agent** - Use for market research, brainstorming, competitive analysis, creating project briefs, initial project discovery, and documenting existing projects (brownfield)
- **PM Agent** - Use for creating PRDs, product strategy, feature prioritization, roadmap planning, and stakeholder communication
- **Architect Agent** - Use for system design, architecture documents, technology selection, API design, and infrastructure planning
- **PO Agent** - Use for backlog management, story refinement, acceptance criteria, sprint planning, and prioritization decisions
- **SM Agent** - Use for story creation, epic management, retrospectives in party-mode, and agile process guidance
- **Dev Agent** - Use for code implementation, debugging, refactoring, and development best practices
- **QA Agent** - Use for senior code review, refactoring, test planning, quality assurance, and mentoring through code improvements
- **UX Expert** - Use for UI/UX design, wireframes, prototypes, front-end specifications, and user experience optimization
- **BMAD™ Master** - Use when you need comprehensive expertise across all domains, running 1 off tasks that do not require a persona, or just wanting to use the same agent for many things
- **BMAD™ Orchestrator** - Use for workflow coordination, multi-agent tasks, role switching guidance, and when unsure which specialist to consult

## Practical Exercises

### Exercise 1: Creating a Brainstorming Document with Analyst Agent

The Analyst Agent helps facilitate structured brainstorming sessions to gather ideas and requirements.

**How to use:**
```
# Load Analyst agent
/BMad:agents:analyst

# Run brainstorm to facilitate structured brainstorming session and create brainstorming-session-results.md document
*brainstorm {topic}
```

**What happens:**
1. The analyst agent loads the brainstorming session facilitation task
2. Guides you through selecting appropriate brainstorming techniques
3. Helps structure and capture ideas systematically
4. Creates a `brainstorming-session-results.md` document with organized results

**Example Output Structure:**
```markdown
# Brainstorming Session: [Topic]

## Session Details
- Date: [Date]
- Participants: [List]
- Technique Used: [Mind Mapping/SCAMPER/etc.]

## Ideas Generated
### Category 1
- Idea A
- Idea B

### Category 2
- Idea C
- Idea D

## Next Steps
- Prioritized action items
```

**When done:**
```
# Run *exit to exit Analyst agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 2: Creating a Project Brief with Analyst Agent

The project brief captures the essential overview and context of your project.

**How to use:**
```
# Load Analyst agent
/BMad:agents:analyst

# Run create-project-brief to create brief.md document
*create-project-brief
```

**What happens:**
1. The analyst loads the project brief template
2. Guides you through each section with targeted questions
3. Ensures comprehensive coverage of project context
4. Outputs a complete `brief.md` document

**Key Sections Created:**
- Executive Summary
- Problem Statement
- Objectives & Goals
- Stakeholders
- Success Criteria
- Constraints & Assumptions

**When done:**
```
# Run *exit to exit Analyst agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 3: Creating a PRD with PM Agent

The Product Requirements Document (PRD) is the cornerstone of product definition.

**How to use:**
```
# Load PM agent
/BMad:agents:pm

# Run create-prd to create prd.md document
*create-prd
```

**What happens:**
1. PM agent loads the PRD template
2. Systematically elicits information for each section
3. Ensures alignment with business objectives
4. Creates a comprehensive `prd.md` document

**PRD Structure:**
```markdown
# Product Requirements Document

## Product Vision
[Clear statement of what we're building and why]

## User Stories
[Detailed user scenarios and requirements]

## Functional Requirements
[Specific features and capabilities]

## Non-Functional Requirements
[Performance, security, usability standards]

## Success Metrics
[How we measure success]
```

**When done:**
```
# Run *exit to exit PM agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 4: Creating Architecture Documentation with Architect Agent

Technical architecture documentation ensures robust system design.

**How to use:**
```
# Load Architect agent
/BMad:agents:architect

# Run create-backend-architecture to create architecture.md document
*create-backend-architecture
```

**What happens:**
1. Architect agent loads architecture template
2. Guides through technical design decisions
3. Documents system components and interactions
4. Produces `architecture.md` with diagrams and specifications

**Architecture Components:**
- System Overview
- Component Design
- Data Architecture
- Security Architecture
- Deployment Architecture
- Technology Stack

**When done:**
```
# Run *exit to exit Architect agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 5: Sharding Documents with Shard-Doc Task

Large documents can be broken into manageable pieces for parallel development.

**How to use:**
```
# Load PM agent
/BMad:agents:pm

# Run shard-prd to shard provided prd.md
*shard-prd '/path/to/your/prd.md'

# Run *exit to exit PM agent
*exit

# Run /clear to clear conversation history and free up context
/clear

# Load Architect agent
/BMad:agents:architect

# Run shard-prd to shard provided architecture.md
*shard-prd '/path/to/your/architecture.md'

# Run *exit to exit Architect agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

**What happens:**
1. Analyzes the source document structure
2. Identifies logical boundaries and sections
3. Creates smaller, focused documents
4. Maintains traceability between shards

**Benefits:**
- Enables parallel work streams
- Improves focus on specific areas
- Facilitates incremental development
- Simplifies review processes

### Exercise 6: Running Checklists with PO Agent

The Product Owner agent ensures quality through systematic checklist execution.

**How to use:**
```
# Load PO agent
/BMad:agents:po

# Run execute-checklist-po to execute checklist
*execute-checklist-po
```

**What happens:**
1. PO agent loads the specified checklist
2. Guides through each checkpoint
3. Records compliance status
4. Identifies gaps and action items
5. Generates compliance report

**Common Checklists:**
- Story Definition of Done
- Sprint Planning Checklist
- Release Readiness Checklist
- Architecture Review Checklist

**When done:**
```
# Run *exit to exit PO agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 7: Writing User Stories with SM Agent

The Scrum Master agent helps create well-formed user stories.

**How to use:**
```
# Load SM agent
/BMad:agents:sm

# Run draft to create user story
*draft {story number, e.g: 1.1}
```

**What happens:**
1. SM agent loads story creation workflow
2. Elicits story details using standard format
3. Ensures acceptance criteria are clear
4. Creates story document with proper structure

**Story Format:**
```markdown
# Story: [Title]

## User Story
As a [role]
I want [feature]
So that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Notes
[Implementation considerations]

## Effort Estimate
[Story points or time estimate]
```

**Change Story Status**
- After review the story, change story status from "draft" to "approved" for Dev Agent to develop the story

**When done:**
```
# Run *exit to exit SM agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 8: Implementing Stories with Dev Agent

The Developer agent guides implementation following best practices.

**How to use:**
```
# Load Dev agent
/BMad:agents:dev

# Run develop-story to implement user story
*develop-story '/path/to/your/stories/1.1.story.md'
```

**What happens:**
1. Dev agent analyzes story requirements
2. Creates implementation plan
3. Guides through coding standards
4. Ensures test coverage
5. Documents implementation decisions

**Implementation Workflow:**
1. Understand requirements
2. Design solution approach
3. Implement core functionality
4. Add error handling
5. Write tests
6. Document code
7. Create pull request

**When done:**
```
# Run *exit to exit Dev agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

### Exercise 9: Testing Implementation with QA Agent

The QA agent ensures quality through comprehensive testing.

**How to use:**
```
# Load QA agent
/BMad:agents:qa

# Run review to review user story
*review '/path/to/your/stories/1.1.story.md'
```

**What happens:**
1. QA agent reviews implementation against requirements
2. Creates test scenarios
3. Executes test cases
4. Documents findings
5. Provides quality metrics

**Testing Levels:**
- Unit Testing
- Integration Testing
- Functional Testing
- Acceptance Testing
- Performance Testing
- Security Testing

**When done:**
```
# Run *exit to exit QA agent
*exit

# Run /clear to clear conversation history and free up context
/clear
```

## Complete Workflow Example

Here's how all agents work together in a typical project:
- Remember to run "/clear" to clear conversation history and free up context when switching agent

### Phase 1: Planning
```bash
# 1. Brainstorm ideas
/BMad:agents:analyst
*brainstorm {topic}

# 2. Create project brief
/BMad:agents:analyst
*create-project-brief

# 3. Define product requirements
/BMad:agents:pm
*create-prd

# 4. Design system architecture
/BMad:agents:architect
*create-backend-architecture

# 5. Shard documents
/BMad:agents:pm
# Run shard-prd to shard provided prd.md
*shard-prd

/BMad:agents:architect
# Run shard-prd to shard provided architecture.md
*shard-prd

# 6. Run quality checklists
/BMad:agents:po
*execute-checklist-po
```

### Phase 2: Development
```bash
# 7. Create user stories
/BMad:agents:sm
*draft

# 8. Implement stories
/BMad:agents:dev
*develop-story

# 9. Test implementation
/BMad:agents:qa
*review
```

## Advanced Tips

### 1. Customizing Templates
You can modify templates to match your organization's needs while maintaining BMAD™ structure.

### 2. Chaining Commands
Execute multiple commands in sequence for efficient workflow:
```bash
*create-doc prd && *shard-doc prd.md stories/
```

### 3. Knowledge Base Integration
Use `*kb` command with BMAD™ Master agent to access BMAD™ knowledge base for detailed methodology information.

### 4. Yolo Mode
For experienced users, toggle `*yolo` to skip confirmations and work faster (use with caution).

## BMAD-METHOD™ in AI Singapore

### BMAD™ AI/ML Engineering Expansion Pack:
- AI Singapore specialized agents
- AI Singapore program-specific workflows (MVP, POC, SIP, LADP)
- Specialized templates for ML/LLM development
- Unified AI security, ethics, and governance

### Agents:
- ML/AI Engineer & MLOps Specialist (`ml-engineer`)
- ML/AI System Architect (`ml-architect`)
- Senior Data Scientist (`ml-data-scientist`)
- ML Security & Ethics Specialist (`ml-security-ethics-specialist`)
- ML Research Scientist & Experimental Design Specialist (`ml-researcher`)

### Workflows:
- 6-Month MVP Projects (`aisg-mvp-workflow`)
- 3-Month POC Projects (`aisg-poc-workflow`)
- 3-Month SIP - Short Industry Projects (`aisg-sip-workflow`)
- 4-Month LADP - LLM Application Developer Programme (`aisg-ladp-workflow`)

## Conclusion

The BMAD-METHOD™ provides a structured approach to software development through specialized agents and defined workflows. By following these exercises, you've learned how to:

- Leverage specialized agents for different phases
- Create comprehensive documentation
- Maintain quality through checklists
- Implement stories systematically
- Test thoroughly

Remember: BMAD-METHOD™ is about bringing method to the madness of software development. Use these tools consistently, and you'll see improved project outcomes, better documentation, and higher quality deliverables.