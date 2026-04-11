# Anti-Triggers — Overview README

## Overview

This directory contains routing examples where the `subagent-prompt-foundry` skill should **NOT** activate. Anti-trigger examples are as important as trigger examples for routing quality: a skill that activates correctly on valid requests but also activates incorrectly on invalid requests has poor precision and will frustrate users who wanted something done, not a prompt for doing it.

---

## Why Anti-Triggers Matter

The `subagent-prompt-foundry` skill has a specific and narrow activation criterion: the user wants a reusable system prompt for a custom subagent that a parent agent can delegate to. Any request that does not meet this criterion should be routed elsewhere.

In practice, there are two ways routing fails:

1. **False positive on obvious cases**: the skill activates when the request clearly wants direct task execution, generic advice, or a simple result. This is a coarse routing failure — the request uses none of the skill's vocabulary, yet the skill activates anyway.

2. **False positive on deceptive cases**: the skill activates when the request uses the skill's vocabulary ("system prompt," "subagent," "prompt") but fails a routing criterion on closer inspection. This is a precision routing failure — the skill recognized surface vocabulary but did not evaluate the criteria carefully enough.

Both failure types produce the same user experience problem: the user receives a prompt artifact they did not ask for and must re-do their work. But they reveal different problems in the routing system.

---

## Two Categories

### `obvious/` — Clearly Not This Skill

Six cases where the request fails multiple routing criteria simultaneously and uses none of the skill's vocabulary. The routing decision should be immediate and unambiguous.

Common patterns:
- **Direct task execution** — "review my code," "fix this bug," "summarize this PDF," "do the vendor research."
- **Generic advice** — "give me tips on writing prompts."
- **Explicit rejection** — "I only need the result, not a reusable prompt."

These cases test that the skill does not activate by default when it cannot find a strong reason to activate. They establish the routing floor: a skill that misroutes these has a fundamental problem.

See `obvious/cases.md` for the full case table and criterion citations.
See `obvious/README.md` for detailed analysis of each case.

### `deceptive/` — Look Like Triggers but Aren't

Six cases that use skill vocabulary but fail one or more routing criteria on careful reading. These are harder to route correctly because the surface signal is misleading.

Common patterns:
- **One-off prompt** — "Give me a system prompt for X" (says "system prompt" but lacks reuse intent).
- **Meta-agent request** — "Create a meta-agent that writes subagent prompts" (says "subagent prompt" but wants a prompt generator, not a subagent prompt).
- **Agent implementation** — "Help me build an agent that does X" / "Create an agent for my team" (wants code and infrastructure, not a prompt artifact).
- **Vague prompt request** — "Write me a prompt" (no domain, no subagent context, no reuse signal).

These cases test that the skill evaluates all four routing criteria rather than pattern-matching on vocabulary.

See `deceptive/cases.md` for the full case table and criterion citations.
See `deceptive/README.md` for detailed analysis of each case and the ROUTING_MATRIX.md resolution logic.

---

## The Four Routing Criteria (from `assets/routing-checklist.md`)

The skill activates only if **all four** are true:

1. **The output should be a reusable system prompt** — the user wants a prompt artifact that can be applied repeatedly, not a one-time result or one-off prompt.
2. **The prompt defines a custom subagent** — the prompt configures a specialized agent with a specific role, scope, and methodology — not just any prompt.
3. **Direct task execution is not the goal** — the user does not want the task done immediately; they want the infrastructure to delegate it.
4. **A meta-agent prompt is not the goal** — the user does not want a system that generates other prompts; they want one specific subagent prompt.

Any single criterion failure is sufficient to not activate. The anti-trigger examples demonstrate each failure pattern:

| Failure pattern | Category | Examples |
|----------------|----------|----------|
| Criterion 1 (no reuse) | Both | obvious/case 2, 6; deceptive/cases 1, 4, 6 |
| Criterion 2 (no subagent) | Obvious | obvious/cases 1, 2, 3, 4, 5 |
| Criterion 3 (direct execution) | Both | obvious/cases 1, 3, 4, 5; deceptive/cases 3, 5 |
| Criterion 4 (meta-agent) | Deceptive | deceptive/case 2 |

---

## How to Use These Examples

**During skill development**: use these cases to test routing logic changes. If a routing rule change causes any of these cases to activate, the change has introduced a false positive.

**During eval validation**: compare these cases against the eval cases in `evals/evals.json`. Several of the anti-trigger cases are reflected in the eval set (e.g., evals.json id 11 matches obvious/case 5).

**As documentation**: the routing decision column in each `cases.md` file documents the alternative skill or behavior that should handle each request. This is useful for understanding how the `subagent-prompt-foundry` skill fits into the broader skill ecosystem.

---

## Routing Flow for Ambiguous Cases

When a request appears to be in the deceptive anti-trigger zone (uses vocabulary but routing is uncertain):

1. Apply the four routing criteria in order.
2. For criterion 1 (reuse intent): check whether the request contains reuse signals: "reusable," "production-grade," "delegate to," "my parent/main agent," "across projects." If none are present, consult `references/ROUTING_MATRIX.md` before activating.
3. For criterion 3 (direct task execution): ask whether the deliverable is a prompt file or a task result. If the user would be satisfied by receiving a document they can re-use, it may activate. If they expect a completed task or running system, it does not.
4. For criterion 4 (meta-agent): check whether the user wants one specific subagent prompt or a system that can generate many. The latter is a meta-agent request.

If the criteria evaluation is still ambiguous after checking the routing matrix, ask one focused clarifying question rather than defaulting to activation.
