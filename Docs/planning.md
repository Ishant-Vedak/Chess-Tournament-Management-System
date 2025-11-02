# 🧠 Project Planning — Chess Tournament System

## ✅ Goal
Build a web system for chess tournament organizers to register tournaments, receive a secure access code, and manage player/team submissions.

## 🎯 MVP Scope

### Organizer Flow
- Visit landing page
- Submit tournament form (name, date, location, organizer email)
- Backend saves to DB
- Secure alphanumeric tournament access code generated
- Code sent via email (Brevo)
- Organizer logs in using code (no password system — code = access token)

### Tournament Setup
Once logged in:
- Set players-per-team
- Optional CFC rating requirement
- Dashboard displays:
  - Teams (if team event)
  - Player list
  - Ratings & info

### Player Registration
- Generate Google Form link for organizers to share
- Later: sync form data into dashboard

> MVP uses Google Forms manually; automation can come later.

---

## 📦 Data Model (Initial)

### Tournament
| Field | Type |
|---|---|
id | UUID  
name | string  
location | string  
date | date  
organizer_email | string  
access_code | string (unique)  
team_size | int (nullable)  
rating_limit | int (nullable)  
created_at | datetime  

### Team *(future optional)*
| Field | Type |
|---|---|
id | UUID  
tournament_id | FK  
team_name | string  

### Player
| Field | Type |
|---|---|
id | UUID  
tournament_id | FK  
team_id | FK (nullable)  
name | string  
cfc_rating | int (nullable)  

---

## 🌐 API Endpoints (Django REST)

| Route | Method | Purpose |
|---|---|---|
`/api/tournaments/create/` | POST | Create tournament |
`/api/tournaments/login/` | POST | Login via code |
`/api/tournaments/settings/` | POST | Set rules (team size, rating req) |
`/api/tournaments/<id>/` | GET | Tournament dashboard |
`/api/teams/` *(future)* | GET/POST | Team management |
`/api/players/` *(future)* | GET/POST | Player management |

---

## ✉️ Email Logic
- On tournament creation:
  - Save to DB
  - Generate secure code
  - Email organizer summary + code + login link

---

## 🧠 Security Notes
- `secrets` module for code generation
- Rate-limit login attempts
- Code only grants access to that tournament
- No passwords to store

---

## 🧪 Testing Checklist
- ✅ Tournament form submits
- ✅ Email delivered
- ✅ Login with code
- ✅ Save team size + rating req
- ✅ Dashboard loads
- ✅ Display mock players

---

## 🚀 Deployment Plan (Free Tier)
| Layer | Platform |
|---|---|
Frontend | Vercel |
Backend | Render |
Database | Supabase |
Email | Brevo |
Forms | Google Forms |

---

## 📅 Development Phases

### Phase 1 — MVP
- Organizer registration + code login
- Tournament setup screen
- Basic dashboard
- Manual Google Form link

### Phase 2 — Enhanced
- Import Google Form responses
- Auto-create players & teams from spreadsheet

### Phase 3 — Future Ideas
- Swiss pairing algorithms
- Online payment for registration fees (Stripe)
- Notification system
- Admin broadcast messages

---

## 🏁 Success Criteria
Organizer can:
1. Create tournament  
2. Receive access code  
3. Configure event settings  
4. View team/player data  

If these work, MVP is complete ✅
