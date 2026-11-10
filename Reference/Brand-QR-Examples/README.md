---
title: "Grace QR code house style — the reference artifacts"
type: reference
date: 2026-09-22
tags: [brand, reference, qr-codes, marketing]
people:
  - "[[People/Heather Noble]]"
  - "[[People/Connor Frey]]"
---

# Grace QR code house style

**These two PDFs are the only record of Grace's current QR style.** Both were made by Heather Noble and arrived by email; neither existed in the vault until 2026-09-22. [[Reference/Grace-Brand-Guideline]] (Summer 2019) is silent on QR codes — the string "QR" appears in it exactly twice, both times inside a typeface specimen.

| File | Source | Notable |
|---|---|---|
| `Volunteer - Sunday Night_white.pdf` | Heather → Connor, "Volunteer Sign", 2026-09-11 10:13 AM ET | **Has** the teal centre badge with the white `g` |
| `BootCampMealSign.pdf` | Heather → Derek/John/Callie/Jennifer/Connor, "Re: Boot Camp meal", 2026-09-10 4:06 PM ET | **No** centre badge. Heather made it herself because *"Amanda is on vacation"* |

`.png` previews sit beside each PDF for quick viewing.

## The style, read off the artifacts

- **Data modules are small separated dots**, not squares — roughly 0.8 of the module pitch, so there is visible white between them.
- **Colour is Stable Blue `#1C3B6B`** on white. Active Blue is *not* used for the data.
- **Finder eyes are rounded squares**: a thick rounded ring with a solid **circle** inside — not a square inside.
- **The centre badge is OPTIONAL.** The volunteer sign carries a teal (`#2F97A0`) disc with the white lowercase `g` from the wordmark; the Boot Camp sign carries nothing. Do not treat the badge as mandatory.
- A badge needs **error correction H**, since the disc covers live modules.
- The QR always sits on a **white card**, even when the sign's field is navy or teal — see the Boot Camp sign, where the white card floats on the teal band.

## Reproducing it

`Workflows/promo-slide-build.py` draws this style from segno's module matrix (segno itself only emits squares). The white `g`, cropped from the wordmark and inverted, is vendored at `Workflows/assets/brand/grace-g-white.png`.

> [!warning] Decoder note
> OpenCV's strict `QRCodeDetector` **cannot read this style at all** — the rounded eyes defeat it, and it would fail on Heather's own signs above just as it fails on ours. Verify with the **WeChat detector** (`cv2.wechat_qrcode.WeChatQRCode()`, from `opencv-contrib-python-headless`), which is far more tolerant and much closer to a phone camera. A strict-detector failure is expected here and is **not** evidence of a broken code.

## What is still missing

[[Trackers/Actions/Heather Noble - Email Connor the updated brand-guidelines document]] is still open. These artifacts give the geometry; they do not give the **written rules** — logo minimum-spacing, minimum print size, whether the `g` badge has a rule governing when it applies, or whether colour inversions are permitted.
