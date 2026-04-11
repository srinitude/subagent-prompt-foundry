# Obvious Anti-Triggers

These cases clearly do not activate the `subagent-prompt-foundry` skill. The user wants something other than a reusable subagent system prompt.

## Routing checklist criteria (from `assets/routing-checklist.md`)

Activate only if **all four** are true:
1. The output should be a reusable system prompt
2. The prompt defines a custom subagent
3. Direct task execution is not the goal
4. A meta-agent prompt is not the goal

Do **not** activate if:
- The user wants prompt advice
- The user wants the final answer directly
- The user wants a prompt-generating meta-agent

---

## Cases

| # | Invocation | Why it should NOT activate | Routing decision |
|---|------------|---------------------------|------------------|
| 1 | "Just review my code and tell me what's wrong." | Direct task execution — the user wants the code reviewed, not a prompt for a code reviewer. Fails criterion 1 (no reusable prompt requested) and criterion 3 (direct task execution IS the goal). | DEFER → direct-task-review skill |
| 2 | "Give me some tips on writing better prompts." | Generic advice request — the user wants guidance, not a prompt artifact. Fails criterion 1 (no reusable system prompt requested) and criterion 2 (no custom subagent defined). The anti-trigger phrase "give me prompt tips" from `routing-checklist.md` matches exactly. | DEFER → prompt-advice skill |
| 3 | "Summarize this PDF for me." | Direct task execution — the user wants a PDF summarized immediately. Fails criteria 1, 2, and 3. There is no subagent context and no prompt artifact requested. | DEFER → direct-task-summarization skill |
| 4 | "Fix this bug in my authentication module." | Direct task execution — the user wants the bug fixed, not a prompt for a bug-fixing subagent. Fails criteria 1, 2, and 3. No prompt artifact is requested; the user wants a result. | DEFER → direct-task-debugging skill |
| 5 | "Just do the vendor research for me." | Direct task execution — the user wants the research completed immediately. The anti-trigger phrase "just do the task" from `routing-checklist.md` and evals.json (eval id 11: "Just do the vendor research for me", `should_activate: false`) matches exactly. Fails criteria 1, 2, and 3. | DEFER → direct-research skill |
| 6 | "I only need the result, not a reusable prompt." | Explicitly rejects the skill's deliverable — the user has stated they do not want a prompt artifact. The anti-trigger phrase "I only need the result" from `SKILL.md` matches exactly. Fails criteria 1, 2, and 3. | DEFER → direct-task skill matching the requested domain |

---

## Criterion citations

Each rejection maps to a specific line in `assets/routing-checklist.md`:

- Cases 1, 3, 4, 5: **"direct task execution is not the goal"** — all four fail this criterion because the user explicitly wants the task done.
- Case 2: **"the output should be a reusable system prompt"** and the matching `SKILL.md` anti-trigger phrase **"give me prompt tips"**.
- Case 6: **"the output should be a reusable system prompt"** — the user explicitly stated they do not want a prompt artifact; the `SKILL.md` anti-trigger phrase **"I only need the result"** is a direct match.
