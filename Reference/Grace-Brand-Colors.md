---
title: "Grace Brand Colors — hex reference"
type: reference
date: 2026-08-18
source: "trygrace.org (Rock v17.6.1.0) computed CSS, 2026-08-18; plus Sunday_Night_Service_Promo_Deck_73026.pptx XML, 2026-08-18. Values read from source, not eyeballed from screenshots."
tags: [brand, reference, marketing]
people:
  - "[[People/Heather Noble]]"
---

# Grace Brand Colors

> [!danger] ⚠️ SUPERSEDED 2026-09-16 — this note's central conclusion was backwards
> **The real brand book is now in the vault:** [[Reference/Grace-Brand-Guideline]] (`GraceCommunity_BrandGuideline_190627.pdf`, Summer 2019, from Heather Noble). **Use it, not this file, for palette and type.**
>
> This note argued that the website's `#2A95A0` was *"the only defensible teal"* and that Heather's promo deck's `#2F97A0` navy `#1C3B6B` had *"no traceable Grace origin."* **The opposite is true.** The book specifies **Active Blue `#2F97A0` (PANTONE 2235 C)**, **Stable Blue `#1C3B6B` (PANTONE 534 C)**, **Cinder Gray `#ABABAB` (429 C)** and **Cloud Gray `#E3E3E3` (427 C)** — every color in Heather's deck, exactly. **The deck was on-brand; the website is the drift.**
>
> The reasoning failed in a specific, repeatable way: the website's CSS could be *queried*, so it was treated as the source of truth, while a deck that could not be queried was treated as suspect because it had been machine-generated. **Ease of access is not provenance.** Worth remembering the next time a value is "verified" because it was easy to read.
>
> **What in this note is still good:** the drift table (three teals in circulation, only one real — the conclusion holds, the winner changes), the Rock-CMS warning below, and the note that `--base-primary: #ff791d` will produce an orange Grace asset. Keep reading for those. Ignore every verdict about which value is authoritative.

**Read this before building anything Grace-branded.** Heather Noble, 2026-07-30, on an AI-generated social graphic for John's faith story: *"Claude designed that, and it did not get our brand colors right."* This note exists so that stops happening.

## The palette

| Role | Hex | Where it appears |
|---|---|---|
| **Teal — primary** | **`#2A95A0`** | The brand color. Buttons (GIVE, COME AND SEE), links, icons. Declared as `--color-primary` and `--color-base-primary: 42,149,160`. |
| Teal — dark / hover | `#276975` | Darker shade of the primary. |
| Teal — heading | `#0D7B8D` | Section headings ("Arlington"). Slightly deeper and bluer than the primary. |
| Teal — muted | `#40788E` | Form labels. |
| **Pale blue-grey** | **`#CADDE2`** | Light section backgrounds — the only tint in the palette. |
| **Black** | **`#000000`** | Top bar, main nav, footer. Grace's chrome is true black, not charcoal. |
| Near-black | `#292929` | Dark content section backgrounds. |
| Near-black alt | `#3A3A3A` · `#343434` | Secondary dark panels. |
| **White** | **`#FFFFFF`** | Body background, and the wordmark reversed out of dark imagery. |
| Body text grey | `#757575` | Paragraph copy. |
| Heading dark | `#333333` | Headings on white. |
| Hairline grey | `#F0F0F0` | Dividers, subtle fills. |

Theme greys declared in CSS, for completeness: `--theme-darkest #222` · `--theme-dark #333` · `--theme-medium #555` · `--theme-light #eee` · `--theme-lightest #f3f3f3` · `--theme-black #343a40`.

## ⚠️ Do not use these — they are Rock CMS defaults, not Grace

The site runs on **Rock v17.6.1.0**, which ships its own design tokens. They are present in the page's CSS and they are **not Grace's brand**:

`--base-primary: #ff791d` (orange) · `--base-critical: #ee7725` · `--base-secondary: #83758f` · `--base-link: #006dcc` · the whole `--color-categorical-*` set (`#007aff`, `#5856d6`, `#4cd964`, `#ff2d55`…).

Anything reading the raw stylesheet will find `--base-primary` first and produce an **orange** Grace asset. Grace's primary is `--color-primary`, the teal.

## ⚠️ Known drift: the 7/26 volunteer sign is off-brand

[[Events/2026-09-20-Sunday-Night-Service/4th-Service-Volunteering-Rock-Form]] documents `4th-Service-Volunteering-Sign.pdf` as built with *"thin teal (#44979D) bands top and bottom, charcoal #3D3D3D type."*

Neither value is Grace's:

| Used on the sign | Actual brand | Delta |
|---|---|---|
| `#44979D` | `#2A95A0` | lighter and greyer — visibly close, measurably wrong |
| `#3D3D3D` | `#333333` (text) / `#000000` (chrome) | close to nothing in the real palette |

Not worth reprinting a sign already used on 7/26 — but **rebuild from `#2A95A0` next time**, and treat this as the second recorded instance of a Grace asset shipping with invented colors.

## The Sunday Night promo deck uses a different palette

`Sunday_Night_Service_Promo_Deck_73026.pptx` (16 slides, Heather Noble last-modified 2026-07-31) — the deck Connor called *"thoroughly impressed… no notes"* on 7/30. Every slide uses the same six colors:

| Role in the deck | Hex | Notes |
|---|---|---|
| **Navy — dominant** | **`#1C3B6B`** | Title-slide full bleed, all headings, the big stat numbers. **Appears nowhere on trygrace.org.** |
| **Teal — accent** | **`#2F97A0`** | Rules under headings, eyebrow labels ("PROMO BEGINS"), the logo lockup box. **Not the site teal.** |
| Body copy | `#2A2A2A` | |
| Card fill | `#E3E3E3` | |
| Footer line | `#ABABAB` | |
| Background | `#FFFFFF` | |

Type is **Arial** throughout. The PowerPoint theme is stock **Office** (Calibri, `#4472C4`, `#ED7D31`) — untouched, so every color is a hard-coded override.

## ⚠️ There are three Grace teals in circulation and only one has provenance

| Value | Where | Provenance |
|---|---|---|
| **`#2A95A0`** | trygrace.org `--color-primary` | ✅ **The system declares it.** Use this. |
| `#2F97A0` | Heather's promo deck | ✖ none — off by (5,2,0) |
| `#44979D` | 7/26 volunteer sign | ✖ none — off by (26,2,-3) |

All three read as "Grace teal" to the eye and none of them match. That is the signature of a color **approximated** rather than copied — which is what happens when someone samples a screenshot or a generator guesses.

### Why the deck's palette is not a brand source

The deck's own metadata: `dc:creator` = **PptxGenJS**, `Company` = **PptxGenJS**, `dc:title` = *"PptxGenJS Presentation"*, theme *"Office Theme"*. PptxGenJS is a JavaScript generation library — this deck was **built programmatically**, then opened and edited in PowerPoint by Heather (revision 10, created 7/15, modified 7/31).

So `#1C3B6B` navy has **no traceable Grace origin**. It may be a real brand secondary that simply isn't on the website — Grace's print and social material could well use it. But it is equally consistent with a generator inventing a "churchy navy," and it is the same class of artifact Heather herself flagged on 7/30: *"Claude designed that, and it did not get our brand colors right."*

**Do not treat the deck as the standard, and do not treat this note as settling it either.** → **Ask Heather Noble for Grace's actual brand standard** — a one-line ask to the person who owns brand, and the only thing that ends the guessing. Until then, `#2A95A0` is the only defensible teal, and navy is unverified.

## Other brand facts worth having here

- **Wordmark:** lowercase "grace" with "COMMUNITY CHURCH" letterspaced beneath, white when reversed on dark imagery.
- **Tagline on the site:** *"A church for people who don't go to church."*
- ⚠️ **The Sunday-night external line was never actually picked.** The vault records *"New Rhythm, Same Grace"* as the positioning line, but deck slide 13 lists **two** options under the same "Primary" heading: *"New rhythm, same service. Join us for Sunday Night Service beginning September 20 at 6pm."* and *"New rhythm, same Grace. Join us for Sunday Night Service beginning September 20 at 6pm."* Nobody chose. **"Same Grace" is the better line** — it puts the church's name in the promise and says the thing that reassures a morning attendee; "same service" is literally false, since the format is different. But that is a recommendation, not a decision, and Derek's marketing needs it by 8/30.
- **Front-door decal, week of 9/13:** a new colour was specified because **white is unreadable in daylight** — so the decal will not be the reversed white wordmark.
- ⚠️ **These values expire.** Grace is building a **fully new AI-agentic website** (~3 months out as of 2026-07-30, so roughly late Oct 2026). The 9/20 launch runs on this old site. **Re-derive this palette once the new site is live.**

## How to re-derive

Load trygrace.org and read `--color-primary` off `:root`, then tally computed `background-color` / `color` across rendered elements by area. Do not sample a screenshot — JPEG artifacts shift hex values by a few points, which is exactly how `#2A95A0` becomes something like `#44979D`.
