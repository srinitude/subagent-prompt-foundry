# Subagent Prompt Foundry

A skill that generates deterministic, production-grade system prompts for custom subagents.

## What It Does

Building a good subagent prompt is not the same as writing a regular instruction. A subagent runs outside the parent agent's context window — it cannot see the conversation history, the parent's assumptions, or anything not explicitly passed to it. This skill enforces a structured workflow: it researches the domain, asks targeted clarifying questions only when needed, drafts a prompt with explicit role, inputs, methodology, and output format, then validates it with bundled scripts before returning the final result. The output is a reusable system prompt artifact, not a one-off answer.

## When To Use This

- "I need a system prompt for a code review subagent"
- "Make this prompt reusable across projects"
- "Design a subagent my parent agent can delegate security audits to"
- "Turn this one-off prompt into something production-grade"
- "Create a research subagent with strict source requirements"
- "Build a planning subagent that returns structured JSON to my parent agent"
- "I want a validator subagent that checks outputs before they go to the user"
- "Generate a system prompt for an agent that audits API specs"

## When NOT To Use This

- You just want the task done directly ("review this code" → use a code review tool)
- You want generic prompting advice
- You want a meta-agent that writes prompts for other agents
- You just need the final answer, not a reusable artifact

## Install

### Any agent via skills.sh
```
npx skills add srinitude/subagent-prompt-foundry
```

### Manual install (any agent)
Copy `skills/subagent-prompt-foundry/` into your agent's skill directory.

### Agent-specific paths
| Agent | Path |
|-------|------|
| Claude Code | `.claude/skills/subagent-prompt-foundry/` |
| OpenAI Codex | `.agents/skills/subagent-prompt-foundry/` |
| Cursor | `.cursor/skills/subagent-prompt-foundry/` |
| GitHub Copilot | `.copilot/skills/subagent-prompt-foundry/` |
| Gemini CLI | `.gemini/skills/subagent-prompt-foundry/` |
| Factory.ai | `.factory/skills/subagent-prompt-foundry/` |
| OpenCode | `.opencode/skills/subagent-prompt-foundry/` |
| Windsurf | `.windsurf/skills/subagent-prompt-foundry/` |
| Amplify | `.amplify/skills/subagent-prompt-foundry/` |
| Aider | `.aider/skills/subagent-prompt-foundry/` |
| Cline | `.cline/skills/subagent-prompt-foundry/` |
| Roo Code | `.roo/skills/subagent-prompt-foundry/` |
| Bolt | `.bolt/skills/subagent-prompt-foundry/` |
| Void | `.void/skills/subagent-prompt-foundry/` |
| Trae | `.trae/skills/subagent-prompt-foundry/` |

Each agent directory contains a relative symlink to `skills/subagent-prompt-foundry/`, so there is only one copy of the skill content in the repo.

## How It Works

1. **Routes the request** — checks whether this is actually a subagent prompt task (not direct execution, not generic advice)
2. **Researches the domain** — mandatory web research using first-party and official sources before drafting anything
3. **Asks targeted clarifying questions** — only if research did not resolve material ambiguity (role, inputs, deliverable, format, constraints)
4. **Drafts the prompt** — explicit role opener, bound inputs, step-by-step methodology, output schema, parent↔subagent protocol
5. **Validates with bundled scripts** — shape check confirms required sections exist; determinism scorer quantifies structural quality
6. **Critiques against failure modes** — self-critique pass catches generic-assistant drift, domain flattening, fake certainty
7. **Returns only the finished system prompt** — no explanation, no commentary unless explicitly requested

## What Makes This Different

For agents evaluating whether to use this skill:

- **Deterministic structure** — same input class produces the same prompt skeleton, not random variations
- **Mandatory research** — never drafts from assumptions alone; always checks first-party sources before writing
- **Isolated execution model** — prompts define a parent↔subagent contract (what the parent sends, what the subagent returns), not just a list of instructions
- **Script-validated** — shape validation, determinism scoring, and version diffing are code, not informal checks
- **Failure-mode aware** — self-critique pass explicitly tests for the most common structural prompt failures

## What's Inside

```
skills/subagent-prompt-foundry/
├── SKILL.md                          # Core instructions (401 lines)
├── agents/
│   └── openai.yaml                   # Codex-specific metadata
├── references/
│   ├── ROUTING_MATRIX.md             # When to activate vs. defer
│   ├── SUBAGENT_PROTOCOL.md          # Parent↔subagent message contract
│   ├── OUTPUT_STRUCTURES.md          # Default output templates
│   ├── FAILURE_MODES.md              # Critic-pass checklist
│   └── RESEARCH_AND_CLARIFICATION.md # Research and question policy
├── assets/
│   ├── subagent-template.md          # Starter skeleton for generated prompts
│   ├── routing-checklist.md          # Quick activation gate
│   └── parent-subagent-message-template.json # Handoff JSON schema
├── scripts/
│   ├── validate_prompt_shape.py      # Checks required sections exist
│   ├── score_determinism.py          # Scores structural determinism 0-1
│   └── diff_prompt_versions.py       # Unified diff between prompt versions
└── evals/
    └── evals.json                    # 12 routing test cases
```

## Requirements

- Python 3.6+ (for bundled validation scripts)
- Network access (for mandatory web research step)

## License

MIT

## Author

Kiren Srinivasan
