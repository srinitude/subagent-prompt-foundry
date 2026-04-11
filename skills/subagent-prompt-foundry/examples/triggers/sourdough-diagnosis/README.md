# sourdough-diagnosis — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to food science and computer vision: a parent baking assistant agent delegates sourdough loaf diagnosis to a specialist subagent that analyzes a photo of the baked loaf (cross-section preferred) and identifies the most likely process failure from a structured failure taxonomy. The example is notable for testing the skill in a domain where the primary input is an image rather than text or structured data, and where the diagnostic methodology draws on both food microbiology and visual pattern recognition.

---

## Domain: Sourdough Fermentation Science and Crumb Analysis

Sourdough bread is leavened by a naturally occurring starter culture containing wild yeasts (primarily Saccharomyces cerevisiae and Kazachstania humilis) and lactic acid bacteria (LAB, primarily Lactobacillus species). The starter ferments a flour-and-water mixture through two stages: bulk fermentation (the initial rise of the dough mass) and final proofing (the rise of the shaped loaf before baking). Both stages are sensitive to time, temperature, and starter strength, making sourdough one of the most process-dependent foods a home baker can produce.

### The Crumb as a Diagnostic Record

The interior structure of a baked loaf — the "crumb" — is a record of the fermentation history. The gas pockets (alveoli) are CO₂ bubbles produced by yeast activity during fermentation. Their size, distribution, and cell-wall thickness encode information about when, how much, and how evenly fermentation occurred. Unlike a cooking error that changes flavor without visible evidence, a fermentation error almost always leaves a distinct visual signature in the crumb.

This is what makes crumb analysis a natural subagent specialization: the same visual patterns appear reliably across different recipes, flours, and bakers. A diagnostic trained on the visual signatures of under-proofing, over-proofing, and shaping failures can interpret a new loaf photo without knowing the specific recipe — the crumb is the evidence.

### Failure Taxonomy

The prompt uses a standardized failure taxonomy:

- **Under-fermentation**: insufficient yeast/LAB activity during bulk fermentation. The dough did not develop enough gas. Visual: dense crumb throughout, tight alveoli, no open structure. Often accompanied by a gummy or wet interior despite appearing baked. Distinguished from under-proofing because the problem originated in bulk fermentation, not the final proof stage.

- **Over-fermentation**: bulk fermentation extended too long. The gluten network degraded as LAB produced excess organic acids. Visual: flat loaf that spread laterally instead of rising, possibly with a light and airy crumb (because gas was produced) but poor structure retention. The gluten failed before baking and the loaf lost its shape.

- **Under-proofing**: bulk fermentation was adequate but the final proof was too short. The dough had structure but not enough gas volume in the final shape. Visual: dense crumb with random large holes (as the oven spring broke through weak points in the structure), side splits (the loaf expanded at unintended weak points rather than the score line), and a squat profile.

- **Over-proofing**: final proof was too long. The gluten exhausted itself supporting the gas volume. Visual: flat loaf, collapsed alveoli, sunken center or collapsed shoulders, no ear on the score. The dough deflated partially during baking because the gluten could no longer hold the gas.

- **Shaping tension failure**: inadequate surface tension during shaping. The loaf spread rather than rising because the outer skin was too slack to hold the gas upward. Visual: pancake or frisbee shape with good oven spring once in the oven (distinguishing it from over-fermentation).

- **Hydration mismatch**: the dough's water content was too high or too low for the flour type or desired crumb structure. Visual: at high hydration, tunneling (elongated horizontal holes) or extremely open crumb that collapsed; at low hydration, too-dense crumb even with good fermentation.

- **Scoring failure**: the score line (the slash made with a lame or razor before baking) was too shallow, in the wrong position, or applied to over-proofed dough. Visual: the ear (the raised flap along the score line) is absent or malformed; the loaf may have burst at an unintended location.

- **Baking environment issue**: oven temperature, steam method, or baking vessel problems. Visual: pale crust (low temperature or insufficient bake time), thick hard crust without blistering (no steam), or excess browning.

### Poke Test

The poke test is performed on the shaped, proofed dough immediately before baking: the baker presses a finger approximately 1 cm into the dough and observes the spring-back speed:
- **Springs back quickly and completely**: under-proofed (dough is tight, needs more time).
- **No spring-back, indentation stays**: over-proofed (gluten exhausted, bake immediately or sooner next time).
- **Springs back slowly but not fully**: correctly proofed (the ideal moment to bake).

The poke test is corroborating evidence, not a primary diagnostic tool. It must be correlated with visual diagnosis from the baked loaf to have full diagnostic value.

### Professional Bread Evaluation Rubric

The Cereals & Grains Association's professional bread evaluation rubric assesses loaves across five dimensions: aspect (lift and oven spring), crust (color, texture, blistering), crumb structure (alveoli size/distribution, cell wall thickness, gumminess), aroma, and sound/touch (crust crackling, interior spring). The prompt adopts this rubric as the structured visual inspection protocol, using the five dimensions as the column headers for the visual_inspection object in the return JSON.

### Why this tests the skill well

**Image as primary input.** The sourdough diagnosis example is the only one in this set where the primary diagnostic input is an image, not text or structured data. This tests the skill's ability to specify how a subagent handles a non-textual modality: the prompt must instruct the subagent to treat visual evidence as the primary diagnostic source and contextual notes (recipe details, bulk time, temperature) as secondary evidence. The prompt also must handle the case where the photo quality or angle is insufficient for diagnosis — in which case the subagent must state the limitation explicitly and ask for a better photo.

**Generalization from a one-off prompt.** The invocation is unusual among the six examples: the user provides a concrete one-off request ("Look at this photo of my sourdough and tell me what went wrong") and asks the skill to generalize it into a reusable subagent prompt. This tests the skill's ability to identify what is generalizable (the diagnostic methodology, the failure taxonomy, the visual inspection protocol) and what needs to be parameterized (the specific loaf photo, the recipe context, the baker's intended crumb style).

**Quantified corrective actions.** A corrective action that says "ferment longer" is not useful. A corrective action that says "extend bulk fermentation by 45 minutes at 22°C; verify success by observing 50–75% volume increase with domed surface and visible bubbles" is actionable. The prompt enforces quantified corrective actions by specifying a required format: what to change, how much to change (with specific quantities), and how to verify success before the next step.

---

## Routing Decision

**ACTIVATE.** The invocation states: "Turn this into a reusable subagent prompt: 'Look at this photo of my sourdough and tell me what went wrong.' I want my baking assistant agent to delegate crumb analysis to a specialist subagent."

- "Reusable subagent prompt" — explicit.
- "My baking assistant agent to delegate" — parent delegation named.
- "Specialist subagent" — scoped custom role.
- "Turn this into" — generalizing a one-off prompt, a named trigger pattern from SKILL.md.
- The user wants the prompt infrastructure, not the crumb analysis itself.

All four routing-checklist.md criteria pass. The "turn this into a reusable subagent prompt" pattern is explicitly named as a trigger in SKILL.md: "a prompt that should be generalized from an example."

---

## Research Performed

The invocation.md records five research sources:

- **Pauline Manor — Underproofed vs. Overproofed** — confirmed the visual indicators for under-proofing (tight crumb, side splits, fast poke test) and over-proofing (flat loaf, no oven spring, no poke test spring-back). Also confirmed the common diagnostic confusion between the two failure modes.
- **The Sourdough Journey — Open Crumb FAQ** — confirmed the hydration guide (65–70% hydration = closed/tight crumb; 75–80% Tartine style = open crumb) and the role of bulk fermentation as the primary driver of crumb openness.
- **Simply Bread — Reading Crumb Structure** — confirmed the alveoli size/distribution indicators, the tunneling pattern (shaping fault), and the compressed crumb pattern (fermentation failure).
- **Cereals & Grains / King Arthur Scoring Rubric PDF** — the professional five-dimension evaluation framework: aspect (lift/spring), crust color, crumb texture, aroma, sound/touch. This is the closest available professional standard for bread evaluation, analogous to a rubric from a culinary institute or baking certification body.
- **Instagram diagnostic guide** — scenario mapping: flat dough + dense bake = under-fermentation; flat dough + light bake = over-fermentation; flat dough + good oven spring = tension failure. This practical heuristic map informed the failure mode classification decision tree.

The research produced the diagnostic decision tree in the Methodology section — a structured conditional logic that maps visual patterns to failure modes rather than asking the subagent to make unconstrained judgments.

---

## What the Generated Prompt Covers

**Role** — "You are diagnosing the fermentation, proofing, and baking outcome of a sourdough loaf from a photo and contextual details provided by the baker." The diagnostic posture is explicit; the isolation constraint is stated: "You do not inherit the baking assistant agent's conversation history, the baker's recipe, or previous loaf assessments unless explicitly passed in the handoff."

**Visual inspection protocol** — four dimensions with specific visual indicators for each:
1. Crumb/alveoli: even distribution (healthy), dense compression (under-fermentation or under-proofing), collapsed honeycomb (over-fermentation), tunneling (shaping fault).
2. Loaf shape and oven spring: good spring (well-proofed), pancake/frisbee shape (over-fermentation or weak gluten), squat with side splits (under-proofing), collapsed shoulders (over-proofing).
3. Score/ear: dramatic ear (well-proofed), no ear (over-proofed or inadequate steam), burst at wrong location (under-proofed).
4. Crust color and texture: deep amber (adequate bake), pale (under-baked), blistering (positive fermentation sign).

**Failure mode classification decision tree** — a conditional table mapping visual pattern combinations to failure modes. This is the structural heart of the prompt: it converts visual observation into a probability-ranked diagnostic output rather than a freeform opinion.

**Corrective action standards** — the three-field format (what to change, how much to change, how to verify success) with quantified examples.

**Output schema** — returns primary_diagnosis with failure mode and confidence rating (High/Medium/Low with justification rules), secondary_diagnoses (maximum 2), corrective_actions array, poke test interpretation, and hydration note.

---

## Determinism Score: 0.923

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.93 | The five-dimension visual inspection protocol and the primary/secondary/corrective action output structure are stable across sourdough loaf analyses. |
| constraint_preservation | 0.92 | Core constraints (quantified corrective actions, no flavor diagnosis without tasting notes, confidence justification rules) are preserved. Small gap: the intended crumb style clarification question is present but not prominently featured. |
| research_completeness | 0.91 | Five sources consulted covering visual indicators, hydration effects, professional rubric, and practical diagnostic heuristics. Minor gap: starter strength assessment (a factor in under-fermentation diagnosis) was not separately researched. |
| protocol_clarity | 0.93 | The JSON schema handles all six output components. The blocking question examples (missing crumb cross-section, missing bulk time) are concrete and actionable. |

The 0.923 score reflects a domain where the primary evidence is visual and the failure mode classification involves genuine inference. Unlike the dependency scanner (binary CVE presence/absence) or the mix critique (quantitative LUFS deltas), sourdough diagnosis requires mapping a visual gestalt to a causal explanation. The prompt minimizes this variability through the decision tree, but cannot eliminate it entirely.

---

## Interesting Observations

**Cross-section vs. exterior photo.** A crumb cross-section photo provides the primary diagnostic evidence (alveoli distribution, cell wall thickness, tunneling patterns). An exterior-only photo provides secondary evidence (crust color, shape, score ear). The prompt explicitly addresses this gap: if only an exterior photo is available, the subagent should flag it as a lower-confidence diagnosis and ask for a cross-section. The blocking question is specified verbatim: "Can you provide a crumb cross-section photo? Exterior analysis has lower confidence for fermentation diagnosis."

**The under-fermentation / under-proofing diagnostic challenge.** Under-fermentation and under-proofing are the two most commonly confused failure modes. Both produce dense crumb. Both can produce side splits. The distinguishing evidence is in the degree of severity and the timing context: under-fermentation produces uniformly dense crumb even at the top of the loaf (because the gas was never produced); under-proofing often produces denser crumb at the bottom with some alveoli at the top (because some gas developed but the final proof was cut short). The decision tree encodes this distinction.

**The intended crumb style question.** Not every closed crumb is a failure. A sandwich loaf or a pan loaf is intentionally closed-crumb; a baker producing this style should not be told their bread is under-fermented. The constraints section addresses this: "Do not assume the baker made an error if the crumb is intentionally closed (e.g., a sandwich loaf style) — ask about the intended crumb style if not stated." This is a nuance that only emerges from understanding baking culture rather than just fermentation science.

**Temperature specificity in corrective actions.** The prompt's evidence standards tie corrective action quantities to fermentation science baselines: "bulk fermentation at 22°C typically requires 4–8 hours for a 20% levain; cold retard at 4°C slows fermentation to near-zero." These baselines allow the subagent to recommend "extend bulk by 45 minutes at 22°C" rather than "ferment longer." The temperature specificity is non-trivial: a 45-minute extension at 28°C (a warm kitchen in summer) has a completely different effect than the same extension at 18°C (a cold kitchen in winter). The prompt constrains the subagent to cite the temperature assumption when making time-based recommendations.
