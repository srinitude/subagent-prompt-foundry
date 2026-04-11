# Examples

Test outputs from invoking `/subagent-prompt-foundry` across diverse domains.

Each trigger example follows the 19-step mandatory workflow from `SKILL.md` exactly: routing check → research → role/scope definition → input binding → methodology → evidence standards → protocol definition → output format → constraints → drafting → failure-mode critique → validation → determinism scoring.

---

## Triggers (skill activates and produces a prompt)

| Example | Domain | Determinism Score | Validation |
|---------|--------|-------------------|------------|
| [dependency-scanner](triggers/dependency-scanner/) | DevSecOps — CI pipeline vulnerability scanning using NVD, CVE, CVSS, OSV | 0.950 | ✓ PASS |
| [market-research](triggers/market-research/) | Business strategy — competitive market entry evaluation using Porter's Five Forces, TAM/SAM/SOM, Gartner | 0.925 | ✓ PASS |
| [dnd-dungeon-master](triggers/dnd-dungeon-master/) | Gaming/creative — D&D 5e encounter tables, loot drops, and NPC dialogue trees | 0.920 | ✓ PASS |
| [sample-clearance](triggers/sample-clearance/) | Music IP/legal — master vs. composition rights, HFA, MLC, WhoSampled, interpolation vs. direct sample | 0.945 | ✓ PASS |
| [mix-master-critique](triggers/mix-master-critique/) | Audio engineering — LUFS, K-system, Fletcher-Munson, EQ/compression with specific Hz/dB values | 0.958 | ✓ PASS |
| [sourdough-diagnosis](triggers/sourdough-diagnosis/) | Food science + vision — crumb analysis, proofing failure taxonomy, professional bread evaluation rubric | 0.923 | ✓ PASS |

All determinism scores exceed the 0.7 minimum threshold defined in `SKILL.md`.

### Per-example file layout

Each trigger directory contains:

| File | Contents |
|------|----------|
| `invocation.md` | The exact `/subagent-prompt-foundry` command that triggered this example, routing decision, and research sources |
| `prompt.md` | The final generated system prompt (the primary deliverable) |
| `metrics.json` | Four-dimension determinism input scores (structure_stability, constraint_preservation, research_completeness, protocol_clarity) |
| `validation.json` | Output from `validate_prompt_shape.py` confirming all required sections present, plus the determinism score |

---

## Anti-triggers

### Obvious (clearly not this skill)

Cases where the request clearly does not match the skill's activation criteria. Users want direct task execution, generic advice, or a result — not a reusable subagent prompt.

See [obvious/cases.md](anti-triggers/obvious/cases.md)

**Summary of cases:**

| # | Request type | Criterion violated |
|---|-------------|--------------------|
| 1 | "Review my code and tell me what's wrong" | Direct task execution is the goal |
| 2 | "Give me tips on writing better prompts" | Output is advice, not a reusable system prompt |
| 3 | "Summarize this PDF for me" | Direct task execution; no subagent context |
| 4 | "Fix this bug in my authentication module" | Direct task execution |
| 5 | "Just do the vendor research for me" | Direct task execution (matches evals.json id 11) |
| 6 | "I only need the result, not a reusable prompt" | User explicitly rejects the prompt artifact |

### Deceptive (look like triggers but aren't)

Cases where the request uses skill vocabulary ("system prompt," "subagent," "agent," "prompt") but fails one or more of the four routing-checklist.md criteria on closer inspection.

See [deceptive/cases.md](anti-triggers/deceptive/cases.md)

**Summary of cases:**

| # | Request type | Why it looks like a trigger | Why it isn't |
|---|-------------|----------------------------|--------------|
| 1 | "Give me a system prompt for a code auditor" | Says "system prompt" | One-off, no reuse or delegation signal |
| 2 | "Create a meta-agent that writes subagent prompts" | Says "subagent prompt" | Wants a meta-agent, not a single subagent prompt |
| 3 | "Help me build an agent that reviews pull requests" | Says "build an agent" | Wants the agent built/coded, not a system prompt |
| 4 | "I want a prompt that reviews my database schema" | Says "prompt" | One-off, no subagent context or parent delegation |
| 5 | "Create an agent for my team that handles onboarding" | Says "create an agent" | Wants a full deployed agent product, not just a prompt |
| 6 | "Write me a prompt" | Says "prompt" | Too vague; no domain, no subagent context, ask for more |

---

## Scripts used

All scripts were run from the skill directory root (`skills/subagent-prompt-foundry/`):

```bash
python3 scripts/validate_prompt_shape.py examples/triggers/<name>/prompt.md
python3 scripts/score_determinism.py examples/triggers/<name>/metrics.json
```

Required sections checked by `validate_prompt_shape.py`: `Role`, `Scope`, `Inputs`, `Task`, `Methodology`, `Output`

---

## Issues

See [ISSUES.md](ISSUES.md) for any ambiguities, inconsistencies, or broken behaviors observed during this test suite run.
