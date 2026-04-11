# Routing Checklist

Use this checklist before activation.

Activate only if all are true:
- the output should be a reusable system prompt
- the prompt defines a custom subagent
- direct task execution is not the goal
- a meta-agent prompt is not the goal

Do not activate if:
- the user wants prompt advice
- the user wants the final answer directly
- the user wants a prompt-generating meta-agent

> **Reuse intent note:** Reuse intent is signaled by words like 'reusable', 'production-grade', 'delegate to', 'my parent/main agent', or 'across projects'. If none of these signals are present, consult `references/ROUTING_MATRIX.md` before activating.
