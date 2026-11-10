---
title: "4th Service Volunteering — Rock Form Record"
event: "Sunday Night Service"
date: 2026-07-24
status: built-and-live (not yet promoted)
tags: [event, rock, form, volunteers]
source: "Built directly in Rock per [[Workflows/rock-event-request]] format; modeled on the World Cup registration"
participants:
  - "[[People/Connor Frey]]"
---

# 🙋 4th Service Volunteering — Rock Form Record

Built directly in Rock on 2026-07-24 at Connor's request. **This is not a request to Kay** — the template and instance were created in Rock admin, not via the Event Registration Request form.

## Live link

**https://trygrace.org/registration?RegistrationInstanceId=542**

⚠️ Registration window is **open** (7/24/2026 → 12/31/2026) and the form is publicly reachable by anyone with the link, but it has not been posted anywhere. Nothing goes out until Connor clears it.

## What was created

| Object | Value |
|--------|-------|
| Registration Template | **4th Service Volunteering** — ID **120**, category **General** |
| Group Type | **Services** (Connor's deliberate choice — not the usual "Event Registrations - already belongs"). Group Member Role: Member. |
| Registration Instance | **4th Service Volunteering** — ID **542** |
| Registration Starts | 7/24/2026 |
| Registration Ends | **(blank — no end date)**. The 12/31/2026 I originally entered didn't persist; leaving it open is arguably right for a standing interest form. |
| Cost | $0.00 (free) |
| Account | Event Registration |
| Max Attendees | none (uncapped) |
| Wait List | off |
| Contact | **Connor Frey** · connor.frey@trygrace.org · (973) 699-0180 |
| Admin URL | https://trygrace.rockcloud.com/RegistrationInstance/542 |

## Why a new template

The World Cup Viewing Party ran as an instance on the shared **General Men's Event** template (ID 12) — and its event-specific volunteer questions ("setup at 1:00 pm," "cleanup until 6pm," plus a smoked-meat and a cornhole question) are **still bolted onto that shared template**, where every future Men's Event inherits them. Connor asked for a clean template so Men's Events and Boot Camp are untouched.

Method: duplicated the General Men's Event template (to inherit its format/settings), renamed it, then stripped all five World Cup/Men's-specific registrant attributes and added the 4th-service questions. **The original General Men's Event and Boot Camp templates were not modified.**

## Form fields (Default Form)

Matches the World Cup format: four Person Fields for contact info, then registrant attributes for the questions.

| # | Field | Source | Type | Values |
|---|-------|--------|------|--------|
| 1 | First Name | Person Field | — | — |
| 2 | Last Name | Person Field | — | — |
| 3 | Email | Person Field | — | — |
| 4 | Mobile Phone | Person Field | — | — |
| 5 | Which areas are you interested in serving in at the Sunday Night Service? **(required)** | Registrant Attribute | Multi-Select | **Connor's trimmed list, 2026-07-24:** MC/Host · Worship Team · Tech/Slides · Greeter/Welcome · Usher · Setup (before service) · Teardown (after service) · Not sure yet — help me find a fit *(my longer 14-option draft — separate Audio/Lights/ProPresenter, Communion, Prayer Team, Meet Grace, Welcome & Language Desk — was consolidated by Connor)* |
| 6 | How often are you hoping to serve? | Registrant Attribute | Single-Select | Every week · Twice a month · Once a month · Occasionally / as needed · Not sure yet |
| 7 | Do you already serve on a Sunday morning team? | Registrant Attribute | Single-Select | Yes — currently serving · No — this would be my first team · I used to serve and want to get back in |
| 8 | What's your age range? | Registrant Attribute | Single-Select | 18–24 · 25–34 · 35–44 · 45+ |
| 9 | Anything else you'd like us to know, or questions you have? | Registrant Attribute | Memo | free text |

All five registrant attributes have **Show in Grid** on, so answers appear in the Registrants grid the same way the World Cup setup/cleanup answers did.

The serving-area list is drawn from the Night column of [[Workflows/Service-Structure]] — every role marked ✅ or ◐ for night, minus the ones that aren't volunteer-recruitable (Message, Custodian, Police Officers).

Screenshot of the live form: `4th-Service-Volunteering-Rock-Form.jpg`

## Open items for Connor

1. **Registration end date** — 12/31/2026 is a placeholder. If this is a standing interest form, push it out; if it's a launch push, tie it to 9/20.
2. ~~**Registration Instructions** are blank.~~ **Done by Connor 2026-07-24:** *"Most positions will have a call time of 5:30PM for the 6PM service."*
3. ~~**Nothing is required** except the four contact fields.~~ **Done 2026-07-24:** the serving-areas question is now Required. The other three (frequency, current team, age range) and the free-text box remain optional by design.
4. ~~**Contact person + phone are blank on instance 542.**~~ **Done 2026-07-24:** Contact = Connor Frey, phone (973) 699-0180 (Connor had already added the phone; I added the person record). This fixed two renders at once — the success page's *"please contact  at … or ."* dangling line, **and** the confirmation email's **From Name**, which is `{{ ContactPersonAlias.Person.FullName }}` and was resolving to an empty string. Emails would have gone out with a blank sender name.
5. **Confirmation Email — reviewed, no Men's-Event wording found.** Details below. One content gap remains: **Additional Confirmation Details is blank**, so the email tells a new volunteer nothing about what happens next. That's the remaining substantive improvement.
6. ⚠️ **Duplicate Connor Frey records in Rock.** The person picker returns two: one *Prospect* (freycncr@gmail.com) and one *Attendee* (connor.frey@trygrace.org, spouse Skylar) — both carrying (973) 699-0180. I selected the Attendee/work-email record. Worth merging, unrelated to this form.
6. **Comms Request** — if this link is going on the website or in a bulletin, it needs a Comms Request per [[Workflows/rock-event-request]]. Rock first (done), Comms second with the link in the Registration field.
6. **Consider retiring the World Cup questions** from the General Men's Event template (ID 12) — they'll show on the next Men's Event registration otherwise. Not touched here.

## Registration Confirmation Text (on-screen success page)

Rock's stock default Liquid, unmodified. With this form's settings, most of it never renders:

| Block | Renders? | Why |
|-------|----------|-----|
| "You have successfully registered the following…" + name list | ✅ | the only substantive block that fires |
| Per-registrant cost | ❌ | gated on `registrant.Cost > 0`; cost is $0 |
| Fees / Additional Options | ❌ | no fees defined |
| Waiting list | ❌ | wait list disabled |
| Total Cost / payments / balance | ❌ | gated on `Registration.TotalCost > 0` |
| "A confirmation email has been sent to…" + contact line | ✅ | ⚠️ see defect in open item 4 |

Two latent bugs in Rock's stock Liquid, both in blocks that won't fire here — worth knowing if the form ever takes a fee or a wait list:
- the waiting-list paragraph pluralizes on `registrantCount` instead of `waitListCount`
- the fee term pluralizes on `registrantCount` instead of `feeCount`

## Print collateral

- **`4th-Service-Volunteering-Sign.pdf`** — Grace-branded **8.5×11 portrait** sign, built 2026-07-26 for Sunday 7/26. Deliberately minimal per Connor: wordmark, **"Sunday Night Service Volunteering"** set over three lines at 83 pt, and a 5" QR, centered stack. Nothing else — no body copy, no serving-area list, no contact line, no "scan to sign up" prompt. Thin teal (#44979D) bands top and bottom, charcoal #3D3D3D type. Print on white; no bleed needed.
  - *Design history: v1 was portrait carrying the full pitch — headline, serving areas, call time, 1 Peter 4:10, contact block. Connor cut it ("way too much"). v2 stripped it to logo/title/QR in landscape. v3 lengthened the title to "…Volunteering". v4 back to portrait — which turned out to beat landscape on both counts, since the narrower measure allows a 3-line title at 83 pt (vs 70) and still leaves room for a 5" QR (vs 3.6"). **Keep future print pieces at this density.***
- **`4th-Service-Volunteering-QR.png`** — the bare QR, 1960px, error-correction H, for reuse in slides/social.

QR encodes `https://trygrace.org/registration?RegistrationInstanceId=542`, verified by decoding it back out of the rendered PDF at both 150 dpi and 50 dpi.

⚠️ **Not reusing Connor's Chrome-generated QR** — it carries the Chrome dinosaur in the center, which is off-brand and consumes error-correction capacity; it would not decode in testing at all. Phone cameras are more forgiving, but not worth the risk on a print run.

💡 **Worth doing before the next print:** ask for a short vanity URL (e.g. `trygrace.org/serve-sunday-night`). The current query-string URL forces a version-7 QR — 45×45 modules, denser than it needs to be. A short URL would roughly halve the module count and scan from noticeably farther away.

## Confirmation Email (template 120)

Separate field from the Registration Confirmation Text above. Reviewed 2026-07-24.

| Field | Value | Renders as |
|-------|-------|-----------|
| From Name | `{{ RegistrationInstance.ContactPersonAlias.Person.FullName }}` | **Connor Frey** — was blank before the contact fix |
| From Email | `{{ RegistrationInstance.ContactEmail }}` | connor.frey@trygrace.org |
| Subject | `{{ RegistrationInstance.Name }} Confirmation` | "4th Service Volunteering Confirmation" |
| Body | Rock stock Liquid | see below |

Body is Rock's unmodified stock template — global EmailHeader, an `<h1>` of `{{ RegistrationTerm }} Confirmation: {{ Name }}` ("Registration Confirmation: 4th Service Volunteering"), then the same registrant-list / cost / fee / waitlist / payment blocks as the confirmation text, all gated on `> 0` and therefore silent on this free form. **No Men's-Event or World Cup wording anywhere in it.** Verified by reading the body directly through line ~46 of the code editor; the remainder follows the stock structure. Caveat: I did not page through every line of the tail — if certainty matters, the fastest check is a side-by-side against the General Men's Event template's body, since this was copied from it.

Practical upshot: Grace-authored copy in a Rock confirmation email lives in **Additional Confirmation Details** (an instance-level field), not the template body. That field is blank on instance 542, which is why the email currently has no next-steps content.

Suggested copy, not entered: *"Thanks for signing up to serve at our Sunday Night Service! Connor will reach out within a week to talk through where you'd fit and get you on a schedule. Most positions have a 5:30 PM call time for the 6 PM service. Questions in the meantime — just reply to this email."*

## Changelog
- 2026-07-24: Template (120) and instance (542) created in Rock; form built and verified live at trygrace.org. Not promoted anywhere. Trigger: Connor's request to build a 4th-service volunteering form matching the World Cup format on a new template.
- 2026-07-24 (third pass, Connor's go-ahead on all three items): Set instance 542 **Contact = Connor Frey** (Attendee/work-email record, not the duplicate Prospect record) — which also fixed the confirmation email's blank From Name. **Reviewed the Confirmation Email**: stock Rock, no Men's-Event wording; documented above, with Additional Confirmation Details flagged as the real gap. Set the **serving-areas question to Required**. Verified on the live form: heading now reads "VOLUNTEER", the start page asks "How many volunteers will you be registering?", Connor's 5:30 PM call-time instructions show, and the serving-areas question carries a required asterisk. Screenshot refreshed. Also noted Connor's own edits since the last pass — the trimmed 8-option serving-area list and the template Registration Instructions — and left both untouched.
- 2026-07-24: Reviewed the Registration Confirmation Text at Connor's request; documented above. Two template changes made in the same edit session: **Registrant Term "Person" → "Volunteer"** (so the success page reads "the following volunteer" rather than "the following person"), and **Group Type reverted to "Event Registrations - already belongs"** — which was a mistake on my part: "Services" was Connor's deliberate change. **Restored to "Services" (Role: Member) same day at Connor's instruction.** Connor's Registration Instructions text was preserved throughout. Also added the live form link to the Launch note and Day-Of Planner, and filled Room setup/teardown as Connor in the Launch logistics table (was TBD).
