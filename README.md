#  Chess Tournament Management System
##  Project Overview

This project is a web application for organizing chess tournaments. Organizers can register a tournament, receive a secure alphanumeric access code via email, and then manage tournament settings — including team size and CFC rating requirements. A separate organizer portal will allow viewing all registered teams, players, and ratings once submissions are collected.

A Google Form link will later be generated and shared with players/teams to submit player details (phase 2 of project — will be implemented later).

## Core Features
### Phase 1 — Organizer Flow

1.	Organizer visits landing page and completes tournament registration form.
2.	Backend stores the tournament in PostgreSQL.
3.	Backend generates secure alphanumeric access code.
4.	Organizer receives access code via email.
5.	Organizer logs in using code on dedicated portal page.

### Phase 2 — Tournament Setup

After login:

- Specify team size
- Set CFC rating requirement (optional)
- View tournament dashboard with:
- Team list
- Player names
- CFC ratings
- Additional info fields

### Phase 3 — Player Registration (Future)

- System generates a Google Form
- Link shared with clubs/players
- Responses pulled and displayed in the dashboard

##  Technology Stack
### Frontend

- React

- Vanilla CSS / Sass

- Vercel for deployment (free)

### Backend

- Django + Django REST Framework

- Python secrets for secure tournament code generation

- Supabase PostgreSQL (free, persistent DB)

- Brevo email service (free 300 emails/day)

- Render for backend hosting (free tier)

### Additional Services

- Google Forms for player registration forms
(future-proof, free, easy API access)