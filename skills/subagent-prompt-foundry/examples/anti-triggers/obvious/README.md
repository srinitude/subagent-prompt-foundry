# obvious anti-triggers — Example README

## Overview

This directory contains six cases that clearly should NOT activate the `subagent-prompt-foundry` skill. These are "obvious" anti-triggers because they fail multiple routing criteria simultaneously and share a common characteristic: the user wants something done, not a prompt for doing it. They represent the baseline of routing quality — any skill with adequate routing should handle these without hesitation.

---

## What Makes an Anti-Trigger "Obvious"

An obvious anti-trigger is a case where:

1. **Multiple routing criteria fail simultaneously** — not just one criterion, but two or three at once. This means there is no ambiguity to resolve; the routing decision is clear from the first sentence of the request.
2. **No skill vocabulary is used** — the user does not mention "system prompt," "subagent," "agent," "reusable," "delegate," or "production-grade." The request is unambiguously about getting a task done.
3. **The request pattern is familiar** — direct task execution requests ("review my code," "fix this bug," "summarize this PDF") are common baseline requests that agents encounter constantly. Misrouting these to a prompt-generation skill would be a systematic failure.

The cases in this directory collectively cover three failure types:

- **Direct task execution** (cases 1, 3, 4, 5): the user explicitly wants a task completed. The output should be the task result, not a prompt for a subagent that could complete the task.
- **Generic advice request** (case 2): the user wants guidance on prompting, not a prompt artifact. This is easy to route correctly because "give me prompt tips" is an explicit anti-trigger phrase in SKILL.md.
- **Explicit rejection of the skill's deliverable** (case 6): the user states they do not want a reusable prompt. This is the clearest possible anti-trigger — the user has named the skill's output type and rejected it.

---

## Case Analysis

### Case 1: "Just review my code and tell me what's wrong."

The word "just" is an anti-trigger signal. It signals impatience with overhead — the user wants a direct answer, not a process. "Tell me what's wrong" is a direct deliverable request: the output is a code review, not a prompt for a code reviewer.

Two criteria fail simultaneously:
- Criterion 1 fails: the output should be a code review, not a reusable system prompt.
- Criterion 3 fails: direct task execution (reviewing the code) is explicitly the goal.

The agent should route to a code review skill or perform the review directly. Creating a code reviewer subagent prompt would be a category error — the user would receive a prompt they did not ask for and would need to re-invoke a subagent with it before getting their actual code review.

### Case 2: "Give me some tips on writing better prompts."

This is the only case where the request is adjacent to the skill's domain (prompt engineering) without being the skill's use case. The user wants advice, not an artifact. "Tips" and "advice" are fundamentally different from "a prompt."

Two criteria fail:
- Criterion 1 fails: the output should be prompt-writing advice, not a reusable system prompt.
- Criterion 2 fails: no custom subagent is being defined; no domain, no role, no scope is implied.

This case is in the obvious category (not the deceptive category) because "give me prompt tips" is an explicit anti-trigger phrase listed in SKILL.md's anti-trigger phrases section. Any routing system that reads the skill specification will recognize this pattern immediately.

### Case 3: "Summarize this PDF for me."

Pure direct task execution. The deliverable is a PDF summary, not a prompt. No subagent context is implied, no reuse is requested, no delegation is named.

Three criteria fail simultaneously (1, 2, 3) — the clearest failure profile in the set. The agent should route to a document summarization skill or perform the summarization directly.

### Case 4: "Fix this bug in my authentication module."

Direct task execution: the deliverable is a fixed authentication module. Debugging and fixing is not prompt authorship.

Three criteria fail (1, 2, 3). No prompt artifact is requested; the user wants a working result. The agent should route to a debugging or code-fixing skill.

### Case 5: "Just do the vendor research for me."

The word "just" again, combined with "for me" — a direct request for completed work. The deliverable is vendor research results, not a vendor research subagent prompt.

Three criteria fail (1, 2, 3). This case is explicitly documented in evals.json (eval id 11: "Just do the vendor research for me", `should_activate: false`) — it is a named test case for the skill's routing evaluation.

### Case 6: "I only need the result, not a reusable prompt."

The most explicit rejection possible: the user has named the skill's deliverable ("a reusable prompt") and rejected it. There is no routing ambiguity when the user states explicitly what they do not want.

Three criteria fail (1, 2, 3). "I only need the result" is an explicit anti-trigger phrase in SKILL.md. The agent should route to whichever direct-task skill matches the domain of the "result" the user wants.

---

## How Agents Should Handle Obvious Anti-Triggers

The correct behavior is **immediate, unambiguous deferral**:

1. Recognize that the request fails routing criteria (no clarifying questions needed — the failure is clear).
2. Identify the appropriate alternative skill or behavior (code review, summarization, debugging, direct task execution, advice).
3. Route to that alternative and begin executing.

There is no need to explain the routing decision to the user unless they ask. The user asked for code review; the agent performs code review. Announcing "I'm routing this to a code review skill rather than the subagent-prompt-foundry skill" adds no value.

Importantly, obvious anti-triggers should not trigger clarifying questions. A question like "Do you want me to review your code, or would you like a prompt for a code review subagent?" would be bizarre in response to "Just review my code and tell me what's wrong." The user's intent is clear.

---

## Why Both Categories (Obvious and Deceptive) Matter

Obvious anti-triggers test the floor of routing quality: if a skill cannot correctly decline these, it has a fundamental routing problem. Correctly handling obvious cases is necessary but not sufficient for high routing quality.

The more challenging test is the deceptive category — cases that use skill vocabulary but fail on closer inspection. Those cases require actually evaluating whether the routing criteria are met, not just pattern-matching on the absence of trigger phrases.

Together, the two categories form a routing quality spectrum:
- Obvious anti-triggers: test that the skill does not activate when clearly inappropriate.
- Deceptive anti-triggers: test that the skill correctly resolves ambiguity in borderline cases.

A skill that handles obvious anti-triggers but fails on deceptive ones has coarse routing. A skill that handles both has precise routing.

---

## Criterion Citations

The cases map to these specific lines in `assets/routing-checklist.md`:

| Case | Criterion violated | Checklist line |
|------|--------------------|----------------|
| 1 | Direct task execution is the goal | "direct task execution is not the goal" |
| 2 | No reusable prompt, no subagent defined | "the output should be a reusable system prompt" + "the prompt defines a custom subagent" |
| 3 | Direct task execution, no subagent context | "direct task execution is not the goal" + "the output should be a reusable system prompt" |
| 4 | Direct task execution, no prompt artifact | "direct task execution is not the goal" + "the output should be a reusable system prompt" |
| 5 | Direct task execution | "direct task execution is not the goal" (matches evals.json id 11) |
| 6 | User rejected the prompt artifact | "the output should be a reusable system prompt" (user explicitly declined) |

The anti-trigger phrases for cases 2 and 6 are also listed verbatim in SKILL.md: "give me prompt tips" and "I only need the result."
