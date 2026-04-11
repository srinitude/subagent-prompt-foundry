# dependency-scanner — Example README

## Overview

This example demonstrates the `subagent-prompt-foundry` skill applied to a DevSecOps domain: a CI/CD pipeline that needs a specialized subagent to scan software dependency manifests for publicly disclosed vulnerabilities. The result is a reusable system prompt that any CI pipeline can delegate to without encoding vulnerability-scanning logic into the pipeline itself.

---

## Domain: DevSecOps and Software Composition Analysis

Software Composition Analysis (SCA) is the practice of identifying open-source components in a codebase and checking those components against databases of known vulnerabilities. The discipline sits at the intersection of security engineering and DevOps, and is typically the first automated gate before code reaches staging or production.

The primary authoritative sources for vulnerability data are:

- **NVD (National Vulnerability Database)** — operated by NIST. The NVD provides the official repository of CVE (Common Vulnerabilities and Exposures) records, each scored using the CVSS (Common Vulnerability Scoring System). As of 2024, the NVD has adopted CVSS v4.0 alongside v3.1, though v3.1 remains the dominant scoring version in production tooling.
- **CVE / CVSS** — CVE identifiers (e.g., CVE-2021-44228) are assigned by CVE Numbering Authorities (CNAs). CVSS base scores represent the inherent severity of a vulnerability independent of the environment: CRITICAL ≥ 9.0, HIGH 7.0–8.9, MEDIUM 4.0–6.9, LOW 0.1–3.9. CVSS v4.0 introduced a restructured scoring model with new metric groups (Base, Threat, Environmental, Supplemental) but the four-tier severity map is preserved.
- **OSV (Open Source Vulnerabilities)** — the OpenSSF's machine-readable vulnerability format at osv.dev. OSV normalizes vulnerability records across ecosystems (npm, PyPI, Go, Maven, RubyGems, Hex, etc.) and is particularly valuable for resolving affected version ranges for packages that NVD's CPE-based model covers imprecisely.
- **OWASP Dependency-Check** — an open-source SCA tool that identifies CPE identifiers for project dependencies and maps them to NVD CVEs. It supports suppression lists (XML format) to exclude known false positives from repeated reports.
- **SBOM standards** — Software Bills of Materials describe the full component graph of a software artifact. The two dominant formats are CycloneDX (OWASP-backed, JSON/XML) and SPDX (Linux Foundation, used by government procurement). The prompt explicitly names both as valid input artifacts, meaning the subagent can accept either a raw manifest or a pre-generated SBOM.

### Why this tests the skill well

Dependency scanning is an archetype for subagent delegation because the decision criteria are entirely rule-based: a dependency either has a confirmed CVE in the version range or it does not; the CVSS score either exceeds the threshold or it does not; the pipeline signal is binary (PASS/FAIL). There is no room for interpretation. This makes it an ideal stress test for the skill's ability to produce **deterministic** prompts — the subagent must not use judgment to soften a CRITICAL finding or upgrade a LOW one. The evidence standards section must close every gap a careless subagent might exploit.

The domain also tests **ecosystem awareness**: a Python `requirements.txt`, a Node `package-lock.json`, a Java `pom.xml`, and a Go `go.sum` each require a different resolution path to a CPE or OSV identifier. A prompt that says "scan dependencies" without specifying the resolution methodology for each ecosystem will produce inconsistent results across languages.

---

## Routing Decision

**ACTIVATE.** All four routing-checklist.md criteria are satisfied:

1. The user asked for "a system prompt for a dependency vulnerability scanner subagent that my CI pipeline delegates to" — the deliverable is explicitly a reusable system prompt.
2. The prompt defines a single, scoped subagent (vulnerability scanner) with a concrete role.
3. The user did not want the scan performed — they wanted the infrastructure to delegate the scan repeatedly across builds.
4. A meta-agent that generates vulnerability scanning prompts was not requested.

The invocation phrasing "my CI pipeline delegates to" is a strong trigger signal: it names a parent process (the CI pipeline), it implies repeated reuse, and it implies isolation (the subagent runs outside the pipeline's primary context).

---

## Research Performed

The invocation.md records four research sources:

- **NVD CVE API** (`nvd.nist.gov/developers/vulnerabilities`) — used to understand the NVD's REST API query structure (`/rest/json/cves/2.0?cpeName=...`), CVSS scoring tiers, and the treatment of CNAs vs. NVD-assigned scores (CNAs may assign scores before NVD analysis completes, creating a gap the prompt explicitly handles: "awaiting NVD analysis").
- **OWASP Dependency-Check** — used to understand CPE-based matching, the suppression list format (XML), and the distinction between direct and transitive dependencies.
- **OSV Schema** (`osv.dev`) — used to understand the OSV API's POST-based query interface (`/v1/query`), affected-version range format, and ecosystem naming conventions.
- **OSV-Scanner CI integration** — used to understand practical CI/CD integration patterns, particularly how fail-on-severity thresholds produce machine-parseable exit signals.

This research shaped three concrete decisions in the prompt:
1. The methodology cross-references both NVD and OSV by default (not just one), because neither database is complete without the other for all ecosystems.
2. The `pipeline_signal` field was placed at the top of the summary JSON object specifically so CI systems can parse it with a single field read — a detail learned from examining real CI integration patterns.
3. The `suppressed_findings` field is retained in the output structure (not omitted) even when empty, because OWASP Dependency-Check tooling expects the field to be present for merge operations.

---

## What the Generated Prompt Covers

The prompt's six sections encode distinct safety properties:

**Role** — opens with "You are auditing a software project's dependency manifest for publicly disclosed vulnerabilities." The word "auditing" (not "reviewing" or "helping with") signals a verification posture. The subagent is told explicitly it does not inherit the pipeline's prior steps, logs, or runtime context — enforcing isolation at the role level.

**Scope** — restricts the subagent to CVSS v3.x/v4.0 severity tiers and named authoritative sources. The scope constraint "do not speculate about vulnerabilities not present in the provided database sources" closes the hallucination gap: without this, a naive model might infer a CVE from package behavior descriptions rather than database records.

**Inputs** — the JSON handoff schema includes both the manifest file types (package-lock.json, requirements.txt, go.sum, pom.xml, Gemfile.lock) and the optional SBOM formats (CycloneDX, SPDX). The `allowed_tools` field explicitly lists the NVD API, OSV API, and OWASP Dependency-Check report as the only permitted sources. This prevents the subagent from fetching vulnerability data from informal sources (blog posts, GitHub issues).

**Methodology** — ten ordered steps cover the full resolution pipeline: parse → resolve ecosystem → query NVD/OSV → verify version range → score with CVSS → classify severity → deduplicate → apply suppressions → summarize → flag unresolved. The deduplication step is non-obvious: the same CVE can apply to multiple packages (a transitive vulnerability in a shared library), and without explicit deduplication logic the report becomes unreadable. The suppression step instructs the subagent to mark suppressed findings as SUPPRESSED (not omit them), preserving audit trail integrity.

**Output** — the JSON schema is fully specified: summary counts by severity tier, per-finding detail (package, version, CVE ID, CVSS score, severity, fixed version, remediation, source URLs), an unresolved_dependencies array, and a suppressed_findings array. The `pipeline_signal: "PASS | FAIL"` field is the machine-readable gate. The prompt explicitly states: "every response must include `pipeline_signal`" — even when no vulnerabilities are found the field must be present (with value PASS).

**Constraints** — the prohibitions section closes seven specific failure modes: fabricating CVE IDs, treating a popular package as safe, trusting OWASP output over NVD version-range verification, omitting the unresolved field, skipping the pipeline signal, softening severity, and acting as a generic advisor rather than a scanner.

---

## Determinism Score: 0.95

The four metrics:

| Dimension | Score | Interpretation |
|-----------|-------|---------------|
| structure_stability | 0.95 | The same vulnerability scan request will always produce the same Role/Scope/Inputs/Task/Methodology/Output layout. |
| constraint_preservation | 0.95 | All user constraints (source restrictions, CVSS tiers, pipeline signal requirement) are preserved verbatim. |
| research_completeness | 0.92 | Four authoritative sources informed the prompt. One minor gap: CISA KEV (Known Exploited Vulnerabilities) catalog is referenced in the evidence standards but was not explicitly listed in the invocation's research log. |
| protocol_clarity | 0.98 | The highest score across all six examples. The parent↔subagent JSON schema is fully specified, field-level, with no ambiguous fields. |

A score of 0.95 means this prompt is highly stable: a different agent running the same invocation against the same domain research would produce a structurally identical prompt. The slight gap from 1.0 reflects the CISA KEV gap noted above, and the fact that the v3.1 vs. v4.0 CVSS precedence is stated as a preference ("prefer v3.1") rather than a hard rule — leaving minor variation room.

---

## Interesting Observations

**The CVSS version preference problem.** NVD is mid-transition from CVSS v3.1 to v4.0. Many tools and organizations have not updated their alerting thresholds. The prompt handles this by preferring v3.1 where available, falling back to v4.0, and flagging CNA-provided scores (which appear before NVD analysis completes). This three-tier precedence is unusual and reflects a real operational pain point: a CI pipeline configured to fail on CVSS ≥ 7.0 using v3.1 scores may behave differently from one using v4.0 scores for the same CVE.

**The suppression list subtlety.** The OWASP Dependency-Check suppression list format (XML) is a project-level override file that team members add to acknowledge known false positives. If the subagent omits suppressed findings entirely, the CI audit trail loses evidence that a vulnerability was seen and deliberately waived. The prompt mandates marking suppressed findings as SUPPRESSED — a detail that only emerges from reading actual SCA tool documentation rather than summaries.

**Transitive dependencies are the hard problem.** Most manifest files list direct dependencies; the transitive graph (what those dependencies depend on) is where most real vulnerabilities live. The prompt explicitly covers direct and transitive dependencies and requires resolving both. For ecosystems like npm (where `package-lock.json` includes the full transitive tree) this is straightforward; for ecosystems like Python (where `requirements.txt` typically lists only direct dependencies) it requires more inference, which the prompt flags via the `unresolved_dependencies` field.
