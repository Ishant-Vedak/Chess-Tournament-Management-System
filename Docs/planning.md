# Project Planning — Chess Tournament System

- This is just for planning the current feature I want to address. 

Organizer pipeline (?): 

Creating Tournament:

1. Visit landing page, 
2. click on create tournament in hero, 
3. login/create account (although many find it annoying, but will deal with this later), 
4. fill out tournament form, 
5. receive confirmation email, 
6. gain access to tournament admin page and control participants, staff, be able to link a google forms for participant registration (and probably confirm if fee is paid), 
7. host tournament.

This tournament logic will vary based on type, and I will figure this out later.

Ending Tournament:

1. End tournament, 
2. show final results will all points, 
3. create a file (probably pdf or json or both) containing all data,
4. delete it in 14 days (seems like good amount of time). OR save every tournament until it becomes an issue.


## Current Goal:

> **An organizer can generate Round 1 and enter results without touching code.**

Everything below serves that.

---

## STEP 1 — Participant model (highest priority)

You cannot host *anything* without this.

### What to build

* `Participant` (or `PlayerEntry`)
* ForeignKey → Tournament
* NOT linked to User

Minimum fields:

* name
* rating (nullable)
* email (nullable)
* seed / ordering index (optional)

### Rules

* Can only be added when `REGISTRATION_OPEN`
* Frozen once tournament is `ONGOING`

### Tests

* Adding when open → allowed
* Adding when closed → blocked

---

## STEP 2 — Import pipeline (CSV first)

Forget Google Forms API for now.

### Build:

* CSV upload form
* Preview parsed rows
* Confirm import
* Store batch ID

### Why now

* This is how organizers *actually* add players
* Manual entry does not scale
* This is a key demo feature

---

## STEP 3 — Round + Match models (format-agnostic)

Design this carefully once.

### Round

* tournament
* round_number
* status (PENDING / ACTIVE / COMPLETE)

### Match

* round
* player1
* player2 (nullable → bye)
* result

These models **do not care about format**.

---

## STEP 4 — Swiss Round 1 generation (only)

Do NOT build all formats yet.

### Logic (v1)

* Sort participants by rating (or random)
* Pair top half vs bottom half
* One bye if odd count

### Where

* `tournaments/services/swiss.py`

### Tests

* Correct number of matches
* One bye max
* No duplicate players

---

## STEP 5 — Result entry + standings

Minimum viable standings:

* Player
* Points
* Games played

No tiebreaks yet.

This makes your tournament **feel real**.

---

## STEP 6 — Organizer admin page (ugly but functional)

This page should:

* Show participant list
* Show rounds
* Enter results
* Advance tournament

If this page works, your app works.

---

## What to NOT do yet ❌

* Multiple formats simultaneously
* Tiebreak math
* Color balancing
* Fancy UI
* Player accounts
* Ratings updates

---

## Decision point (I need one answer)

Before I guide you further, answer this:

**Do you want to implement Swiss first, or Knockout first?**

Swiss is harder but more impressive.
Knockout is simpler and faster.

Reply with **“Swiss”** or **“Knockout”**, and we’ll continue step-by-step.


