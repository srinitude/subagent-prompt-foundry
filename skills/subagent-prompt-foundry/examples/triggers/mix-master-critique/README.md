# mix-master-critique — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to audio engineering: a parent DAW (Digital Audio Workstation) assistant delegates mix and mastering critique to a specialist subagent. The subagent analyzes a stereo bounce against a reference track across five technical dimensions — frequency balance, dynamic range, stereo width, integrated loudness (LUFS), and true peak — and returns actionable recommendations with specific Hz and dB values. This example has the highest determinism score among all six trigger examples (0.958), reflecting the unusual precision of the domain's quantitative standards.

---

## Domain: Audio Mixing, Mastering, and Loudness Measurement

Audio engineering for commercial release involves meeting platform-specific technical standards while achieving subjective goals (clarity, punch, width, warmth). The subagent's role is the technical half: verify compliance with delivery standards and identify specific frequency/dynamics issues relative to a reference track.

### LUFS and Platform Loudness Targets

LUFS (Loudness Units relative to Full Scale) is the primary loudness measurement unit for streaming and broadcast audio. LUFS is defined by the ITU-R BS.1770-4 standard (International Telecommunication Union, Radiocommunication Sector), which specifies a K-weighting filter applied before RMS measurement. K-weighting roughly models the frequency sensitivity of human hearing by attenuating low frequencies and applying a high-shelf boost above 2 kHz.

**Integrated LUFS** measures average loudness over the full duration of a track, which is the value streaming platforms use for normalization decisions.

**Short-term LUFS** measures loudness over a 3-second sliding window.

**Momentary LUFS** measures loudness over a 400ms sliding window.

**LRA (Loudness Range)** measures the difference between loud and quiet sections of a track, indicating dynamic contrast.

**True Peak (dBTP)** measures inter-sample peaks — transient spikes that occur between sample points and can cause distortion after lossy codec encoding. The standard delivery ceiling is −1 dBTP.

Platform loudness targets (integrated LUFS):

| Platform | Target | Source |
|----------|--------|--------|
| Spotify | −14 LUFS | Spotify loudness normalization specification |
| Apple Music | −16 LUFS | Apple Digital Masters specification |
| YouTube | −14 LUFS | YouTube Content ID normalization |
| Tidal | −14 LUFS | Tidal MQA and standard delivery spec |
| AES Streaming recommendation | −16 to −20 LUFS | AES AESTD1008 |
| Broadcast (EBU R128) | −23 LUFS | EBU (European Broadcasting Union) |

Platforms normalize down (attenuate) tracks that exceed their target but do not normalize up tracks that fall below. A track mastered at −8 LUFS integrated will be attenuated by 6 LUFS on Spotify, but its dynamic range will be artificially compressed by the normalization algorithm, often making it sound worse than if it had been mastered at −14 LUFS.

### K-System Metering

The K-system was developed by mastering engineer Bob Katz as a reference metering standard that correlates to a calibrated monitoring level (83 dBSPL at 0 dB RMS). Three K-scales:

- **K-20**: Film and classical music. RMS anchor at −20 dBFS (20 dB of headroom above the anchor). Preserves wide dynamic range for orchestral dynamics and film scoring.
- **K-14**: Pop, rock, and most commercial music. RMS anchor at −14 dBFS (14 dB of headroom). Balances loudness with dynamic range.
- **K-12**: Broadcast. RMS anchor at −12 dBFS. Tighter dynamic window for broadcast normalization.

The K-system is not a delivery standard but a monitoring and calibration tool. The prompt uses K-system references to help the subagent contextualize whether a track's dynamic range is appropriate for its genre, independent of the absolute LUFS reading.

### Fletcher-Munson Equal Loudness Contours

The Fletcher-Munson curves (ISO 226:2003 update: equal loudness contours) describe how the human ear's sensitivity varies across frequencies at different listening levels. Key properties:

- **2–5 kHz is the most sensitive frequency range** at moderate listening levels. The ear is approximately 10 dB more sensitive here than at 1 kHz. Boosts in this range are highly audible — even 1–2 dB can noticeably increase harshness or listening fatigue.
- **100 Hz requires approximately 10 dB more SPL than 1 kHz to sound equally loud** at moderate listening levels (83 dBSPL reference). This is why mixes that sound bass-heavy at low volume can sound balanced or even bass-light at a louder reference level.
- At very loud levels (95+ dBSPL), the equal loudness contours flatten significantly, meaning frequency perception becomes more uniform.

The practical consequence for mix critique: a subagent should not recommend a bass boost simply because the bass sounds thin at a given monitoring level, without first assessing what monitoring level the producer is using. This nuance is encoded in the prompt's Fletcher-Munson compensation note: "if the mix sounds bass-light at 83 dBSPL reference but correct at lower volumes, note this as a monitoring-level calibration artifact, not a mix error."

### Crest Factor and Stereo Correlation

**Crest factor** (peak-to-average ratio) measures transient preservation. A crest factor that is significantly lower than a reference track's indicates over-compression: the limiter has crushed the attack transients of kick drums and snares, making the mix sound "flat" even at acceptable LUFS levels.

**Stereo correlation** is measured on a scale from +1 to −1:
- +1: fully mono (left and right channels are identical).
- 0: channels are completely independent (stereo).
- −1: channels are phase-inverted (cancels to silence in mono).

A correlation below +0.2 is a mono-compatibility risk: the track will sound significantly different (often thinner or with cancellation artifacts) on mono speakers, car audio systems, and many club PA systems. Sub-bass (below 100 Hz) should always be mono or near-mono to prevent phase cancellation in bass-frequency ranges.

### Why this tests the skill well

The mix-master-critique domain is the hardest of the six examples to make deterministic because the input (audio file) requires actual signal processing to analyze. The prompt must specify exactly what measurements the subagent needs, in what units, compared to what reference, and what to do if the audio cannot be analyzed directly (text-only model context). This is a constraint no other example in this set faces — all other subagents receive text or structured data, not audio files.

The domain also tests the skill's ability to **require specific quantitative language** rather than vague qualitative descriptions. An audio critique that says "the low end is muddy" is not actionable. A critique that says "mud accumulation at 200–250 Hz, approximately +3 dB relative to reference, recommend a high-Q peak cut at 220 Hz with Q=2.0, gain −3 dB" is actionable. The prompt encodes this quantitative requirement as a constraint: "Do not use vague language such as 'muddy,' 'harsh,' or 'thin' without specifying the frequency range (Hz) and approximate magnitude (dB)."

---

## Routing Decision

**ACTIVATE.** The invocation states: "Design a production-grade subagent prompt for mix/master critique. A producer's DAW assistant delegates with a stereo bounce and reference track. Analyze frequency balance, dynamic range, stereo width, loudness (LUFS), and return actionable EQ/compression suggestions with specific frequency ranges and dB values."

- "Production-grade subagent prompt" — both "production-grade" and "subagent prompt" are explicit trigger phrases.
- "A producer's DAW assistant delegates" — parent delegation named.
- The user specifies the five analysis dimensions and requires specific Hz/dB values — they want the prompt infrastructure, not the critique itself.

All four routing-checklist.md criteria pass cleanly. The phrase "production-grade" is a strong signal: it implies the prompt will be reused across many mixes, not used once.

---

## Research Performed

The invocation.md records five research sources:

- **iZotope — Mastering for Streaming Platforms** — confirmed the LUFS targets for Spotify (−14), Apple Music (−16), and the AES AESTD1008 recommendation (−16 to −20). iZotope is an industry-leading audio software company whose documentation carries strong authority.
- **Youlean — Loudness Standards Comparison Table** — provided a comprehensive table of worldwide streaming and broadcast LUFS targets, useful for the `platform_target` field in the output schema.
- **K-system — MeterPlugs** — confirmed the K-12/K-14/K-20 definitions, the 83 dBSPL reference level, and the RMS anchor positions.
- **iZotope — Fletcher-Munson Curves** — confirmed the peak sensitivity at 2–5 kHz, the 10 dB bass sensitivity gap vs. midrange at moderate levels, and the practical implications for low-end management in mixes.
- **RTW — Worldwide Loudness Delivery Standards** — provided additional verification of global streaming targets and broadcast standards.

The research shaped three decisions:
1. The prompt's evidence standards require every LUFS reading to cite ITU-R BS.1770-4, not just report a number.
2. The Fletcher-Munson compensation note in the methodology section addresses the monitoring-level calibration artifact, a nuance that only emerges from studying the psychoacoustic literature.
3. The true peak ceiling (−1 dBTP) is stated as the delivery standard — not just a preference — because codec encoding can amplify inter-sample peaks above 0 dBFS, causing digital clipping in the encoded file even when the unencoded file has no clipping.

---

## What the Generated Prompt Covers

**Methodology** — the most technically specific of all six examples. Six steps:
1. Measure integrated LUFS using ITU-R BS.1770-4, with comparison to platform target.
2. Run FFT spectral analysis across seven frequency bands (sub-bass 20–80 Hz, bass 80–250 Hz, low-mid 250–500 Hz, mid 500 Hz–2 kHz, upper-mid 2–5 kHz, presence 5–8 kHz, air 8–20 kHz), with per-band status (OK/OVER/UNDER) and dB delta.
3. Assess dynamic range via crest factor, LRA, and K-system reference check.
4. Assess stereo width via inter-channel correlation, sub-bass mono content, and mid/side balance.
5. Compare all dimensions against the reference track, computing dB or LUFS deltas for each.
6. Generate top-3 priority recommendations, each with: frequency (Hz), filter type, bandwidth (Q), gain change (dB), expected outcome.

**Output schema** — the JSON output is the most field-dense of all six examples. The loudness object carries six fields; the frequency_balance object carries seven per-band objects each with status, delta_db, and note; the dynamics object carries peak-to-average, transient status, and K-system reference; the stereo_width object carries correlation, mono compatibility, and sub-bass stereo content.

**Constraints** — "Do not use vague language" (with specific prohibited examples: muddy, harsh, thin); no plugin brand recommendations; no arrangement critique; no LUFS/perceived loudness conflation; no omission of true peak measurement; Fletcher-Munson context for low-end recommendations; explicit uncertainty acknowledgment when audio cannot be analyzed directly.

---

## Determinism Score: 0.958

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.95 | The five-dimension analysis structure (loudness, frequency, dynamics, stereo, reference) is stable across any stereo audio critique request. |
| constraint_preservation | 0.97 | The highest constraint score of any dimension across all six examples. The quantitative language requirement (specific Hz and dB), the true peak mandate, and the no-legal-advice equivalents (no plugin brands, no arrangement critique) are all fully preserved. |
| research_completeness | 0.95 | Five authoritative sources consulted, covering LUFS standards, K-system metering, Fletcher-Munson psychoacoustics, and worldwide delivery targets. |
| protocol_clarity | 0.96 | The JSON schema is fully specified with typed fields and units (LUFS, dBTP, Hz, Q, dB). The blocking questions address the two most common missing inputs: reference track and platform. |

The 0.958 composite is the highest score in the test suite. This reflects the domain's unusually strong foundation in quantitative standards: unlike market research (where evidence interpretation has judgment gaps) or D&D (where creative content introduces variability), audio engineering delivery standards are precise and universally measurable. The prompt codifies those standards into constraints, which is straightforward when the standards themselves are unambiguous.

---

## Interesting Observations

**The text-only limitation is architecturally honest.** The mix/master critique subagent requires actual audio analysis — LUFS meters, FFT analyzers, correlation meters. In a text-only model deployment where audio files cannot be processed, the subagent cannot perform real measurements. Rather than papering over this with vague promises to "analyze the audio," the prompt handles it by requiring the subagent to flag the limitation and request meter readings from the parent instead. This is the correct engineering decision: a partially degraded subagent with stated limitations is more useful than a confident one that fabricates measurements.

**True peak is not the same as peak.** A mix can have a peak of −1 dBFS (the waveform never exceeds −1 dBFS in the digital file) and still have a true peak above 0 dBTP after MP3 or AAC encoding. Inter-sample peaks are artifacts of the sample-and-hold reconstruction process; they exceed the nominal amplitude of the digital signal. The −1 dBTP ceiling exists precisely to leave headroom for this codec-induced amplification. A subagent that reports "no clipping" based on digital peak measurement alone may be wrong about the delivered file.

**The 2–5 kHz ear fatigue zone requires special handling.** The upper-mid frequency band (2–5 kHz) is where the ear is most sensitive. Small deviations from reference in this band are highly audible and can make the difference between a mix that sounds clear and one that causes listening fatigue. The prompt specifically flags this zone: "small boosts here are highly audible — flag if the submission is 3+ dB above the reference in this range." This threshold (3 dB) is based on the Fletcher-Munson research: a 3 dB boost in the 2–5 kHz range corresponds to a perceived loudness increase much larger than 3 dB would suggest at other frequencies.

**The crest factor transient test.** The prompt specifies a concrete criterion for detecting over-compression: "if kick and snare transients are more than 6 dB below the reference's transient peak relative to the integrated level, flag over-compression." This 6 dB threshold is not arbitrary — it represents a perceptually significant loss of attack energy that makes drums sound flat. Having a concrete threshold turns subjective transient assessment into an objective comparison.
