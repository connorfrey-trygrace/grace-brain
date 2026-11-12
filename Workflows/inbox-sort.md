# Workflow: Inbox Sort (read mail → Outlook folders)

Run by [[Workflows/grace-quick-refresh]] **Phase 3b**, beside the Open Actions sweep. Moves Connor's **read** Inbox mail into his existing Outlook folders. Connor's calls (2026-11-11): **move automatically, no approval step**; mail that fits no folder **stays in Inbox** and, when a theme repeats, gets a **proposed new folder** in the report.

Touches Outlook only — never the vault, never a sync marker.

## Folder map

Folders are subfolders of Inbox, nested — **the folder pane hides subfolders until expanded, so read the full tree, never the top level.** Built 2026-11-11 from what was already filed in each. Match on what the thread is *about*, not just who sent it. Prefer the most specific subfolder.

| Folder | Path | Goes here |
|---|---|---|
| **4th Service** | Events › 4th Service | Sunday Night general: chair setup/facility for evenings, security, format ideas, cleaning-crew requests for Sunday setup |
| **Scheduling & Volunteers** | …› 4th Service › Scheduling & Volunteers | PCO accepted/confirmed/declined notices for Sunday Night positions, volunteer replies to Connor's sign-up/"extra hands" sends, door codes/who-to-find |
| **Connect Cards** | …› 4th Service › Connect Cards | "<Name> has filled out a … connect card" (YP and other types) |
| **Comms & Promo** | …› 4th Service › Comms & Promo | Heather/marketing threads, QR landing pages, comms requests, photographer/shoot scheduling, event-reminder blasts |
| **Worship & Music** | …› 4th Service › Worship & Music | Setlists (Seth's shared docs), worship leads, baptism music, theme songs, JeanPaul AV/music |
| **Discussion Guides** | …› 4th Service › Discussion Guides | Weekly discussion-guide drafts/finals (Brian, Alexis) |
| **Attendance & Systems** | …› 4th Service › Attendance & Systems | Rock/PCO setup for Sunday Night (groups, tags, auto-welcome), attendance numbers |
| **NYC Recon** | …› 4th Service › NYC Recon | NYC trip receipts (closed — stragglers only) |
| **Boot Camp** | Events › Boot Camp | Bible Bootcamp: John's weekly emails (incl. from "John Slye Jr." via info@), table-leader threads, host scripts, group-join notices |
| **Concerts** | Events › Concerts | Grace concerts: dates, setup, concert volunteer asks, concerts calendar |
| **Volunteers** | Events › Volunteers | Connor *as* a volunteer: PCO requests for kids/greeter slots, "extra hands" asks to him |
| **20260719 World Cup** › **Registrations** | Events › … | World Cup only (event over) |
| **Events** | Events | Event-process mail not tied to one event (comms-request how-to) |
| **Sermon Outlines** | Sermon Outlines | Weekly outlines, outline-thread replies, series updates, testimony scripts for the message |
| **YoPro Ministry** | YoPro Ministry | YP events (Friendsgiving etc.) — **not** connect cards |
| **Announcements** | Admin › Announcements | All-Staff announcements: staffing news, Rock outages/upgrades |
| **Bank** | Admin › Bank | Credit-card coding (Shore Accounting), reimbursements, tool receipts |
| **Facility** | Admin › Facility | Building access codes, room bookings |
| **Procurement** | Admin › Procurement | Vendors, catering, Amazon/Instacart business accounts |
| **Software** | Admin › Software | Tool/account notices: Rock/PCO accounts & permissions, GitHub, Notion, connectors |
| **Staff Meetings** | Admin › Staff Meetings | Staff-meeting notices and recaps |
| **Admin** | Admin | Church-wide staff threads that fit no Admin subfolder (service-time decisions, gift receipts) |

No confident match → **leave it in Inbox.** Two folders fit equally → leave it in Inbox (don't guess).

## Never move

- **Unread** mail — the whole point is that Connor has seen it.
- A **conversation that still holds an unread message** — OWA moves the whole conversation, so the unread one would go with it.
- **Flagged or pinned** mail — Connor is using it as a to-do.
- Mail received **after this run's email-sync window-end** (the `--window-end` Phase 2 stamped) — the next sync hasn't read it yet.
- Calendar invites still awaiting a response.

## Steps

1. **List (connector — cheap).** `outlook_email_search` with `folderName: "Inbox"` only, `limit: 25`, paging by `nextOffset` to the end. Keep `isRead: true` and `receivedDateTime` ≤ window-end. The previews (`subject`, `sender`, `summary`) are enough to classify — **do not fetch full bodies.**
2. **Classify** each kept message against the folder map. Build `{folder: [subject + sender + received]}` plus an **unmatched** list.
3. **Move (Outlook web, Claude in Chrome).** Open `https://outlook.office.com/mail/inbox`. Mechanics proven on the first run (2026-11-11):
   - **Inbox is split Focused / Other.** Sort both tabs. Automated senders (info@ blasts, PCO volunteer mail) often land in Other.
   - The list is virtualized (only ~11 rows mounted). Select by scrolling the list's scroll container and clicking each matching row's `[role=checkbox]` until the reading pane says **"N items selected"**. Check that N matches your count before moving.
   - **2+ selected:** reading-pane **Move** → recent folders are listed; otherwise the menu's folder search box is already focused (zoom to confirm the cursor), type the folder name, click the result. **1 selected:** the message opens instead — use the **ribbon Move** button, then **click into** its "Search for a folder" box before typing.
   - ⚠ Search results include a **`"<name>" (Create new)`** row right under the real folder. Click the plain folder row by position, never the quoted one.
   - Each move shows a toast ("N moved to <Folder>"); read it before the next group.
   - ⛔ **Never type into the message list.** Outlook web's single-key shortcuts delete and archive mail (3 emails were once deleted this way). Type only into a search box you've confirmed has focus.
   - After a move, Outlook opens the next message in the reading pane, which can mark an unread one read. Re-check that unread mail is still unread.
4. **Verify.** Re-run step 1's Inbox listing. Every message you moved must be gone from Inbox. Anything still there: retry once, then list it in the report as **not moved**.
5. **Propose folders.** If **3 or more** unmatched read emails share a clear theme, propose one folder for them (name + where it would sit + the emails it would take). Don't create folders — proposals only.

## Report (one block in Part 2 of the refresh report)

- `Sorted N read emails — 4th Service 4, Admin 3, Boot Camp 2…` (folders with 0 left out).
- **Left in Inbox:** count only, unless a folder is being proposed.
- **Proposed folder:** `"<Name>" under <parent> — would take: <subject>, <subject>, <subject>`. On Connor's yes: create it, move those emails, and add a row to the folder map above.
- **Not moved** (verification failures), if any.

Add `sorted N` to the refresh line in [[Logs/refresh-run-log]]. Nothing else is logged.

## Changelog

New changes get their own dated file in [[Changelog/README|/Changelog]]. **Not read on a normal run.**
