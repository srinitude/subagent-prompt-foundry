# Issues Log

Issues, ambiguities, and observations encountered during the full test suite run. Logged per SKILL.md instruction: "Log any issues with the skill instructions to examples/ISSUES.md."

---

## ISSUE-001: `score_determinism.py` does not validate dimension ranges

**Status:** RESOLVED  
**Observed during:** Dependency-scanner scoring  
**Description:** The `score_determinism.py` script accepts any float values in the JSON and silently clamps them to [0.0, 1.0] via the `clamp()` function. However, it does not warn the user when a value is out of range and gets clamped. If a practitioner accidentally enters `9.5` instead of `0.95`, the script will silently use `1.0` and return a misleadingly high score with no error message.  
**Suggested fix:** Add a validation warning: `if value != clamp(value): print(f"WARNING: {key} value {value} was clamped to {clamp(value)}", file=sys.stderr)`  
**Impact on test suite:** None — all values in this test suite are in the valid range.

**Resolution:** Added `key: str = ""` parameter to `clamp()` and a conditional `print()` to stderr when clamping occurs. All four callers in `score_determinism()` now pass the dimension name as the key. Fixed in `scripts/score_determinism.py`.

---

## ISSUE-002: `validate_prompt_shape.py` uses plain string matching (case-sensitive)

**Status:** RESOLVED  
**Observed during:** All six prompt drafts  
**Description:** The validator checks for exact section header strings: `"Role"`, `"Scope"`, `"Inputs"`, `"Task"`, `"Methodology"`, `"Output"`. It does not match variations like `"## Role"`, `"# Role"`, `"ROLE"`, or `"Roles"`. A prompt that uses `"## Scope:"` (with a colon) instead of just `"Scope"` will still pass because `"Scope"` is a substring of `"## Scope:"`. However, a prompt that writes `"Input"` (singular) instead of `"Inputs"` will silently fail.  
**Suggested fix:** Normalize both the section header list and the file text to lowercase before matching, or use a regex pattern like `r'#{1,3}\s*inputs?\s*'` to catch singular/plural variants.  
**Impact on test suite:** None — all six prompts use the exact expected strings. This became clear during drafting when care was needed to write `Inputs` (not `Input`).

**Resolution:** Replaced `REQUIRED_SECTIONS` string list with regex patterns (`r"roles?"`, `r"scopes?"`, etc.) and replaced the plain `in` check with `re.search(pattern, text, re.IGNORECASE)`. Added `import re` to script imports. Fixed in `scripts/validate_prompt_shape.py`.

---

## ISSUE-003: SKILL.md step 17 (`diff_prompt_versions.py`) has no applicable context for first-run examples

**Status:** RESOLVED  
**Observed during:** All six first-run trigger examples  
**Description:** SKILL.md step 17 states: "Diff against any prior draft with `scripts/diff_prompt_versions.py` when applicable." For a new prompt with no prior version, this step is not applicable. However, the SKILL.md note also says "When a prior draft exists, always run `scripts/diff_prompt_versions.py`. Regression from one version to the next is a common and silent failure mode." This creates slight ambiguity: does step 17 always run (even against /dev/null) or only when a v1 file exists?  
**Resolution applied in this test suite:** Step 17 was treated as "not applicable" for all six new prompts since no prior drafts existed. The skip was intentional and noted.  
**Suggested clarification in SKILL.md:** Add to step 17: "Skip this step if no prior draft exists; note the skip explicitly in your output."

**Resolution:** Changed SKILL.md step 17 from "Diff against any prior draft with `scripts/diff_prompt_versions.py` when applicable" to "Diff against any prior draft with `scripts/diff_prompt_versions.py`. Skip this step if no prior draft exists."

---

## ISSUE-004: The routing-checklist.md does not distinguish between "one-off subagent prompt" and "reusable subagent prompt" at the checklist level

**Status:** RESOLVED  
**Observed during:** Deceptive anti-trigger case 1 ("Give me a system prompt for a code auditor")  
**Description:** The `assets/routing-checklist.md` first criterion is "the output should be a reusable system prompt." However, a request like "Give me a system prompt for a code auditor" is borderline — it mentions "system prompt" but lacks explicit reuse intent. The checklist does not provide a test for inferring reuse intent from context. The `references/ROUTING_MATRIX.md` handles this case explicitly: "User wants a one-off prompt for a single agent and reuse is not important → Usually no." However, the checklist itself is silent on this nuance, so a practitioner reading only the checklist would not know how to rule.  
**Suggested fix:** Add a note to the checklist: "Reuse intent may be inferred from language like 'reusable,' 'production-grade,' 'delegate to,' 'my [parent/main] agent,' or 'across projects.' Absent these signals, consult `references/ROUTING_MATRIX.md`."

**Resolution:** Added reuse intent note to `assets/routing-checklist.md` after the "Do not activate if" block: "Reuse intent is signaled by words like 'reusable', 'production-grade', 'delegate to', 'my parent/main agent', or 'across projects'. If none of these signals are present, consult `references/ROUTING_MATRIX.md` before activating."

---

## ISSUE-005: Audio analysis limitation for mix-master-critique subagent

**Status:** By-design constraint, but worth documenting  
**Observed during:** mix-master-critique prompt drafting  
**Description:** The mix-master-critique subagent prompt requires actual audio analysis (LUFS meters, spectral analyzers, correlation meters). In a text-only agent context where the audio file is not parseable, the subagent cannot perform real measurements. The prompt handles this via the constraints section: "If the audio file cannot be analyzed directly (text-only context), the subagent must flag this limitation and request a meter readout from the parent instead of guessing values." This is correct behavior but means the subagent is partially degraded in text-only deployments.  
**Impact on test suite:** None — this is an expected constraint documented in the prompt itself.  
**Suggested enhancement:** The parent DAW assistant should include pre-computed LUFS/peak readings in the handoff artifacts for text-only deployments of this subagent.

---

## ISSUE-006: No examples directory existed before this test run

**Status:** Resolved  
**Observed during:** Directory creation step  
**Description:** The `examples/` directory and all subdirectories (`triggers/`, `anti-triggers/`) did not exist in the skill repository. They were created as the first step of this test suite. The SKILL.md and the test task both implied these directories should be created by the test run.  
**Resolution:** `mkdir -p` was used to create all required directories before writing any files.  
**Impact on test suite:** None.
