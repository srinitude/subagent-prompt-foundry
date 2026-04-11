# market-research — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to business strategy: a parent agent evaluating whether to enter a new market delegates the competitive research to a specialist subagent. The result is a system prompt that enforces structured analytical frameworks (Porter's Five Forces, TAM/SAM/SOM, Gartner Magic Quadrant), strict source requirements, and a clear scope boundary — the subagent produces evidence, never makes the final decision.

---

## Domain: Competitive Market Research and Market Entry Evaluation

Market entry evaluation is one of the most common uses of structured analytical frameworks in business strategy. The core challenge is that market attractiveness is multi-dimensional: a market can be large (high TAM) but saturated (high competitive rivalry), or small but defensible (high entry barriers protecting incumbents). A single number or summary cannot capture this complexity, which is why frameworks like Porter's Five Forces exist.

### Porter's Five Forces

Michael Porter's framework, introduced in 1979, analyzes industry structure through five competitive forces that collectively determine average profitability:

1. **Threat of new entrants** — ease with which new competitors can enter the market. High capital requirements, regulatory licensing, brand loyalty, and economies of scale reduce this threat.
2. **Bargaining power of buyers** — ability of customers to drive prices down. High buyer concentration, low switching costs, and readily available alternatives increase buyer power.
3. **Bargaining power of suppliers** — ability of upstream suppliers to raise input costs. Concentrated suppliers with no substitutes and forward integration capability have high power.
4. **Threat of substitutes** — likelihood that a different product or service fulfills the same customer need. Substitutes don't need to be direct competitors — cloud storage is a substitute for external hard drives.
5. **Competitive rivalry** — intensity of competition among existing players. High rivalry is typical in markets with many similar-sized firms, low differentiation, slow growth, and high fixed costs.

The Five Forces are scored qualitatively (Low / Medium / High) and explained with evidence. The prompt enforces this structure precisely: each force must have a score and a supporting evidence summary. A Five Forces report without evidence is an opinion, not analysis.

### TAM / SAM / SOM

Market sizing uses three nested estimates:

- **TAM (Total Addressable Market)** — the revenue opportunity if a product captured 100% of the market. Usually estimated top-down from industry reports (IBISWorld, Gartner, IDC) or bottom-up from first principles (total potential buyers × average contract value).
- **SAM (Serviceable Addressable Market)** — the subset of TAM that a company can realistically reach given its product fit, geographic coverage, and distribution channels.
- **SOM (Serviceable Obtainable Market)** — the fraction of SAM that the company can capture within a defined time horizon, typically derived from analogous market penetration benchmarks or competitive win rates.

The prompt requires each estimate to state its methodology explicitly (top-down, bottom-up, or value-theory) and cite the source data. This is a critical discipline: TAM estimates that aren't grounded in a specific methodology or source are essentially guesses, and a business case built on ungrounded TAM estimates has failed at the foundation.

### Gartner Magic Quadrant

The Gartner Magic Quadrant is an annual analyst report positioning vendors across two axes: Ability to Execute (horizontal) and Completeness of Vision (vertical). Quadrant positions are Leaders, Challengers, Visionaries, and Niche Players. For the parent agent making a market entry decision, knowing whether the incumbents are Leaders (dominant execution and vision) or Niche Players (specialized, limited reach) is material to assessing how hard displacement will be.

The prompt acknowledges that not every market has a Gartner Magic Quadrant. The constraints section explicitly requires stating when Gartner data is unavailable rather than substituting a generic alternative framework without noting the difference.

### Why this tests the skill well

Market research is an excellent test for several skill properties:

**Source discipline.** Vague market research that cites "industry reports" without naming the publisher, title, and year is a common failure mode. The evidence standards in this prompt are unusually strict: every market size estimate must name its source, every competitor profile must reference a public record, and unverifiable figures must be labeled as estimates. This tests whether the skill can encode source discipline into a structured prompt rather than leaving it to the subagent's discretion.

**Scope boundary enforcement.** The parent agent makes the go/no-go decision; the subagent produces evidence only. This boundary is non-trivial to enforce because a helpful subagent will naturally drift toward making a recommendation. The prompt closes this with two explicit constraints: "Do not generate financial projections or ROI estimates" and "Do not make the go/no-go decision." The subagent returns evidence and flags uncertainty; the parent agent decides. This is a clean demonstration of the parent↔subagent separation of concerns.

**Framework parameterization.** Different market types require different Five Forces logic. A regulatory market (healthcare, financial services) has fundamentally different entry barriers than a commodity market. The constraints section addresses this: "Do not flatten all markets into the same template. Regulatory markets, platform markets, and commoditized markets each require different force scoring logic." This tests the skill's ability to build nuance into constraints rather than producing a generic template that collapses all markets into identical analysis.

---

## Routing Decision

**ACTIVATE.** The invocation states: "Design a subagent prompt for competitive market research that my parent agent delegates to when evaluating whether to enter a new market." This is a near-perfect trigger phrase:

1. The user asks for a "subagent prompt" — explicit.
2. The prompt defines a "competitive market research specialist" subagent — scoped role.
3. "My parent agent delegates to" — names the delegation relationship and implies reuse.
4. The user wants the prompt artifact, not the market research itself.

All four routing-checklist.md criteria pass cleanly. There is no ambiguity about whether this is a one-off research request (it is not) or a meta-agent request (it is not).

---

## Research Performed

The invocation.md records four research sources:

- **Porter's Five Forces** — the research verified the five force definitions, scoring scales, and typical evidence types for each force. This informed the methodology section's structured breakdown of each force with its specific evidence dimensions.
- **TAM/SAM/SOM** — research confirmed the three methodology types (top-down from reports, bottom-up from unit economics, value-theory from willingness-to-pay) and the typical sources for each (IBISWorld, Gartner, IDC for top-down; customer data or ICP analysis for bottom-up).
- **Gartner Magic Quadrant** — research confirmed the two axes (Ability to Execute vs. Completeness of Vision), the four quadrant positions (Leaders, Challengers, Visionaries, Niche Players), and the critical citation requirement (specific Quadrant name and publication year, since Gartner publishes quadrants annually and positions change).
- **IBISWorld and HG Insights methodology** — research into how SCA firms filter TAM to SAM (by geography, product fit, distribution channel) and how competitive win-rate data informs SOM estimates.

The research shaped three decisions:
1. The methodology section names specific report publishers (IBISWorld, Gartner, IDC) rather than generic "industry reports" because first-party source naming is what separates a useful evidence standard from a vague one.
2. The competitor profiling template explicitly includes "Gartner quadrant position if applicable" and flags when a Gartner report does not exist for the market.
3. The output JSON schema requires the TAM/SAM/SOM fields to carry both the value and the methodology and source — not just the number.

---

## What the Generated Prompt Covers

**Role** — "You are researching the competitive landscape and market attractiveness of a target market to support a go/no-go entry decision." The word "researching" (not "advising" or "recommending") signals the evidence-production posture. The scope explicitly prohibits making investment recommendations.

**Scope** — restricts analysis to the target market specified in the handoff, prevents expansion to adjacent markets without explicit parent authorization, and names the three analytical frameworks as the required analytical lens.

**Task** — specifies five deliverables: Porter's Five Forces analysis with force-level scores and evidence, TAM/SAM/SOM sizing with methodology stated, competitive landscape with 3–5 profiles, entry barriers enumerated by type (regulatory, capital, switching cost, network effect), and a structural attractiveness summary paragraph.

**Methodology** — six ordered steps: define the market (with instructions to flag ambiguity as a blocking question if the scope is unclear), run Porter's Five Forces (with per-force evidence criteria), size the market (with the three TAM/SAM/SOM approaches), profile competitors (capturing revenue/valuation, product, differentiation, Gartner position, recent moves), enumerate barriers (distinguishing structural from execution barriers), and synthesize (comparing Five Forces profile against competitive density and TAM/SOM ratio).

**Output schema** — the return JSON carries a full nested structure: each Porter force with score and evidence, market sizing with value/methodology/source per tier, a competitor array, an entry barriers array, and a structural attractiveness summary string. The confidence field encodes the degradation rule: HIGH if all five forces are evidenced and TAM is sourced, MEDIUM if any force lacks support or TAM is unverifiable.

---

## Determinism Score: 0.925

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.93 | The Five Forces + TAM/SAM/SOM + competitor profile structure is stable across market research requests. Minor variation risk when a market lacks Gartner coverage. |
| constraint_preservation | 0.92 | All key constraints (source requirements, no investment recommendations, no go/no-go decision) are preserved. Small gap: the 2-year data currency constraint allows some interpretation at the margin. |
| research_completeness | 0.90 | Three frameworks well-researched. Slight gap: IBISWorld pricing and access method not researched (relevant if the parent specifies tool availability). |
| protocol_clarity | 0.95 | The parent↔subagent schema is clear and all fields have unambiguous types. The `blocking_questions` field is populated with a concrete example (market definition ambiguity). |

The 0.925 overall score reflects a slightly higher level of inherent variability than the dependency-scanner (0.95). Market research involves more judgment — a Five Forces score of "Medium" vs. "High" competitive rivalry requires genuine evidence interpretation, not just a lookup table. The prompt is designed to minimize arbitrary judgment (by requiring evidence for each score) but cannot fully eliminate it.

---

## Interesting Observations

**The go/no-go boundary is the hardest constraint to enforce.** A well-informed market research subagent will naturally want to conclude with a recommendation. The constraints section explicitly forbids this, but enforcement depends on the subagent respecting the boundary at inference time. The structural attractiveness summary paragraph is the designed release valve: it synthesizes the evidence into a single paragraph that implicitly points toward or away from entry, without stating "enter" or "don't enter." This respects the boundary while being genuinely useful to the parent agent.

**Blocking questions as a reliability mechanism.** If the market definition is ambiguous (e.g., "the healthcare market" — which segment? which geography?), a market research subagent that proceeds with assumptions produces a Five Forces analysis that may be entirely wrong for the parent's actual target. The prompt handles this by requiring the subagent to flag ambiguity as a blocking question rather than guessing. The blocking_questions field in the return schema is populated with a concrete example: "Should the analysis include [adjacent segment]?"

**The SAM-to-SOM ratio as a signal.** The synthesis step explicitly instructs the subagent to compare the TAM/SOM ratio (how much of the addressable market the entrant could capture) against competitive density (how many players are competing for the same SAM). A large TAM with a tiny SOM and high rivalry is a red flag. A moderate TAM with a high SOM because the competitive density is low is an opportunity. This ratio is not a standard output in most market research templates; its inclusion reflects the research into how analysts actually use these frameworks in strategic decisions.
