# Invocation

```
/subagent-prompt-foundry Create a system prompt for a dependency vulnerability scanner subagent that my CI pipeline delegates to.
```

## Routing decision

**ACTIVATE** — the user explicitly requests a system prompt for a subagent that a parent process (CI pipeline) delegates to. All four routing-checklist.md criteria are satisfied:

1. The output should be a reusable system prompt ✓
2. The prompt defines a custom subagent (dependency vulnerability scanner) ✓
3. Direct task execution is not the goal ✓
4. A meta-agent prompt is not the goal ✓

## Research performed

- [NVD CVE API](https://nvd.nist.gov/developers/vulnerabilities) — CVSS v3/v4 scoring, severity tiers (CRITICAL/HIGH/MEDIUM/LOW), CPE identifiers
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) — SCA tool that identifies CPE and linked CVE entries
- [OSV Schema](https://osv.dev) — OpenSSF OSV format, machine-readable vulnerability format with affected version ranges
- [OSV-Scanner CI integration](https://docs.kondukto.io/docs/osv) — Docker-based CI/CD workflow, fail-on-severity thresholds
- CVSS v4.0 standard — CRITICAL ≥9.0, HIGH 7.0–8.9, MEDIUM 4.0–6.9, LOW 0.1–3.9
