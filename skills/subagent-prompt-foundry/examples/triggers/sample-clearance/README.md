# sample-clearance — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to music intellectual property law: a parent beat-making agent delegates sample clearance research to a specialist subagent that identifies the rights holders and classifies clearance difficulty for any given music sample. The domain is legally sensitive, which places unusual demands on the prompt's scope constraints — the subagent must research facts without crossing into legal advice.

---

## Domain: Music Sampling, Dual-License Structure, and Clearance Research

Music sampling involves taking a portion of a recorded sound and incorporating it into a new work. From a copyright perspective, sampling is one of the most complex licensing scenarios in intellectual property law because it implicates two entirely separate and independently owned copyrights: the **master recording** and the **musical composition**.

### The Dual-License Problem

**Master rights** (also called "sound recording copyright") are typically owned by the record label that funded the recording session. When an artist signed to a major label records a song, the label holds the master. If the artist is independent or later reclaimed their masters (as Taylor Swift did with her re-recorded albums), the artist or their estate may own the master. Master rights have changed hands repeatedly through label acquisitions: many masters originally owned by small independent labels from the 1960s–1980s are now controlled by Universal Music Group, Sony Music, or Warner Music Group.

**Composition rights** (also called "publishing rights") are owned by the songwriter(s) and administered by their publishing company. The publishing company registers the composition with a Performing Rights Organization (PRO): ASCAP, BMI, SESAC in the United States; SOCAN in Canada; PRS in the UK. The composition right covers the underlying melody, harmony, and lyrics — the musical ideas, independent of any particular recording.

For a producer who wants to directly sample a sound recording and include it in a commercially released track, **both licenses are required**:
1. A **master use license** from the label or artist who owns the master recording.
2. A **synchronization/mechanical license** (often called a "composition license" in the sampling context) from the publisher who controls the composition copyright.

Neither license automatically implies the other. Clearing the master does not grant the right to use the composition, and vice versa.

### Interpolation as an Alternative Path

Interpolation is the practice of re-recording the melodic or harmonic elements of a source track (the "hook" or "riff") rather than lifting the original sound recording. Because interpolation uses a new recording, the **master use license is not required** — only the composition license. However, the composition must still be cleared from the publisher; there is no free-ride on composition rights simply because the master was not used.

Interpolation is not always viable. It makes sense when:
- The sampled element is melodic (a riff, chord progression, or vocal phrase that has an underlying composition).
- The original master owner has refused or would likely refuse clearance.
- The producer's budget cannot support a major-label master use fee.

Interpolation is **not viable** when the sampled element is purely textural or rhythmic (a drum break, ambient noise, spoken word without melodic content). There is no copyrightable composition underlying a drum hit; the only copyright at stake is the master, and interpolation doesn't help.

### The Harry Fox Agency and the MLC

Two institutions have historically administered mechanical licensing in the United States:

**Harry Fox Agency (HFA)** was the dominant mechanical licensing agent for physical phonorecords (vinyl, CDs) and digital permanent downloads for decades. HFA issued compulsory mechanical licenses on behalf of publishers and collected royalties. HFA's role has narrowed significantly following the Music Modernization Act of 2018.

**The Mechanical Licensing Collective (MLC)** was created by the Music Modernization Act of 2018 and launched in January 2021. The MLC administers blanket mechanical licenses for interactive streaming in the United States. For a producer seeking a mechanical license for a new release that will be distributed on streaming platforms, the MLC is now the relevant entity.

However, the MLC's blanket license does not cover sample clearance. Sample licensing is negotiated directly with the publisher, not through the MLC's compulsory license mechanism. The distinction matters: a producer cannot use the MLC's compulsory process to clear a sample; they must negotiate with the publisher directly (or through the publisher's licensing department or sub-publisher).

### WhoSampled and Sample Precedent

WhoSampled.com is the largest crowdsourced database of sample, cover, and remix connections in recorded music. For clearance research, WhoSampled serves as precedent evidence: if a song has been sampled in multiple commercially released, mainstream-distributed tracks, those prior uses imply that clearance was successfully obtained (or at least that the rights holders did not pursue legal action, which can be informative in itself). WhoSampled data is corroborating, not definitive — it is not legal proof of clearance status.

### Clearance Difficulty Tiers

The prompt defines a four-tier classification system:

- **EASY**: independent artist retains masters; small publisher; prior commercial clearance history; brief or non-melodic element.
- **MODERATE**: mid-size label owns masters; established publisher; no known refusals; prior cleared uses.
- **DIFFICULT**: major label (Universal, Sony, Warner) owns masters; prominent publisher (Big Three or major sub-publisher); recognizable hook anchoring the new track; artist or estate known for restrictions.
- **UNCLEARED-RISK**: estate actively litigates against samplers; label has issued cease-and-desist letters; notoriously restrictive rights holder; no precedent of cleared samples from this catalog.

These tiers are research-based risk assessments, not legal conclusions. The subagent states them as such.

### Why this tests the skill well

Sample clearance research is an ideal subagent task because:

1. **The research is well-defined and database-driven.** The subagent queries ASCAP ACE, BMI Repertoire, Discogs, AllMusic, MusicBrainz, and WhoSampled — all publicly accessible databases with structured data. This is exactly the kind of repeatable, database-driven research that a specialized subagent handles better than a general-purpose agent.

2. **The scope boundary (no legal advice) is a hard constraint.** The subagent produces factual ownership research; an entertainment attorney handles negotiation. A poorly specified prompt will let the subagent drift into quasi-legal recommendations ("you should try to clear this for a buyout fee of X"). The prompt's constraints section explicitly prohibits legal advice and license drafting.

3. **The dual-license structure is non-obvious.** A general-purpose agent asked "can I sample this song?" would likely either give a trivially simple answer (yes/no) or a generic disclaimer. A specialist subagent with explicit dual-license methodology will correctly identify both rights holders and separate the master research from the composition research.

---

## Routing Decision

**ACTIVATE.** The invocation states: "Create a reusable subagent prompt for sample clearance research. My beat-making agent needs to delegate to a specialist that identifies the original song, publisher, master owner, and clearance difficulty for any sample a producer wants to flip."

- "Reusable subagent prompt" — explicit.
- "My beat-making agent needs to delegate to a specialist" — parent delegation named.
- "For any sample a producer wants to flip" — signals ongoing reuse across many tracks, not a one-time research request.
- The user wants the prompt infrastructure, not the actual clearance research.

All four routing-checklist.md criteria pass cleanly.

---

## Research Performed

The invocation.md records six research sources:

- **Tracklib — Sample Clearance Guide** — confirmed the master-vs-composition dual-license requirement, the two-step clearance process, and the interpolation path.
- **Musicians Institute — Master vs. Publishing Rights** — confirmed the ownership definitions for each right and the practical differences between direct sampling and interpolation.
- **Harry Fox Agency** (via exploration.io) — confirmed HFA's role in mechanical licensing for physical/permanent-download formats and its narrowed role post-MMA.
- **Horn Wright LLP — Sampling Law** — confirmed that there is no fair use defense for commercial sampling in the United States (a common misunderstanding), and that both the master use and composition license are required regardless of sample length.
- **WhoSampled** — confirmed the platform as the primary precedent research tool.
- **Good Morn Music — HFA vs. MLC** — clarified the post-MMA division of responsibilities: HFA for legacy formats, MLC for U.S. interactive streaming mechanicals.

This research produced the prompt's most important structural features: the explicit interpolation assessment step, the four-tier clearance difficulty scale, and the explicit note that WhoSampled evidence is corroborating rather than legally conclusive.

---

## What the Generated Prompt Covers

**Role** — "You are researching the copyright ownership and clearance complexity of a music sample on behalf of a producer who wants to use it in a new release." The "on behalf of" framing immediately establishes the delegation relationship.

**Scope** — requires treating the master side and composition side as two distinct and separately licensed rights. The scope explicitly covers both direct sampling and interpolation as distinct licensing paths. The prohibition on legal advice is stated at the scope level, not just in the constraints section.

**Methodology** — six steps: identify the source track (via audio fingerprinting or metadata), identify master rights (label lookup, acquisition history, independent verification), identify composition rights (ASCAP/BMI/SESAC database queries), classify clearance difficulty using the four-tier scale, assess interpolation viability (melodic vs. textural analysis), and search WhoSampled for precedent.

**Output schema** — the JSON return structure separates master_rights and composition_rights into distinct objects with their own source citations. The clearance_difficulty object carries both the rating and a rationale string. The interpolation_path object carries a viability boolean and explanatory notes. The sample_precedent object carries the WhoSampled URL and counts.

**Evidence standards** — strict source citation requirements: every ownership claim must cite a named database with URL; pre-1978 works require copyright.gov verification; unverified ownership must be labeled explicitly (not silently left blank).

---

## Determinism Score: 0.945

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.94 | The seven-step research methodology and the dual master/composition output structure are stable across sample clearance requests. |
| constraint_preservation | 0.96 | The highest constraint score among all examples. The dual-license requirement, interpolation assessment, and no-legal-advice boundary are all explicitly preserved. |
| research_completeness | 0.93 | Six sources consulted, covering both the legal framework and the practical database tools. Minor gap: SESAC repertoire was listed in allowed_tools but not specifically researched. |
| protocol_clarity | 0.95 | The JSON return schema distinguishes master and composition rights at the field level. Blocking questions are concrete (missing source track identification). |

The 0.945 score is the second-highest among the trigger examples (mix-master-critique scores 0.958). The high constraint preservation score reflects the prompt's unusually strict no-legal-advice boundary, which was research-verified and explicitly encoded at three levels: scope, methodology note, and constraints section.

---

## Interesting Observations

**The estate problem.** Rights ownership for catalog recordings from the 1960s–1980s is notoriously unstable. Labels were acquired, sold, and merged repeatedly. Artists died and their estates took over master control. Publishers were acquired by the Big Three publishing companies. The prompt explicitly addresses this: "Do not ignore catalog acquisitions. A label that owned a master in 1975 may no longer control it; verify current ownership." The methodology step on master rights identification includes an acquisition history check — a detail that only emerges from domain research.

**The "no fair use for commercial sampling" constraint.** A common misunderstanding among music producers is that sampling a short clip (the "4-bar rule" or "2-second rule") is protected by fair use. It is not. U.S. courts have consistently held that commercial sampling without clearance is infringement regardless of length. The prompt does not make legal pronouncements about this, but the constraints section prevents the subagent from suggesting the producer "use a short enough clip to avoid clearance" — a piece of bad advice a naive assistant might offer.

**Interpolation viability assessment as a mandatory step.** Even when a producer asks for clearance research on direct sampling, the prompt mandates an interpolation assessment as a separate deliverable. This is because interpolation (if viable) eliminates the master use license requirement and may dramatically reduce the clearance cost and complexity. A producer who is not aware of the interpolation option might abandon a sample due to a major-label master refusal when the song's melody could have been re-recorded instead.

**The distinction between corroborating evidence and legal proof.** WhoSampled data is explicitly labeled as "corroborating evidence, not legal proof of clearance." Prior sample uses appear on WhoSampled because they were commercially released, not because they were verified as properly cleared — some tracks use samples that were never officially licensed and the rights holders simply did not pursue legal action. The prompt's evidence standards require the subagent to label this limitation explicitly rather than presenting WhoSampled precedent as equivalent to confirmed clearance.
