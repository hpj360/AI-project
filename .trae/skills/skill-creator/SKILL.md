---
name: skill-creator
description: Create, evaluate, and iterate on Agent Skills. Use this when users want to build, refine, or package custom skills for Claude Code or similar AI coding environments. Guides users through skill design, implementation, testing, and packaging with a structured three-agent workflow.
---

# Skill Creator

A complete workflow for creating, evaluating, and iterating on Agent Skills.

## What this skill does

This skill helps you create high-quality Agent Skills by guiding you through a structured process:

1. **Skill Designer Agent**: Helps you define the skill's purpose, trigger conditions, and implementation details
2. **Skill Implementer Agent**: Writes the SKILL.md file, scripts, and supporting assets
3. **Skill Evaluator Agent**: Tests the skill, identifies issues, and suggests improvements

## When to use this skill

Use this skill when:
- You want to create a new custom skill
- You need to refine an existing skill
- You want to package a skill for sharing
- You want systematic feedback on skill design

## How to use this skill

1. Start by describing what you want the skill to do
2. Follow the guided workflow through design, implementation, and evaluation
3. Iterate based on feedback from the evaluator agent
4. Package the final skill for use

## Skill Structure

A well-designed skill includes:
- `SKILL.md` - Main skill definition with YAML frontmatter
- `scripts/` - Supporting scripts and tools
- `assets/` - Additional resources (images, templates, etc.)
- `agents/` - Sub-agent definitions (optional)
- `references/` - Documentation and references (optional)

## Frontmatter Requirements

```yaml
---
name: my-skill-name
description: Clear description of what this skill does and when to use it
---
```

## Examples

- Create a skill for testing web applications
- Build a skill for generating documentation
- Design a skill for code review workflows
- Package a skill for sharing with others

## Guidelines

1. **Clear Trigger Description**: Make sure the description clearly states when the skill should be used
2. **Structured Instructions**: Break tasks into clear, actionable steps
3. **Include Examples**: Show concrete usage examples
4. **Test Thoroughly**: Verify the skill works as intended before sharing
5. **Iterate**: Use the evaluator feedback to improve the skill continuously
