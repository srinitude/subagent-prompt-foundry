# deceptive anti-triggers — Example README

## Overview

This directory contains six cases that SHOULD NOT activate the `subagent-prompt-foundry` skill even though they superficially resemble trigger phrases. These are "deceptive" anti-triggers because they use the skill's vocabulary — "system prompt," "subagent," "agent," "prompt," "build an agent" — but fail on one or more routing criteria when evaluated carefully. They represent the harder routing challenge: resolving ambiguity when surface signals are misleading.

---

## What Makes an Anti-Trigger "Deceptive"

A deceptive anti-trigger is a case where:

1. **The request uses skill vocabulary** — words like "system prompt," "subagent," "agent," or "prompt" that appear in the skill's trigger phrases and activation criteria. A naive keyword-matching router would activate on these.
2. **Only one criterion fails on close inspection** — unlike obvious anti-triggers, deceptive cases often satisfy two or three of the four criteria. The failure is subtle and requires reading the request carefully rather than pattern-matching.
3. **The routing failure mode is specific** — each deceptive case fails on a different criterion, making them collectively useful for testing whether a router evaluates all four criteria or shortcuts to keyword matching.

The six deceptive cases in this directory fail on four distinct criteria:

| Criterion that fails | Cases |
|----------------------|-------|
| Reuse intent absent (criterion 1) | 1, 4, 5, 6 |
| Meta-agent is the goal (criterion 4) | 2 |
| Direct task execution is the goal (criterion 3) | 3, 5 |

---

## Case Analysis

### Case 1: "Give me a system prompt for a code auditor."

**Why it looks like a trigger:** "System prompt" is the skill's primary output type and a named trigger phrase.

**Why it isn't:** The request is a one-off with no mention of reuse, parent delegation, subagent isolation, or production-grade structure. It could be satisfied by any prompt skill — not specifically by the subagent-prompt-foundry skill, which specializes in reusable, delegation-ready prompts with full parent↔subagent protocol.

`references/ROUTING_MATRIX.md` addresses this case directly: "User wants a one-off prompt for a single agent and reuse is not important → Usually no → Prefer a narrower single-agent prompt skill."

**Routing decision:** DEFER to a narrower single-agent prompt skill. If the user had said "Give me a reusable system prompt for a code auditor that my main agent can delegate to," that would activate the skill. Without the reuse and delegation signals, the request does not clear criterion 1.

**Key lesson:** The word "system prompt" is a necessary but not sufficient condition for activation. Reuse intent must be present or inferrable.

### Case 2: "Create a meta-agent that can write any kind of subagent prompt on the fly."

**Why it looks like a trigger:** "Subagent prompt" is the skill's output type; "create" echoes trigger phrases; "any kind" implies generality.

**Why it isn't:** The user explicitly wants a meta-agent — an agent that generates prompts for other agents, not a single subagent prompt for a specific domain task. The `subagent-prompt-foundry` skill creates individual, domain-specific subagent prompts; it does not create meta-agents.

SKILL.md explicitly lists this as a do-not-use case: "the user wants a meta-agent that writes prompts for other agents." The anti-trigger phrase "create a meta-agent that writes prompts" is listed verbatim in SKILL.md's anti-trigger phrases.

**Routing decision:** DEFER to a meta-agent prompt skill. Criterion 4 ("a meta-agent prompt is not the goal") fails clearly.

**Key lesson:** The presence of "subagent prompt" in the request does not guarantee the user wants a subagent prompt as the deliverable. They may want a system that generates subagent prompts — a fundamentally different thing.

### Case 3: "Help me build an agent that reviews pull requests."

**Why it looks like a trigger:** "Build an agent" echoes trigger phrases; the task (PR review) is a plausible subagent domain.

**Why it isn't:** "Build" signals implementation — the user wants a working, deployed agent, not a system prompt to configure one. Building an agent involves code, infrastructure, testing, and deployment; authoring a system prompt is one input to that process, not the full output.

**Routing decision:** DEFER to a direct implementation / coding skill. Criterion 3 ("direct task execution is not the goal") fails — the goal is to build a working agent, not to produce a prompt artifact.

**Key lesson:** "Build an agent" and "create a subagent prompt for an agent" are categorically different requests. The former wants the agent itself; the latter wants the configuration document for the agent. The `subagent-prompt-foundry` skill produces the configuration document only.

### Case 4: "I want a prompt that reviews my database schema."

**Why it looks like a trigger:** Mentions "prompt" as the desired output.

**Why it isn't:** This is a one-off, narrow request with no subagent context, no parent delegation, and no reuse signal. The word "my database schema" suggests a single use case, not a general pattern. There is no mention of a parent agent, no isolation requirement, and no production-grade structure needed.

`references/ROUTING_MATRIX.md`: "User wants a one-off prompt for a single agent and reuse is not important → Usually no." Criteria 1 and 2 both fail: the requested output is not clearly a reusable system prompt, and no custom subagent (with isolation and delegation) is being defined.

**Routing decision:** DEFER to a narrower single-purpose prompt skill.

**Key lesson:** The word "prompt" in the request is surface-level vocabulary overlap, not a routing signal. The routing criteria require a reusable system prompt for a custom subagent — both "reusable" and "custom subagent" are required, not just "prompt."

### Case 5: "Create an agent for my team that handles onboarding."

**Why it looks like a trigger:** "Create an agent" echoes trigger phrases; the use case (onboarding) is plausible for a specialized subagent.

**Why it isn't:** "For my team that handles onboarding" signals a full-stack agent product: deployed, operational, possibly integrated with HR systems, accessible to team members. This is not a prompt authorship task — it is an agent engineering and deployment task. The user wants the agent to exist and work, not a system prompt file.

Criteria 1 and 3 both fail: the deliverable is a working deployed agent, not a prompt artifact (criterion 1); and the execution of the agent's onboarding function is the goal (criterion 3).

**Routing decision:** DEFER to an agent-building / implementation skill.

**Key lesson:** "For my team" is a contextual signal that distinguishes an agent product (ongoing operational use by multiple users) from a subagent prompt (a configuration file used by a parent agent). The former needs engineering; the latter needs prompt authorship.

### Case 6: "Write me a prompt."

**Why it looks like a trigger:** "Prompt" is the skill's output type.

**Why it isn't:** The request is too vague to satisfy any routing criterion. No domain is specified, no subagent context is implied, no parent delegation is mentioned, no reuse signal is present. This is an ambiguous general request that could be handled by any prompt skill.

SKILL.md requires "a prompt that should be generalized from an example" or "a structured prompt with explicit methodology, constraints, or output rules" — none of these signals are present in "write me a prompt."

**Routing decision:** Ask for more context before routing anywhere. This is the only case in both anti-trigger directories where the correct response is a clarifying question rather than a routing decision.

**Key lesson:** Ambiguity is a valid routing state. Rather than guessing intent or applying the nearest skill by surface matching, the correct behavior is to ask one focused clarifying question: "What should the prompt help with?" The answer determines whether this belongs to `subagent-prompt-foundry` or some other skill.

---

## Why Deceptive Cases Are Harder to Route Correctly

Obvious anti-triggers fail routing because they do not use the skill's vocabulary. A keyword-matching router correctly declines them.

Deceptive anti-triggers fail routing because a keyword-matching router may incorrectly activate on them. The criterion evaluation requires reading the request carefully:
- "System prompt" appears → check: is reuse intended?
- "Subagent prompt" appears → check: is the deliverable a single prompt, or a meta-agent that generates prompts?
- "Build an agent" appears → check: is the deliverable a prompt artifact, or an implemented system?
- "Prompt" appears → check: is there a custom subagent context, or just a general prompting request?

Each check requires evaluating the routing criteria against the request semantics, not just surface vocabulary.

---

## How the Routing Matrix Resolves Ambiguity

When deceptive cases appear, the correct resolution path is:
1. Apply the routing-checklist.md criteria in order.
2. If any criterion fails, note which one and why.
3. If the failure is "reuse intent absent" (criteria 1), check `references/ROUTING_MATRIX.md` for the "one-off prompt, reuse not important" row.
4. If the failure is "meta-agent is the goal" (criterion 4), note that SKILL.md explicitly lists this as a do-not-use case.
5. If the failure is "direct task execution" (criterion 3), identify what the user actually wants built or done, and route to the appropriate implementation or execution skill.

The routing matrix is the tie-breaker for borderline cases. The checklist is the primary gate; the matrix provides the resolution logic for the cases the checklist does not fully specify.

---

## Criterion Citations

Each deceptive case fails on a specific criterion from `assets/routing-checklist.md` and `references/ROUTING_MATRIX.md`:

| Case | Criterion violated | Resolution source |
|------|-------------------|-------------------|
| 1 | Reuse intent absent → criterion 1 | ROUTING_MATRIX.md: "one-off prompt, reuse not important" |
| 2 | Meta-agent is the goal → criterion 4 | SKILL.md anti-trigger phrase (verbatim match) |
| 3 | Direct task execution → criterion 3 | SKILL.md: "user wants direct task execution" |
| 4 | Reuse absent, no subagent context → criteria 1 and 2 | ROUTING_MATRIX.md: "one-off prompt, reuse not important" |
| 5 | Deliverable is an agent product, execution is the goal → criteria 1 and 3 | SKILL.md: "user wants direct task execution" |
| 6 | No domain, no subagent context, no reuse signal → criteria 1 and 2 | Ask for more context first |
