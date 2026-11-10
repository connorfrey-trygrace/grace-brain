#!/usr/bin/env python3
"""Measure token usage for one refresh run from the local Claude Code session log.

WHY THIS EXISTS (2026-09-02). Connor asked whether refresh runs are tracked for time
*and* tokens. Elapsed wall-clock already is (`stamp.py log`, `elapsed Xm` on every run
log line). Tokens were not. This closes that gap using a source that already exists and
needs no setup: Claude Code writes a full `usage` block (input/output/cache tokens,
model, timestamp) into the session's own JSONL transcript at
`~/.claude/projects/<project-slug>/<session-id>.jsonl` for every assistant turn. No API
key, no connector, no admin access — it's on disk already.

Two numbers are reported, and they answer different questions:

  - **Total tokens this run** — sum of (input + cache-write + cache-read + output)
    across every turn in the window. This is total token *traffic*, not context size —
    it counts the same conversation being re-sent (as cache reads) on every turn, which
    is expected and not a bug.
  - **Peak context usage** — the single largest (input + cache-write + cache-read) on
    any *one* turn in the window, divided by that model's context-window limit. This is
    "how full did the conversation get," a snapshot, not a sum. Reported per model,
    because a run can span a model switch (it did on 2026-09-02: opus-5 -> sonnet-5
    mid-run) and each model's window is tracked independently.

WHAT THIS DOES NOT MEASURE. Only Claude Code sessions on this machine — a session run
from another device, or the raw API, is invisible to it. And every number in the
context-window table below (CONTEXT_WINDOWS) is an unverified guess, not pulled from
current docs — this script has no way to look that up. When an observed peak exceeds
its model's table entry, that's proof the guess is too low (a completed turn cannot
exceed the real window), and the line says so plainly instead of printing a false-
precision percentage. This already happened once, for claude-sonnet-5, on the day this
script was written — see the table comment.

  python3 "Workflows/usage-report.py" --session-id <uuid> --since <unix_ts> --until <unix_ts>

`--since`/`--until` are the same `date '+%s'` epoch stamps the refresh already takes at
its phase boundaries — reuse them, don't take new ones. `--session-id` is not guessed
(picking "the newest .jsonl in the folder" breaks the moment two Claude Code windows are
open on the same vault at once) — the calling agent always knows its own session id, so
it is a required argument, not a default.

Prints one log-ready line and nothing else, e.g.:
  tokens 187k total (in 61k, cache-write 45k, cache-read 74k, out 7k) | peak context 58k/1.0M (6%) on claude-sonnet-5 | OK
"""

import argparse, glob, json, os, sys
from datetime import datetime

# Every value here is an unverified guess (see docstring). 200k is the long-standing
# Claude default and the starting assumption for a model with no better evidence.
CONTEXT_WINDOWS = {
    "claude-opus-5": 200_000,
    # 2026-09-02: raised 200k -> 1M the day this script shipped, after this same
    # session's own transcript showed a 281k-token single turn on claude-sonnet-5 —
    # proof 200k was wrong. 1M is the standard long-context tier name, chosen as the
    # next plausible size, NOT confirmed against docs. Replace with a real number
    # when convenient; until then this is a corrected guess, not a verified one.
    "claude-sonnet-5": 1_000_000,
    # 2026-10-26: added after a 245k-token turn on claude-opus-5-5 overflowed the 200k
    # default. 1M is the same corrected-guess tier as sonnet-5 above, not verified.
    "claude-opus-5-5": 1_000_000,
    "claude-haiku-4-5-20251001": 200_000,
}
DEFAULT_CONTEXT_WINDOW = 200_000  # fallback for a model name not in the table at all


def find_session_file(session_id):
    # Session ids are uuids (unique for all practical purposes), and Claude Code's
    # project-directory slugification isn't a clean, documented function of the vault
    # path (spaces, punctuation etc. don't just become "-" the way "/" does) — a
    # hand-reconstructed slug is a guess that can silently point at the wrong file.
    # Globbing on the session id directly needs no guess and can't be stale.
    hits = glob.glob(os.path.join(os.path.expanduser("~"), ".claude", "projects", "*", "%s.jsonl" % session_id))
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit("error: no session file found for %s under ~/.claude/projects/*/" % session_id)
    sys.exit("error: %d ambiguous matches for session %s: %s" % (len(hits), session_id, ", ".join(hits)))


def iso_to_epoch(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def human(n):
    if n >= 1_000_000:
        return "%.1fM" % (n / 1_000_000)
    if n >= 1_000:
        return "%dk" % round(n / 1_000)
    return str(n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session-id", required=True, help="this session's uuid, e.g. from the scratchpad path")
    ap.add_argument("--since", type=float, required=True, help="unix epoch seconds, inclusive")
    ap.add_argument("--until", type=float, required=True, help="unix epoch seconds, inclusive")
    a = ap.parse_args()

    path = find_session_file(a.session_id)

    total_in = total_cache_write = total_cache_read = total_out = 0
    peak_by_model = {}  # model -> peak (input + cache-write + cache-read) tokens on any one turn
    turns = 0

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = d.get("message")
            if not isinstance(msg, dict):
                continue
            usage = msg.get("usage")
            ts = d.get("timestamp")
            if not usage or not ts:
                continue
            try:
                epoch = iso_to_epoch(ts)
            except ValueError:
                continue
            if not (a.since <= epoch <= a.until):
                continue

            model = msg.get("model", "unknown")
            in_tok = usage.get("input_tokens", 0)
            cw_tok = usage.get("cache_creation_input_tokens", 0)
            cr_tok = usage.get("cache_read_input_tokens", 0)
            out_tok = usage.get("output_tokens", 0)

            total_in += in_tok
            total_cache_write += cw_tok
            total_cache_read += cr_tok
            total_out += out_tok
            turns += 1

            context_this_turn = in_tok + cw_tok + cr_tok
            if context_this_turn > peak_by_model.get(model, 0):
                peak_by_model[model] = context_this_turn

    if turns == 0:
        print("tokens: no usage-bearing turns found in window | OK (zero-usage run)")
        return

    total = total_in + total_cache_write + total_cache_read + total_out

    peak_parts = []
    disproved_models = set()  # peak > table window: proof the table entry is too low
    for model, peak in sorted(peak_by_model.items(), key=lambda kv: -kv[1]):
        window = CONTEXT_WINDOWS.get(model, DEFAULT_CONTEXT_WINDOW)
        pct = 100 * peak / window
        desc = "%s/%s (%.0f%%) on %s" % (human(peak), human(window), pct, model)
        if peak > window:
            disproved_models.add(model)
            desc += " ⚠️ EXCEEDS TABLE — guess is too low, treat %s as a floor, not a %%" % human(peak)
        peak_parts.append(desc)

    line = "tokens %s total (in %s, cache-write %s, cache-read %s, out %s) | peak context %s | OK" % (
        human(total), human(total_in), human(total_cache_write), human(total_cache_read), human(total_out),
        " + ".join(peak_parts),
    )
    if disproved_models:
        line += (" | fix CONTEXT_WINDOWS in usage-report.py for: %s" % ", ".join(sorted(disproved_models)))
    print(line)


if __name__ == "__main__":
    main()
