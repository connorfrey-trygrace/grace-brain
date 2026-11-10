---
date: 2026-08-18
tier: 2
governs:
  - "Workflows/actions-index.py"
  - "[[Workflows/Open-Actions-Tracker]]"
---

# `blocked_by: "none"` was read as blocked, shielding two P1s from the neglect sweep

**Found by the 8/18 standalone sweep; fixed the same run at Connor's instruction.**

`load()` passed `blocked_by` through verbatim and every downstream check tested it for truthiness. The literal string `"none"` is truthy, so **two notes that explicitly say they are not blocked printed as `blocked`**:

- `Connor - Boot camp relaunch` (P1)
- `Connor - Identify Sunday night host/MC (boot camp alumni pool)` (P1)

**Why it mattered rather than being cosmetic:** Step 3 of the sweep skips blocked items, on the sound reasoning that neglect can't be attributed to an item that is waiting on something else. So the bug **shielded genuinely actionable P1 items from the exact sweep that exists to catch them** — a silent false negative, the kind nothing downstream reports as an error. It had been true for as long as those two notes carried the string.

**Fix:** normalized at load, so every view inherits it rather than each call site re-deriving the test:

```python
NOT_BLOCKED = {"", "-", "n/a", "na", "no", "none", "nothing", "nobody", "null", "false"}

def normalize_blocker(v):
    return "" if str(v).strip().strip('"\'').lower() in NOT_BLOCKED else v
```

**Measured:** items printing as `blocked` went **8 → 6**; the two P1s above are the difference. The six genuine blocks (PCO roster chain, Q&A link, custodian, greeters, ushers, name-tag station) are unchanged.

Both affected notes had their `blocked_by: "none"` rewritten to `""` as well, so the vault stops carrying a value that means its own opposite. **Same class as the two 8/17 defects** ([[Changelog/2026-08-17-actions-index-utc-date]], [[Changelog/2026-08-17-timezone-marker-defect]]): the instrument was wrong, and the fix belongs in code where it can be measured, not in procedure text.
