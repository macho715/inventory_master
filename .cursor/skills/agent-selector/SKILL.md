---
name: agent-selector
description: Select appropriate agent for task and understand agent capabilities, permissions, and workflow dependencies. Use when deciding which agent to use, understanding agent roles, or planning multi-agent workflows.
---

# Agent Selector

## Quick Reference

### Agent Capabilities Matrix

| Agent | Model | Read/Write | Primary Use Case | Dependencies |
|-------|-------|------------|------------------|--------------|
| `explore` | fast | read-only | Codebase structure mapping | - |
| `planner` | inherit | read-only | plan.json design/validation | `explore` (optional) |
| `implementer` | inherit | **write** | Code implementation (after approval) | `planner`, `tdd-go` |
| `executor` | inherit | **write** | File operations (after approval) | `approver` |
| `approver` | fast | read-only | Approval token validation | `plan-validate` |
| `reviewer` | fast | read-only | Security/quality review | - |
| `verifier` | fast | read-only | Post-operation verification | `implementer`/`executor` |
| `researcher` | fast | read-only | Documentation/Everything integration | - |
| `qa` | fast | **write** | Test case creation | - |
| `coordinator` | fast | read-only | Multi-agent workflow orchestration | - |

## Selection Guide

### When to Use Each Agent

**`explore`** - First-time codebase exploration
- Mapping repository structure
- Finding key entry points
- Architecture validation
- Before planning or implementation

**`planner`** - Plan design and validation
- Creating plan.json structure
- Applying classification rules
- Detecting path conflicts
- Before `plan-gated-apply` skill

**`implementer`** - Code implementation (⚠️ requires approval)
- TDD cycle: RED → GREEN → REFACTOR
- Implementing from `plan.md` tests
- Minimal changes to pass tests
- After approval gate passed

**`executor`** - File operations (⚠️ requires approval)
- Applying approved plan.json
- File moves/renames
- Transactional operations
- After `approver` validation

**`approver`** - Approval gate management
- Validating approval tokens
- Checking approval status
- Before `executor` execution (mandatory)
- Approval workflow coordination

**`reviewer`** - Security and quality review
- Security vulnerability assessment
- Code quality metrics
- Pre-release validation
- Risk evaluation

**`verifier`** - Post-operation verification
- Test execution validation
- Snapshot comparison
- Hash verification
- After any write operation

**`researcher`** - Documentation and research
- Everything integration docs
- Security policy documentation
- Provider setup guides
- Read-only research tasks

**`qa`** - Test case creation
- Writing failure case tests
- Edge case scenarios
- Integration test setup
- Test file creation only

**`coordinator`** - Workflow orchestration
- Multi-agent workflow design
- Dependency order validation
- Step-by-step guidance
- Complex workflow planning

## Workflow Patterns

### Development Workflow
```
explore → planner → plan-gated-apply → implementer → verifier
```

### File Organization Workflow
```
inventory-report → planner → plan-gated-apply → executor → verifier
```

### TDD Workflow
```
tdd-go → plan.md → implementer → verifier
```

### Approval Workflow
```
planner → plan-validate → approval-gate → approver → executor
```

## Safety Rules

### Write Operations (⚠️ Approval Required)
- `implementer`: Requires approval before code changes
- `executor`: Requires approval token before file operations
- `qa`: Test files only, no approval needed

### Read-Only Agents (Safe)
- `explore`, `planner`, `approver`, `reviewer`, `verifier`, `researcher`, `coordinator`
- Can be used without approval
- No file modifications

## Integration Points

### Agent Dependencies
- `planner` → may use `explore` for structure analysis
- `implementer` → requires `planner` or `tdd-go` skill
- `executor` → requires `approver` validation
- `verifier` → follows `implementer` or `executor`

### Skill Dependencies
- `plan-gated-apply` → uses `planner` agent
- `tdd-go` → uses `implementer` agent
- `approval-gate` → uses `approver` agent
- `inventory-report` → may use `explore` agent

## Decision Tree

**Need to write code?**
- Yes → `implementer` (after approval)
- No → Continue below

**Need to move files?**
- Yes → `executor` (after approval)
- No → Continue below

**Need to create plan?**
- Yes → `planner`
- No → Continue below

**Need to verify work?**
- Yes → `verifier`
- No → Continue below

**Need to review quality?**
- Yes → `reviewer`
- No → Continue below

**Need to explore codebase?**
- Yes → `explore`
- No → Use `coordinator` for workflow planning

## Common Scenarios

### Scenario: "I need to implement a feature"
1. `explore` - Understand codebase structure
2. `planner` - Design implementation plan (if needed)
3. `approval-gate` - Get approval (if write needed)
4. `implementer` - Write code
5. `verifier` - Verify tests pass

### Scenario: "I need to organize files"
1. `inventory-report` - Current state analysis
2. `planner` - Create plan.json
3. `plan-validate` - Validate plan
4. `approval-gate` - Get approval
5. `approver` - Verify approval token
6. `executor` - Apply file operations
7. `verifier` - Verify results

### Scenario: "I need to write tests"
1. `qa` - Create test cases
2. `verifier` - Run and verify tests

## Restrictions

- **Never bypass approval**: Write agents require approval
- **Follow dependency order**: Use agents in correct sequence
- **Verify after write**: Always use `verifier` after write operations
- **Read-only first**: Use read-only agents for exploration before write

## Skills Quick Reference

### Skills by Category

| Skill | Type | Dependencies | Primary Use Case |
|-------|------|--------------|------------------|
| `everything-provider-setup` | Setup | - | Everything ES CLI/HTTP setup |
| `everything-test` | Test | `everything-provider-setup` | Everything connectivity test |
| `tdd-go` | Development | `plan.md` | TDD cycle execution |
| `plan-gated-apply` | Safety | `planner` agent | File move/rename (Plan→Approve→Apply) |
| `plan-validate` | Validation | `planner` agent | Plan validation (pre-approval) |
| `approval-gate` | Safety | `plan-validate` | Approval workflow management |
| `inventory-report` | Report | Everything | Weekly/monthly audits |
| `quarantine-audit` | Policy | `plan-gated-apply` | Delete request handling |
| `snapshot-verify` | Validation | `executor` agent | Snapshot integrity check |
| `audit-query` | Query | - | Audit log queries |
| `repo-bootstrap` | Initialization | - | New repo setup |
| `ci-precommit` | Quality | - | CI/Pre-commit hooks |
| `release-check` | Validation | `ci-precommit` | Pre-release checklist |

### When to Use Skills vs Agents

**Use Skills when:**
- You need a specific procedure/workflow
- You need to execute a multi-step process
- You need to follow a standardized workflow

**Use Agents when:**
- You need specialized expertise/role
- You need to perform a specific type of analysis
- You need role-based guidance

**Key Principle**: Agents are "who" (roles), Skills are "what" (procedures)

## Complete Workflow Examples

### New Feature Development
```
explore → tdd-go → implementer → verifier
```

### File Organization
```
inventory-report → planner → plan-gated-apply → executor → verifier
```

### Release Preparation
```
release-check → reviewer → ci-precommit
```

### Initial Setup
```
repo-bootstrap → everything-provider-setup → ci-precommit
```

## Additional Resources

- For complete workflow examples: `docs/AGENTS_AND_SKILLS_GUIDE.md` (SSOT)
- For agent definitions: `.cursor/agents/*.md`
- For skill definitions: `.cursor/skills/*/SKILL.md`
- For architecture details: `agent.md` (SSOT)
- For dependency maps: `docs/DEPENDENCY_MAP.md`
