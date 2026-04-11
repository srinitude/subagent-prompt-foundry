# Deceptive Anti-Triggers

These cases use language that superficially resembles trigger phrases but do not actually warrant activating `subagent-prompt-foundry`. Each case mimics the skill's surface triggers while failing one or more of the routing-checklist.md criteria.

## Routing checklist criteria (from `assets/routing-checklist.md`)

Activate only if **all four** are true:
1. The output should be a reusable system prompt
2. The prompt defines a custom subagent
3. Direct task execution is not the goal
4. A meta-agent prompt is not the goal

---

## Cases

| # | Invocation | Why it LOOKS like a trigger | Why it actually ISN'T | Routing decision |
|---|------------|----------------------------|-----------------------|------------------|
| 1 | "Give me a system prompt for a code auditor." | Mentions "system prompt" — a primary trigger phrase. | The request is a one-off with no mention of reuse, subagent isolation, parent delegation, or production-grade structure. Per `references/ROUTING_MATRIX.md`: "User wants a one-off prompt for a single agent and reuse is not important → Usually no → Prefer a narrower single-agent prompt skill." Fails criterion 1 (reuse is absent). | DEFER → narrower single-agent prompt skill |
| 2 | "Create a meta-agent that can write any kind of subagent prompt on the fly." | Mentions "subagent prompt" — directly echoes skill vocabulary. | The user wants a META-agent that generates prompts for other agents, not a single subagent prompt. `SKILL.md` explicitly lists this as a do-not-use case: "the user wants a meta-agent that writes prompts for other agents." The anti-trigger phrase "create a meta-agent that writes prompts" is a verbatim match. Fails criterion 4. | DEFER → meta-agent-prompt skill |
| 3 | "Help me build an agent that reviews pull requests." | Mentions "build an agent" — implies agent creation. | The user wants the full agent built and/or coded, not just a system prompt to configure it. "Build" signals implementation, not prompt authorship. `SKILL.md` anti-trigger: "user wants direct task execution." Fails criterion 3 (direct task execution IS the goal — the goal is a working agent, not a prompt artifact). | DEFER → direct implementation / coding skill |
| 4 | "I want a prompt that reviews my database schema." | Mentions "prompt" — overlaps with skill output type. | This is a one-off, narrow prompt request with no subagent context, no isolation requirement, and no parent delegation. `references/ROUTING_MATRIX.md`: "User wants a one-off prompt for a single agent and reuse is not important → Usually no." Reuse and subagent isolation are absent. Fails criteria 1 and 2. | DEFER → narrower single-purpose prompt skill |
| 5 | "Create an agent for my team that handles onboarding." | Mentions "create an agent" — echoes the skill's primary use case. | The user wants a complete agent built, deployed, and operational — not just a system prompt. "For my team" and "handles onboarding" signal a full-stack agent product, not a prompt artifact. Fails criterion 3 (execution of the agent itself is the goal) and criterion 1 (the deliverable is an agent, not a prompt). | DEFER → agent-building / implementation skill |
| 6 | "Write me a prompt." | Mentions "prompt" — the skill's core output. | Too vague to qualify: no domain specified, no subagent isolation context, no parent delegation mentioned, no reuse intent expressed. This is an ambiguous general request, not a subagent prompt request. `SKILL.md` requires "a prompt that should be generalized from an example" or "a structured prompt with explicit methodology, constraints, or output rules" — none of those signals are present. Before routing to any skill, ask for context. Fails criteria 1 and 2. | DEFER → ask for more context first |

---

## Criterion citations

Each deceptive case fails on a specific differentiating criterion from `assets/routing-checklist.md`:

- Case 1: Fails **"the output should be a reusable system prompt"** — one-off nature means reusability is absent; `ROUTING_MATRIX.md` "one-off prompt, reuse not important" rule applies.
- Case 2: Fails **"a meta-agent prompt is not the goal"** — the user explicitly wants a meta-agent; `SKILL.md` anti-trigger phrase matches verbatim.
- Case 3: Fails **"direct task execution is not the goal"** — building a working agent is task execution, not prompt authorship.
- Case 4: Fails **"the output should be a reusable system prompt"** and **"the prompt defines a custom subagent"** — one-off, no isolation, no delegation context.
- Case 5: Fails **"the output should be a reusable system prompt"** and **"direct task execution is not the goal"** — the full agent build is the goal, not the system prompt alone.
- Case 6: Fails **"the output should be a reusable system prompt"** and **"the prompt defines a custom subagent"** — no domain, no subagent context, no reuse signal present.
