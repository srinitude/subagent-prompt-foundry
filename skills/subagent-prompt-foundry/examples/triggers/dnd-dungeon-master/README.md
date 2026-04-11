# dnd-dungeon-master — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to tabletop gaming: a parent campaign manager agent that delegates D&D 5th Edition content generation — balanced encounter tables, loot drop tables, and NPC dialogue trees — to a specialist dungeon master subagent. This is an unusual test case because the domain is creative and ludic rather than professional, yet the underlying mechanics are as rules-bound and deterministic as any technical domain.

---

## Domain: D&D 5e Encounter Balancing and Content Generation

Dungeons & Dragons 5th Edition (5e) is a structured role-playing game with explicit mathematical frameworks for designing balanced encounters. The game is published by Wizards of the Coast (a Hasbro subsidiary), and its rules are partly available under the Systems Reference Document (SRD) via Creative Commons.

### Challenge Rating (CR) and XP

Every monster in D&D 5e has a Challenge Rating (CR) that estimates its difficulty for a standard party of four characters. CR values map to XP (experience point) rewards: CR 1 = 200 XP, CR 5 = 1,800 XP, CR 17 = 18,000 XP, and so on. The mapping is not linear — it reflects an empirical calibration of monster statistics against typical party capability at each tier of play.

CR is not a raw difficulty number; it is an expected-difficulty-for-a-party-of-four baseline. Multiple monsters compound in unpredictable ways, which led to the encounter XP multiplier system in the 2014 DMG.

### XP Thresholds and the 2014 DMG Method

The 2014 Dungeon Master's Guide (DMG) defines encounter difficulty via XP thresholds by character level. Each character at each level has four thresholds — Easy, Medium, Hard, and Deadly. A party's total threshold for a given difficulty tier is the sum of each character's individual threshold.

The **encounter XP multiplier** adjusts for the compounding threat of multiple monsters:
- 1 monster: ×1.0
- 2 monsters: ×1.5
- 3–6 monsters: ×2.0
- 7–10 monsters: ×2.5
- 11–14 monsters: ×3.0
- 15+ monsters: ×4.0

The adjusted encounter XP (monster XP × multiplier) is compared to the party threshold to determine difficulty. This method has been the standard for D&D 5e since 2014.

### XP Budget and the 2024 DMG Method

The 2024 DMG revision, released in late 2024, overhauled the encounter-balancing system. Key changes:
- The four-tier naming changed: Easy, Medium, Hard, Deadly → Low, Moderate, High.
- **The XP multiplier was removed entirely.** Monster XP is summed directly without adjustment.
- Instead, the system uses an XP budget per character at each level, multiplied by party size, as the encounter budget ceiling.
- Thresholds were recalibrated, particularly at higher levels (8+), where the 2014 method produced systematically over-lethal encounters.

This distinction matters enormously for the subagent: a prompt that conflates the two editions will produce encounter tables that are incorrectly balanced. A 2024 DMG user following 2014 multiplier logic will create encounters that are 1.5–4× harder than intended.

### Magic Item Tables and Loot Tiers

The 2014 DMG divides magic item tables into two categories: Individual Treasure (per-monster, by CR tier) and Treasure Hoards (for a group or boss encounter). Magic items are distributed across tables A through I, with table letter roughly corresponding to item power level. Hoard tables reference which magic item subtable to roll on.

CR tiers for loot: 0–4, 5–10, 11–16, 17+. A CR 5 encounter uses the 5–10 loot table; a CR 17 encounter uses the 17+ table. Matching loot to encounter tier is essential — awarding Legendary items to a CR 3 encounter breaks campaign economy.

### NPC Dialogue Trees

Dialogue trees in tabletop RPGs are structured branching conversations. Unlike video game dialogue trees, tabletop trees are guidance documents for the DM — the DM adapts them at the table. A well-formed tree specifies: the NPC's motivation, information gates (what the NPC reveals freely vs. under social pressure), skill check difficulty classes (DCs), and failure paths (what happens when a check fails). The PHB establishes DC standards: Easy DC 10, Medium DC 15, Hard DC 20.

### Why this tests the skill well

D&D encounter balancing is a perfect test case for a core claim of the `subagent-prompt-foundry` skill: that **deterministic rules applied to creative output** is an ideal subagent pattern. The content is creative (encounter themes, flavor text, NPC personalities) but the mathematical framework is entirely deterministic. The subagent's job is to apply the XP calculation correctly and then fill the validated encounter slots with creative content. The creative layer cannot contaminate the mechanical layer.

This creates an interesting structural challenge for the prompt: the methodology section must be mathematically precise (exact steps for XP calculation) while the task section permits creative latitude (encounter themes, NPC dialogue). The prompt manages this by separating the balancing methodology from the content generation guidelines.

The 2014/2024 DMG split is also a test of the prompt's parameterization. A good subagent prompt accounts for external variability (which edition?) and binds that variable to a handoff parameter rather than hardcoding a default and silently applying it regardless of what the parent sends.

---

## Routing Decision

**ACTIVATE.** The invocation states: "Create a reusable system prompt for a D&D dungeon master subagent that generates balanced encounter tables, loot drops, and NPC dialogue trees for a parent campaign manager agent."

- "Reusable system prompt" — explicit.
- "D&D dungeon master subagent" — scoped custom role.
- "For a parent campaign manager agent" — parent delegation named.
- "Generates" (not "generate this specific encounter") — signals ongoing reuse, not a one-off.

All four routing-checklist.md criteria pass. The creative domain is not a routing obstacle: the skill is domain-agnostic, and gaming/creative content generation is as valid a subagent use case as DevSecOps.

---

## Research Performed

The invocation.md records four research sources:

- **D&D Beyond — Building Combat Encounters** — the primary source for the XP Thresholds by Character Level table and the adjusted XP multiplier rules. This is a first-party source (D&D Beyond is Wizards of the Coast's official digital platform). The research confirmed the four difficulty tiers and the exact multiplier breakpoints (1, 2, 3–6, 7–10, 11–14, 15+).
- **DMG Loot Tables** (dungeonmastertools.github.io) — verified the magic item table letter assignments (A–I), the CR tier breakpoints (0–4, 5–10, 11–16, 17+), and the coin/gem/art object distributions within each tier.
- **2024 DMG Encounter Math vs. 2014** (ENWorld thread) — the most critical research finding. This source confirmed that the 2024 DMG removes the XP multiplier entirely and changes the difficulty tier naming, with the balancing changes being most significant at level 8 and above. Without this research, the prompt could not have distinguished the two methods cleanly.
- **ChallengeRated.com** — an independent encounter calculation tool that independently verified the XP budget methodology for the 2024 rules.

The research shaped the prompt's most important structural decision: dual encounter balancing methodology sections, one for each edition. These are kept separate rather than merged, because the two methods are not compatible — mixing their logic produces incorrect results.

---

## What the Generated Prompt Covers

**Role** — "You are generating structured Dungeons & Dragons 5th Edition (D&D 5e) content — balanced encounter tables, loot drop tables, and NPC dialogue trees — on behalf of a parent campaign manager agent." The word "generating" signals a production role, and "on behalf of a parent campaign manager agent" explicitly names the delegation relationship.

**Scope** — restricts content to the 5e edition specified by the parent (2014 or 2024 DMG), prohibits homebrew unless explicitly permitted, and prevents scope creep into full adventure modules or campaign arcs unless the parent extends scope.

**Inputs** — the handoff schema captures: content type requested, D&D edition, party composition (count and level), encounter difficulty target, environment/biome, tone, and homebrew permission. These six parameters fully determine the encounter balancing calculation; no other inputs are needed.

**Task** — three subtasks (A, B, C): encounter table (d6 or d8, mixed combat/skill/exploration rows, each with roll range, monster names/CRs, total XP, difficulty rating, and flavor hook), loot drop table (d100, keyed to CR tier, with coin/gem/art object awards and magic item table reference), NPC dialogue tree (branching, minimum 3 player options per node, skill check DCs, failure paths).

**Methodology** — the most technically detailed section, with two encounter-balancing sub-protocols (2014 DMG and 2024 DMG) presented side by side. The loot assignment methodology maps CR tier to the correct DMG table. The NPC dialogue methodology specifies the minimum branching structure, DC standards, and failure path requirement.

**Evidence standards** — every monster CR must cite an official source; every XP value must derive from the applicable DMG table; magic item tables must cite the specific letter; homebrew must be labeled.

**Output schema** — returns structured encounter tables, loot tables, and dialogue trees in Markdown, with a JSON metadata block at the end for the parent to parse programmatically.

---

## Determinism Score: 0.92

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.93 | The three content type sections (encounter, loot, NPC) are stable across requests. The edition parameter creates a bifurcation in the methodology but not in the output structure. |
| constraint_preservation | 0.90 | Core constraints (XP accuracy, official sources, homebrew labeling) are preserved. Small gap: the "tone" parameter (gritty/heroic/comedic/horror) influences creative content but the prompt does not specify how tone affects mechanical choices. |
| research_completeness | 0.91 | Both edition methodologies were researched. Minor gap: the 2024 DMG NPC guidance was not separately verified; the NPC section draws primarily from 2014 PHB standards. |
| protocol_clarity | 0.94 | The handoff schema is well-specified. The `blocking_questions` field includes concrete examples for missing party composition or difficulty target. |

The 0.92 score is the second-lowest among the trigger examples (sourdough-diagnosis is 0.923, market-research is 0.925). The creative domain introduces inherent variability at the content layer that cannot be fully eliminated without over-constraining the creative output. The mechanical layer is highly deterministic; the creative layer (flavor hooks, NPC personalities, encounter themes) is deliberately open. This is the correct tradeoff for a dungeon master subagent.

---

## Interesting Observations

**The 2014/2024 distinction is not cosmetic.** The removal of the XP multiplier in 2024 is a substantive rules change that affects encounter lethality calculations by a factor of 1.5× to 4× depending on monster count. A DM using a 2014-calibrated subagent in a 2024 campaign would be generating encounters that are systematically more dangerous than intended — potentially lethally so at high monster counts. The dual-methodology structure in the prompt is not redundancy; it is a safety mechanism.

**Skill challenge inclusion is a quality signal.** The constraints section explicitly forbids the subagent from producing encounter tables that are 100% combat. "Include at least one skill challenge and one exploration or social encounter variant per encounter table." This reflects a well-known critique of D&D encounter generators: they default to combat because combat mechanics are the most precisely defined. A good DM encounter table is mixed-mode. The prompt enforces this by treating it as a constraint, not a suggestion.

**Homebrew flagging as audit trail.** The prompt requires homebrew content to be labeled "HOMEBREW" with a full stat block or description. This is not a security feature — it is a practical DM tool. When a DM shares their session notes or encounter tables with other DMs, homebrew items need to be identifiable so they can be adapted for campaigns that lack the source material. The subagent's role is to produce portable, reusable content; unlabeled homebrew breaks portability.

**The dialogue tree failure path is the neglected half.** Most NPC dialogue systems focus on success paths: if the player persuades the NPC, they learn the location of the dungeon. The prompt mandates that every check also has a failure path with a consequence — not just a locked door. "The NPC does not simply lock; provide a consequence (combat, withdrawal, partial information, or rumor)." This reflects real tabletop play: failed skill checks that produce no consequence are boring and unrealistic. The constraint pushes the subagent toward higher-quality branching narratives.
