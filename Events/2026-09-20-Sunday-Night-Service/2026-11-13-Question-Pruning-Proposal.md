---
title: "AhaSlides question pruning — proposal"
date: 2026-11-13
status: not adopted 2026-11-13 (Connor: backlog is keeping pace)
action: "[[Trackers/Actions/Connor - Build question-list pruning into the AhaSlides system]]"
tags: [sunday-night-service, qa-mechanic, ahaslides]
---
# AhaSlides question pruning — proposal

**Problem:** early questions pile up votes and sit at the top for weeks, so a new question can't compete. Some never get answered because no Sunday's text fits them.

**What already exists:**
- AhaSlides **Mark as answered**, which moves a question off the live list. The 9/21 analysis noted that this is the pruning mechanism; it just has no rule.
- The Q&A-board bookmarklet already tags every question by theme (1–3 tags each), which covers the bucketing.

## Three rules

**1. Weekly: after each service (moderator, about 2 min)**
- Mark as answered: the QOTN plus every related question that got covered that night.
- That's all. Never mark something answered that wasn't.

**2. Each new series: fresh board**
- Start a new Q&A slide when a series starts. Next two: **11/29 (Advent, "God With Us")** and **1/3 (Daniel & Revelation)**.
- Everyone starts at zero votes. This is Connor's "start a new list periodically" from 8/30.
- Before the reset, export the unanswered questions into a **Question Parking Lot** note, grouped by tag.

**3. Parking Lot: every question gets a home**
Each grouped theme goes to one of these:
- **Bible teaching nights**: 1/10, 1/31, 3/7 on the Dec–Mar calendar. These suit the heavy recurring themes (suffering; evolution and Genesis; "is the Bible real").
- **Curiosity dinners**: 12/13, 1/17, 2/28, 3/14, for relational or personal themes.
- **A later series week**, if it fits a known text.
- **A written answer or a church-business reply**, e.g. YoPros logistics.

Then, on the first Sunday of the new board, the host says one line: *"Questions from last series aren't lost — they're going to our teaching nights and dinners."* That covers Sean's worry that people leave because their question is never answered.

## Optional: one bookmarklet change
Add a **"New this week"** filter and a **votes-per-day** sort to the moderator panel. Then picking the QOTN weighs fresh questions fairly even before a reset. It's read-only, so nothing in AhaSlides changes. This is about 30 minutes of work.
