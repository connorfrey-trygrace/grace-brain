---
type: changelog
date: 2026-08-20
tier: 1
touches: ["[[Workflows/resolve-phone.py]]", "[[Contacts/Phone-Index]]"]
trigger: "grace-quick-refresh, 2026-08-20 — a live Grace-relevant number was reported PHANTOM"
---

# resolve-phone.py: the PHANTOM verdict was returning false positives (WAL ignored)

## What was wrong

`load_handles()` opened `chat.db` with `immutable=1`:

```python
con = sqlite3.connect("file:%s?immutable=1" % path, uri=True)
```

`immutable=1` tells SQLite the file cannot change and to **skip the `-wal` file entirely**. Recent iMessage traffic sits in the WAL until a checkpoint. So every handle created in the last minutes-to-hours was **absent from the `handle` table as this function read it** — and absence from `handle` is precisely what produces the `⚠️ PHANTOM — no such handle in chat.db` verdict (defect 3, added 2026-07-28).

## Why it mattered more than a wrong label

[[Workflows/text-message-sync]] says PHANTOM → **"do not re-resolve; correct or drop it."** So the defect did not merely mislead a run — it **instructed the run to discard a real, correct, Grace-relevant number.** A number Connor had just started texting was the *most* likely to be new and unresolved, i.e. exactly the population this check was built to protect, and exactly the population it silently condemned.

## The measurement

- **617-460-3994** returned `⚠️ PHANTOM — no such handle in chat.db`.
- Direct query of the same db: **handle 2746 (`+16174603994`) exists; chat 2551 exists.** She is **Victoria Nayiga**, a 4th-service volunteer registrant, first texted by Connor **2026-08-20 12:57 ET** — minutes before the resolver ran.
- She was only identifiable because [[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteer-Signups]] already carried her digits. Without that, the run would have dropped her per the workflow's own instruction.

## The fix

Copy `chat.db` plus `-wal` and `-shm` to a scratch dir and open the **copy read-write**, so SQLite replays the WAL. Scratch dir removed in a `finally`. The `OSError`/`shutil.Error` cases fall back to `return None`, which the existing contract already treats as "chat.db unreachable" rather than "this number is fake" — so a copy failure can never manufacture a PHANTOM either.

**Verified after patching:** `617-460-3994` no longer returns PHANTOM (returns `UNRESOLVED`, which is correct — real handle, no naming source), and `520-679-9644` still resolves normally.

## The lesson, which is a repeat

**This is the same root cause the text-message-sync workflow retired on 2026-08-17** — an immutable read misses the WAL. That correction was applied to the *workflow prose*; the *resolver code* never got it. Identical to the 2026-07-28 defect-2 finding: **a fix documented in one file is not a fix in the code, and it looks identical to a working one until someone measures.** Any future WAL/immutable correction should be applied by grepping the vault for `immutable=1`, not by editing the file where the symptom appeared.

## Related

- [[Contacts/Phone-Index]] — Changelog entry for this fix; 617-460-3994 promoted to **Confirmed**
- [[Workflows/text-message-sync]] — the 2026-08-17 immutable/WAL correction this should have propagated from
