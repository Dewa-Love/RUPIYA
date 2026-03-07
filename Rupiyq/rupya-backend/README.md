# RUPYA — Full Stack Setup Guide

## Project Structure
```
rupya/
├── rupya-backend/          ← Flask backend (this folder)
│   ├── app.py              ← Main application
│   ├── requirements.txt    ← Python dependencies
│   └── instance/
│       └── rupya.db        ← SQLite database (auto-created)
│
└── rupya-website/          ← Your HTML frontend (existing folder)
    ├── index.html
    ├── apply.html
    └── ...all other pages
```

---

## Step 1 — Install Python dependencies

```bash
cd rupya-backend
pip install -r requirements.txt
```

---

## Step 2 — Run the server

```bash
python app.py
```

You'll see:
```
✅ Seeded 30 lenders
✅ Database ready
 * Running on http://127.0.0.1:5000
```

Open **http://localhost:5000** — your full website loads with backend connected.

---

## Step 3 — How it works

Flask serves your HTML files directly AND handles all API calls.

| Page | API Endpoint | What it does |
|------|-------------|--------------|
| apply.html | POST /api/apply | Saves loan application to DB |
| contact.html | POST /api/contact | Saves contact message to DB |
| partner-with-us.html | POST /api/partner | Saves partner application |
| customer-reviews.html | POST /api/reviews | Submits review (needs approval) |
| customer-reviews.html | GET /api/reviews | Loads approved reviews |
| eligibility.html | POST /api/eligibility | Real eligibility calculation |
| comparison.html | GET /api/lenders?type=home | Real bank data from DB |
| calculator.html | POST /api/calculate-emi | Server-side EMI calculation |

---

## Admin Endpoints (view submitted data)

Open these in your browser while server is running:

```
http://localhost:5000/api/admin/applications     → All loan applications
http://localhost:5000/api/admin/contacts         → All contact messages
http://localhost:5000/api/admin/partners         → All partner applications
http://localhost:5000/api/admin/reviews/pending  → Reviews awaiting approval
```

**Approve a review:**
```bash
curl -X POST http://localhost:5000/api/admin/reviews/1/approve
```

**Update application status:**
```bash
curl -X POST http://localhost:5000/api/admin/applications/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'
```

Status options: `pending` → `reviewing` → `approved` / `rejected`

---

## Database — View & Edit Directly

Install DB Browser for SQLite (free): https://sqlitebrowser.org
Open: `rupya-backend/instance/rupya.db`

Tables:
- `loan_application` — all applications
- `contact_message` — all contact form submissions
- `review` — customer reviews
- `partner_application` — partnership requests
- `lender` — bank/lender data (edit rates here!)

---

## Updating Interest Rates

Open `rupya.db` in DB Browser → `lender` table → edit `rate_min` / `rate_max` columns.
Changes reflect instantly on the website — no code changes needed.

---

## Deploying to Production (when ready)

### Option A — Render.com (free)
1. Push code to GitHub
2. Create new Web Service on render.com
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`
5. Add environment variable: `FLASK_ENV=production`

### Option B — Railway.app (free tier)
1. Push to GitHub
2. Connect repo on railway.app
3. Auto-detects Python, deploys automatically

### For production, switch SQLite → PostgreSQL:
Change this line in app.py:
```python
# Replace:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/rupya.db'

# With:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host/dbname'
```
Everything else stays the same. Flask-SQLAlchemy handles the switch automatically.

---

## Folder Setup (Important)

Make sure your folder structure looks like this:
```
rupya/
├── rupya-backend/   ← backend lives here
└── rupya-website/   ← frontend HTML files here
```

If you put them in different locations, update this line in app.py:
```python
app = Flask(__name__, static_folder='../rupya-website', static_url_path='')
#                                    ↑ relative path to your HTML folder
```
