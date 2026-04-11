# Triggers — Overview README

## Overview

This directory contains six examples where the `subagent-prompt-foundry` skill correctly activates and produces a complete system prompt. Each example follows the skill's 19-step mandatory workflow exactly, covers a distinct domain, and passes both structural validation and the determinism scoring threshold (minimum 0.7). Together they demonstrate the skill's range across domains while sharing a common structural spine.

---

## What All Trigger Examples Share

Every trigger example in this directory satisfies the same four routing criteria from `assets/routing-checklist.md`:

1. The output is a reusable system prompt (not a one-time result).
2. The prompt defines a custom subagent (a specialized, isolated agent with a defined role, scope, and methodology).
3. Direct task execution is not the goal (the user wants the infrastructure to delegate the task, not the task completed now).
4. A meta-agent prompt is not the goal (the user wants one specific subagent prompt, not a prompt generator).

Beyond routing, all six examples share these structural properties:

### Common Prompt Architecture

Every generated prompt includes the six required sections validated by `scripts/validate_prompt_shape.py`:

| Section | What it specifies |
|---------|-------------------|
| Role | The subagent's identity and immediate context. Uses an active verb opener (auditing, researching, diagnosing, generating, critiquing). Explicitly states isolation from the parent's context window. |
| Scope | What the subagent analyzes and what it does not. Prevents scope creep and defines the boundary between the subagent's responsibility and the parent's responsibility. |
| Inputs | The exact JSON handoff schema from the parent agent. Binds the subagent to explicit artifacts and sources only. |
| Task | The specific deliverables requested. For multi-output prompts, each deliverable is separately labeled. |
| Methodology | Ordered, numbered steps with explicit actions (parse, verify, classify, synthesize, cite). No filler verbs ("think carefully," "consider"). |
| Output | The exact return schema (JSON, Markdown, or both). Field-level specification with types and examples. |

Beyond these required sections, all six prompts include:
- An **Evidence Standards** section requiring source citations and prohibiting fabrication or speculation.
- A **Parent↔Subagent Protocol** section with a complete JSON schema for the subagent's return message.
- A **Constraints** section with explicit prohibitions against generic assistant behavior, vague language, and domain-specific failure modes.

### Common Workflow Steps

All six examples followed the 19-step mandatory workflow:

1. Route correctly (all activated via distinct invocation patterns)
2. Check specification sufficiency
3. Perform web research (all sourced from authoritative first-party or official sources)
4. Ask clarifying questions (none needed — domain research resolved ambiguity in all cases)
5–13. Define role, scope, inputs, task, methodology, evidence standards, protocol, output format, constraints
14. Draft the prompt
15. Validate shape with `scripts/validate_prompt_shape.py`
16. Critique using `references/FAILURE_MODES.md`
17. Diff (skipped for all six — no prior drafts existed; this is documented in ISSUES.md as ISSUE-003)
18. Score determinism with `scripts/score_determinism.py`
19. Return the final system prompt

### Determinism Scores

All six examples exceed the 0.7 minimum threshold:

| Example | Score | Ranking |
|---------|-------|---------|
| mix-master-critique | 0.958 | 1st — highest precision from quantitative audio standards |
| dependency-scanner | 0.950 | 2nd — binary CVE lookup with fully specified JSON schema |
| sample-clearance | 0.945 | 3rd — dual-license methodology with strict source requirements |
| market-research | 0.925 | 4th — analytical frameworks with inherent judgment gaps |
| sourdough-diagnosis | 0.923 | 5th — visual inference with failure taxonomy |
| dnd-dungeon-master | 0.920 | 6th — creative output with constrained mechanical calculation |

The score distribution is not random — it correlates with the inherent determinism of each domain. Domains with quantitative standards (audio engineering, vulnerability scoring) score higher than domains with interpretive judgment (visual diagnosis, market analysis) or creative latitude (content generation).

---

## What Makes Each Example Unique

### dependency-scanner — DevSecOps

**Unique feature: binary pipeline gate.** The subagent's output includes a `pipeline_signal: "PASS" | "FAIL"` field that a CI system can parse with a single field read. This is the only example with a machine-readable exit signal designed for automated pipeline integration. The prompt enforces that every response must include this field, even when no vulnerabilities are found.

**Domain-specific depth:** CVSS v3.1 vs. v4.0 version precedence, OWASP Dependency-Check suppression lists (XML format), OSV ecosystem-specific version range resolution, CNA vs. NVD-assigned CVSS score precedence.

See `dependency-scanner/README.md` for full analysis.

---

### market-research — Business Strategy

**Unique feature: strict evidence/recommendation boundary.** The subagent produces evidence; the parent agent makes the decision. The go/no-go decision boundary is explicitly prohibited at the scope level, the constraints level, and the output schema level (no financial projections, no ROI estimates). The structural attractiveness summary paragraph is the designed release valve — it synthesizes evidence without concluding.

**Domain-specific depth:** Porter's Five Forces per-force evidence criteria, TAM/SAM/SOM methodology types (top-down, bottom-up, value-theory), Gartner Magic Quadrant citation requirements, SAM-to-SOM ratio analysis as a structural signal.

See `market-research/README.md` for full analysis.

---

### dnd-dungeon-master — Gaming / Creative

**Unique feature: dual-edition methodology.** The prompt contains separate encounter balancing protocols for the 2014 DMG (four-tier difficulty with XP multiplier) and the 2024 DMG (three-tier difficulty, no multiplier, per-character XP budget). The two methods are incompatible — a prompt that conflates them produces encounters calibrated to the wrong edition. The parent handoff specifies which edition to use.

**Domain-specific depth:** XP threshold tables by character level, adjusted XP multiplier breakpoints (1/1.5/2/2.5/3/4×), magic item table letter assignments (A–I), 2024 DMG recalibration at level 8+, NPC dialogue tree failure path requirement.

See `dnd-dungeon-master/README.md` for full analysis.

---

### sample-clearance — Music IP / Legal

**Unique feature: mandatory interpolation assessment.** Even when the producer intends direct sampling, the prompt mandates a separate interpolation path assessment. If the sampled element is melodic and the master rights holder is a major label, interpolation may eliminate the most difficult clearance step. This is a value-add the producer might not have thought to ask for; the prompt requires the subagent to surface it.

**Domain-specific depth:** master vs. composition dual-license structure, HFA vs. MLC post-Music Modernization Act responsibilities, four-tier clearance difficulty scale (EASY/MODERATE/DIFFICULT/UNCLEARED-RISK), WhoSampled precedent as corroborating (not conclusive) evidence.

See `sample-clearance/README.md` for full analysis.

---

### mix-master-critique — Audio Engineering

**Unique feature: input modality limitation handling.** This is the only example where the primary input (a stereo audio file) cannot be analyzed by a text-only model. The prompt handles this with an explicit degradation protocol: if audio cannot be analyzed directly, the subagent requests a meter readout from the parent rather than approximating measurements. This is architecturally honest — partial degradation with stated limitations is more useful than confident fabrication.

**Domain-specific depth:** ITU-R BS.1770-4 integrated LUFS measurement, platform loudness targets (Spotify −14, Apple −16, YouTube −14, Tidal −14), K-system reference metering (K-12/K-14/K-20), Fletcher-Munson equal loudness contours (ISO 226:2003), inter-sample true peak vs. digital peak distinction.

See `mix-master-critique/README.md` for full analysis.

---

### sourdough-diagnosis — Food Science + Vision

**Unique feature: generalization from a one-off prompt.** The invocation was a concrete user request ("Look at this photo of my sourdough and tell me what went wrong") rather than a specification-first request. The skill identified what was generalizable (diagnostic methodology, failure taxonomy, visual inspection protocol) and what needed to be parameterized (the specific photo, recipe context, intended crumb style) to produce a reusable subagent prompt from the one-off example.

**Domain-specific depth:** alveoli distribution patterns and their fermentation interpretations, poke test spring-back taxonomy (under/over/correctly-proofed), professional bread evaluation rubric (aspect, crust, crumb, aroma, sound/touch), quantified corrective action format (what/how much/how to verify), hydration guide (65–70% = closed crumb, 75–80% = open crumb).

See `sourdough-diagnosis/README.md` for full analysis.

---

## File Layout

Each trigger example directory contains four files:

| File | Contents |
|------|----------|
| `invocation.md` | The exact `/subagent-prompt-foundry` command, routing decision with criterion checklist, and research sources with URLs |
| `prompt.md` | The final generated system prompt — the primary deliverable |
| `metrics.json` | Four-dimension determinism input scores (structure_stability, constraint_preservation, research_completeness, protocol_clarity) |
| `validation.json` | Output from `validate_prompt_shape.py` confirming all required sections are present, plus the composite determinism score |
| `README.md` | This detailed analysis file (added in the v1.1 documentation pass) |

---

## Observations Across All Six Examples

**Research quality determines prompt quality.** All six examples performed domain-specific research before drafting. The research findings are visible in the prompts: CVSS v3.1/v4.0 precedence in the dependency scanner, the 2024 DMG multiplier removal in the D&D example, the MLC vs. HFA distinction in sample clearance, the ITU-R BS.1770-4 citation in the audio critique. Prompts written without this research would have used generic placeholders where domain-specific standards belong.

**Isolation is the distinguishing structural property.** Every prompt's Role section explicitly states that the subagent does not inherit the parent's context, prior session state, conversation history, or runtime environment. This isolation constraint is what makes the prompts "subagent prompts" rather than "system prompts for a single-context agent." Without isolation, there is no delegation contract — the subagent must receive everything it needs through the explicit handoff.

**The blocking_questions field is a reliability mechanism, not an afterthought.** All six prompts include specific, pre-populated blocking question examples in the return schema. These examples model the most common cases where the parent's handoff is ambiguous (market scope, edition selection, missing party composition, source track identification, audio reference track, bulk fermentation duration). By modeling these questions, the prompt teaches the subagent what to ask for rather than proceeding with silent assumptions.

**Constraints close failure modes that the positive instructions leave open.** The constraint sections in all six prompts are not generic safety disclaimers — they are domain-specific prohibitions derived from failure mode analysis. The dependency scanner cannot fabricate CVE IDs. The market researcher cannot make the go/no-go decision. The DM cannot approximate CRs. The clearance researcher cannot provide legal advice. The audio critic cannot use vague language without Hz/dB values. The sourdough diagnostician cannot diagnose flavor from a photo. Each constraint addresses a specific and plausible failure mode for that domain.
