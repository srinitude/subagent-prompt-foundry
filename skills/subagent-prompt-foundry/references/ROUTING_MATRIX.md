# Routing Matrix

Use this file when activation is ambiguous or overlaps with other skills.

| Situation | Activate this skill? | Why |
|---|---|---|
| User wants a reusable system prompt for a custom subagent | Yes | This is the exact use case |
| User wants a one-off prompt for a single agent and reuse is not important | Usually no | Prefer a narrower single-agent prompt skill |
| User wants a meta-agent that writes prompts for other agents | No | Prefer a dedicated meta-agent prompt skill |
| User wants generic advice about prompting | No | Prefer a prompt-advice skill |
| User wants the task done directly | No | Prefer a direct task-execution skill |
| User wants a parent agent to delegate to an isolated subagent | Yes | This skill defines the delegation contract |

## Trigger examples
- "Create a custom subagent"
- "Make this prompt reusable"
- "Design a production-grade reviewer prompt"
- "I need a subagent my main agent can delegate to"

## Anti-trigger examples
- "Just do the task"
- "Give me prompt tips"
- "Create a meta-agent that writes prompts"
- "Answer directly"
