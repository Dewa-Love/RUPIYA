from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='../rupya-website', static_url_path='')
CORS(app)

# ── DATABASE CONFIG ──
basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'rupya.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rupya-secret-change-in-production'

db = SQLAlchemy(app)


# ════════════════════════════════════════
#  MODELS
# ════════════════════════════════════════

class LoanApplication(db.Model):
    """Submitted loan applications from apply.html"""
    id           = db.Column(db.Integer, primary_key=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Step 1 — Personal Info
    first_name   = db.Column(db.String(100))
    last_name    = db.Column(db.String(100))
    email        = db.Column(db.String(200))
    phone        = db.Column(db.String(20))
    dob          = db.Column(db.String(20))
    pan          = db.Column(db.String(20))

    # Step 2 — Loan Details
    loan_type    = db.Column(db.String(50))   # personal, home, car, business, education, gold
    loan_amount  = db.Column(db.Float)
    tenure       = db.Column(db.Integer)      # months
    purpose      = db.Column(db.String(200))

    # Step 3 — Employment
    employment   = db.Column(db.String(50))   # salaried, self-employed, business
    company      = db.Column(db.String(200))
    income       = db.Column(db.Float)        # monthly net
    experience   = db.Column(db.Integer)      # years

    # Status
    status       = db.Column(db.String(30), default='pending')  # pending, reviewing, approved, rejected

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'phone': self.phone,
            'loan_type': self.loan_type,
            'loan_amount': self.loan_amount,
            'tenure': self.tenure,
            'employment': self.employment,
            'income': self.income,
            'status': self.status,
        }


class ContactMessage(db.Model):
    """Messages from contact.html"""
    id         = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name       = db.Column(db.String(100))
    email      = db.Column(db.String(200))
    phone      = db.Column(db.String(20))
    subject    = db.Column(db.String(200))
    message    = db.Column(db.Text)
    replied    = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'replied': self.replied,
        }


class Review(db.Model):
    """Customer reviews from customer-reviews.html"""
    id         = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name       = db.Column(db.String(100))
    loan_type  = db.Column(db.String(50))
    rating     = db.Column(db.Integer)        # 1–5
    text       = db.Column(db.Text)
    approved   = db.Column(db.Boolean, default=False)  # admin must approve before showing

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'name': self.name,
            'loan_type': self.loan_type,
            'rating': self.rating,
            'text': self.text,
        }


class PartnerApplication(db.Model):
    """Partnership applications from partner-with-us.html"""
    id           = db.Column(db.Integer, primary_key=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    org_name     = db.Column(db.String(200))
    partner_type = db.Column(db.String(100))
    contact_name = db.Column(db.String(100))
    role         = db.Column(db.String(100))
    email        = db.Column(db.String(200))
    phone        = db.Column(db.String(20))
    volume       = db.Column(db.String(50))
    geography    = db.Column(db.String(100))
    message      = db.Column(db.Text)
    status       = db.Column(db.String(30), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'org_name': self.org_name,
            'partner_type': self.partner_type,
            'contact_name': self.contact_name,
            'email': self.email,
            'phone': self.phone,
            'volume': self.volume,
            'status': self.status,
        }


class Lender(db.Model):
    """Bank/lender data for comparison.html and loan pages"""
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(100))
    logo_url        = db.Column(db.String(300))
    loan_type       = db.Column(db.String(50))   # home, personal, car, business, gold, education, lap
    rate_min        = db.Column(db.Float)         # minimum interest rate %
    rate_max        = db.Column(db.Float)
    max_amount      = db.Column(db.Float)         # in rupees
    max_tenure      = db.Column(db.Integer)       # months
    processing_fee  = db.Column(db.String(50))    # e.g. "0.5%" or "₹999"
    approval_time   = db.Column(db.String(50))    # e.g. "24 hrs"
    min_cibil       = db.Column(db.Integer)       # minimum CIBIL score
    is_featured     = db.Column(db.Boolean, default=False)
    active          = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'loan_type': self.loan_type,
            'rate_min': self.rate_min,
            'rate_max': self.rate_max,
            'max_amount': self.max_amount,
            'max_tenure': self.max_tenure,
            'processing_fee': self.processing_fee,
            'approval_time': self.approval_time,
            'min_cibil': self.min_cibil,
            'is_featured': self.is_featured,
        }


# ════════════════════════════════════════
#  SERVE FRONTEND
# ════════════════════════════════════════

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def frontend(filename):
    return send_from_directory(app.static_folder, filename)


# ════════════════════════════════════════
#  API — LOAN APPLICATION
# ════════════════════════════════════════

@app.route('/api/apply', methods=['POST'])
def submit_application():
    d = request.get_json()
    if not d:
        return jsonify({'error': 'No data received'}), 400

    required = ['first_name', 'last_name', 'email', 'phone', 'loan_type', 'loan_amount']
    for field in required:
        if not d.get(field):
            return jsonify({'error': f'Missing required field: {field}'}), 400

    app_obj = LoanApplication(
        first_name  = d.get('first_name', '').strip(),
        last_name   = d.get('last_name', '').strip(),
        email       = d.get('email', '').strip().lower(),
        phone       = d.get('phone', '').strip(),
        dob         = d.get('dob', ''),
        pan         = d.get('pan', '').upper().strip(),
        loan_type   = d.get('loan_type', ''),
        loan_amount = float(d.get('loan_amount', 0)),
        tenure      = int(d.get('tenure', 12)),
        purpose     = d.get('purpose', ''),
        employment  = d.get('employment', ''),
        company     = d.get('company', ''),
        income      = float(d.get('income', 0)),
        experience  = int(d.get('experience', 0)),
    )
    db.session.add(app_obj)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Application submitted successfully!',
        'application_id': app_obj.id,
        'ref': f'RUPYA-{app_obj.id:06d}'
    }), 201


@app.route('/api/apply/<int:app_id>', methods=['GET'])
def get_application(app_id):
    a = LoanApplication.query.get_or_404(app_id)
    return jsonify(a.to_dict())


# ════════════════════════════════════════
#  API — ELIGIBILITY CHECK
# ════════════════════════════════════════

@app.route('/api/eligibility', methods=['POST'])
def check_eligibility():
    d = request.get_json()
    employment  = d.get('employment', 'salaried')
    age         = int(d.get('age', 30))
    income      = float(d.get('income', 0))
    loan_amount = float(d.get('loan_amount', 0))
    cibil       = d.get('cibil', '700-749')
    existing_emi= float(d.get('existing_emi', 0))
    loan_type   = d.get('loan_type', 'personal')

    # Parse CIBIL score midpoint
    cibil_map = {'below-650': 620, '650-699': 675, '700-749': 725, '750-799': 775, '800+': 820}
    cibil_score = cibil_map.get(cibil, 700)

    # Basic eligibility rules
    issues = []
    score = 100

    if age < 21 or age > 65:
        issues.append('Age must be between 21–65 years')
        score -= 40

    if income < 15000:
        issues.append('Minimum monthly income required is ₹15,000')
        score -= 30

    # FOIR — Fixed Obligation to Income Ratio (max 50–60%)
    foir = (existing_emi / income * 100) if income > 0 else 0
    estimated_new_emi = loan_amount * 0.009  # rough EMI estimate
    total_foir = ((existing_emi + estimated_new_emi) / income * 100) if income > 0 else 0

    if total_foir > 60:
        issues.append(f'Total EMI burden ({total_foir:.0f}% of income) exceeds 60% limit')
        score -= 25

    if cibil_score < 650:
        issues.append('CIBIL score below 650 — most lenders require 700+')
        score -= 35
    elif cibil_score < 700:
        score -= 15

    # Loan amount vs income check
    multiplier = {'personal': 24, 'home': 60, 'car': 36, 'business': 18, 'gold': 12, 'education': 30, 'lap': 48}
    max_loan = income * multiplier.get(loan_type, 24)
    if loan_amount > max_loan:
        issues.append(f'Loan amount exceeds recommended limit of ₹{max_loan:,.0f} for your income')
        score -= 20

    score = max(0, min(100, score))
    eligible = score >= 60 and len(issues) == 0

    # Match lenders
    lenders = Lender.query.filter_by(loan_type=loan_type, active=True).all()
    matched = []
    for l in lenders:
        if cibil_score >= (l.min_cibil or 650):
            matched.append(l.to_dict())

    return jsonify({
        'eligible': eligible,
        'score': score,
        'issues': issues,
        'foir': round(total_foir, 1),
        'max_recommended_loan': max_loan,
        'matched_lenders': len(matched),
        'lenders': matched[:5],
        'message': 'You qualify for loans!' if eligible else 'Some issues found — see details below.'
    })


# ════════════════════════════════════════
#  API — CONTACT
# ════════════════════════════════════════

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    d = request.get_json()
    if not d.get('name') or not d.get('email') or not d.get('message'):
        return jsonify({'error': 'Name, email and message are required'}), 400

    msg = ContactMessage(
        name    = d.get('name', '').strip(),
        email   = d.get('email', '').strip().lower(),
        phone   = d.get('phone', '').strip(),
        subject = d.get('subject', 'General Inquiry'),
        message = d.get('message', '').strip(),
    )
    db.session.add(msg)
    db.session.commit()

    return jsonify({'success': True, 'message': "Message received! We'll reply within 24 hours."}), 201


# ════════════════════════════════════════
#  API — REVIEWS
# ════════════════════════════════════════

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    loan_type = request.args.get('type', None)
    query = Review.query.filter_by(approved=True)
    if loan_type:
        query = query.filter_by(loan_type=loan_type)
    reviews = query.order_by(Review.created_at.desc()).limit(20).all()
    return jsonify([r.to_dict() for r in reviews])


@app.route('/api/reviews', methods=['POST'])
def submit_review():
    d = request.get_json()
    if not d.get('name') or not d.get('text') or not d.get('rating'):
        return jsonify({'error': 'Name, rating and review text are required'}), 400

    review = Review(
        name      = d.get('name', '').strip(),
        loan_type = d.get('loan_type', 'Personal Loan'),
        rating    = int(d.get('rating', 5)),
        text      = d.get('text', '').strip(),
        approved  = False,  # requires admin approval
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Review submitted! It will appear after approval.'}), 201


# ════════════════════════════════════════
#  API — PARTNER APPLICATION
# ════════════════════════════════════════

@app.route('/api/partner', methods=['POST'])
def submit_partner():
    d = request.get_json()
    if not d.get('org_name') or not d.get('contact_name') or not d.get('email'):
        return jsonify({'error': 'Organisation name, contact name and email are required'}), 400

    partner = PartnerApplication(
        org_name     = d.get('org_name', '').strip(),
        partner_type = d.get('partner_type', ''),
        contact_name = d.get('contact_name', '').strip(),
        role         = d.get('role', ''),
        email        = d.get('email', '').strip().lower(),
        phone        = d.get('phone', '').strip(),
        volume       = d.get('volume', ''),
        geography    = d.get('geography', ''),
        message      = d.get('message', '').strip(),
    )
    db.session.add(partner)
    db.session.commit()

    return jsonify({'success': True, 'message': "Application received! We'll be in touch within 24 hours."}), 201


# ════════════════════════════════════════
#  API — LENDERS / COMPARISON
# ════════════════════════════════════════

@app.route('/api/lenders', methods=['GET'])
def get_lenders():
    loan_type = request.args.get('type', 'home')
    sort_by   = request.args.get('sort', 'rate')  # rate, fee, speed

    lenders = Lender.query.filter_by(loan_type=loan_type, active=True).all()
    data = [l.to_dict() for l in lenders]

    if sort_by == 'rate':
        data.sort(key=lambda x: x['rate_min'])
    elif sort_by == 'fee':
        data.sort(key=lambda x: x.get('processing_fee', '99'))
    elif sort_by == 'speed':
        data.sort(key=lambda x: x.get('approval_time', 'z'))

    return jsonify(data)


# ════════════════════════════════════════
#  API — EMI CALCULATOR (server-side)
# ════════════════════════════════════════

@app.route('/api/calculate-emi', methods=['POST'])
def calculate_emi():
    d = request.get_json()
    principal = float(d.get('amount', 0))
    rate      = float(d.get('rate', 8.4)) / 100 / 12  # monthly rate
    tenure    = int(d.get('tenure', 240))  # months

    if rate == 0:
        emi = principal / tenure
    else:
        emi = principal * rate * ((1 + rate) ** tenure) / (((1 + rate) ** tenure) - 1)

    total_payment  = emi * tenure
    total_interest = total_payment - principal

    return jsonify({
        'emi': round(emi, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'principal': principal,
        'interest_percentage': round((total_interest / total_payment) * 100, 1)
    })


# ════════════════════════════════════════
#  ADMIN — simple read-only endpoints
# ════════════════════════════════════════

@app.route('/api/admin/applications', methods=['GET'])
def admin_applications():
    apps = LoanApplication.query.order_by(LoanApplication.created_at.desc()).all()
    return jsonify([a.to_dict() for a in apps])

@app.route('/api/admin/contacts', methods=['GET'])
def admin_contacts():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([m.to_dict() for m in msgs])

@app.route('/api/admin/partners', methods=['GET'])
def admin_partners():
    partners = PartnerApplication.query.order_by(PartnerApplication.created_at.desc()).all()
    return jsonify([p.to_dict() for p in partners])

@app.route('/api/admin/reviews/pending', methods=['GET'])
def admin_pending_reviews():
    reviews = Review.query.filter_by(approved=False).all()
    return jsonify([r.to_dict() for r in reviews])

@app.route('/api/admin/reviews/<int:rid>/approve', methods=['POST'])
def approve_review(rid):
    r = Review.query.get_or_404(rid)
    r.approved = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/admin/applications/<int:aid>/status', methods=['POST'])
def update_application_status(aid):
    a = LoanApplication.query.get_or_404(aid)
    d = request.get_json()
    a.status = d.get('status', a.status)
    db.session.commit()
    return jsonify({'success': True, 'status': a.status})


# ════════════════════════════════════════
#  INIT DB + SEED LENDER DATA
# ════════════════════════════════════════

def seed_lenders():
    if Lender.query.count() > 0:
        return  # already seeded

    lenders_data = [
        # HOME LOANS
        dict(name='SBI',           loan_type='home', rate_min=8.40, rate_max=10.15, max_amount=10000000, max_tenure=360, processing_fee='₹10,000', approval_time='72 hrs',  min_cibil=650, is_featured=True),
        dict(name='HDFC Bank',     loan_type='home', rate_min=8.50, rate_max=10.10, max_amount=10000000, max_tenure=360, processing_fee='0.5%',     approval_time='48 hrs',  min_cibil=700, is_featured=True),
        dict(name='ICICI Bank',    loan_type='home', rate_min=8.75, rate_max=10.05, max_amount=10000000, max_tenure=360, processing_fee='0.5%',     approval_time='48 hrs',  min_cibil=700),
        dict(name='Axis Bank',     loan_type='home', rate_min=8.75, rate_max=13.30, max_amount=5000000,  max_tenure=360, processing_fee='1%',       approval_time='72 hrs',  min_cibil=700),
        dict(name='Kotak Mahindra',loan_type='home', rate_min=8.70, rate_max=9.50,  max_amount=10000000, max_tenure=360, processing_fee='0.5%',     approval_time='48 hrs',  min_cibil=720),
        dict(name='LIC HFL',       loan_type='home', rate_min=8.50, rate_max=10.75, max_amount=15000000, max_tenure=360, processing_fee='₹15,000',  approval_time='5 days',  min_cibil=650),
        # PERSONAL LOANS
        dict(name='SBI',           loan_type='personal', rate_min=10.30, rate_max=15.30, max_amount=2000000, max_tenure=84,  processing_fee='1.5%',  approval_time='24 hrs',  min_cibil=650, is_featured=True),
        dict(name='HDFC Bank',     loan_type='personal', rate_min=10.50, rate_max=24.00, max_amount=4000000, max_tenure=60,  processing_fee='2.5%',  approval_time='4 hrs',   min_cibil=700),
        dict(name='ICICI Bank',    loan_type='personal', rate_min=10.65, rate_max=16.00, max_amount=5000000, max_tenure=72,  processing_fee='2%',    approval_time='Same day',min_cibil=700),
        dict(name='Bajaj Finserv', loan_type='personal', rate_min=11.00, rate_max=35.00, max_amount=3500000, max_tenure=96,  processing_fee='3.93%', approval_time='2 hrs',   min_cibil=685, is_featured=True),
        dict(name='Axis Bank',     loan_type='personal', rate_min=10.80, rate_max=22.00, max_amount=4000000, max_tenure=60,  processing_fee='2%',    approval_time='4 hrs',   min_cibil=700),
        dict(name='Tata Capital',  loan_type='personal', rate_min=10.99, rate_max=35.00, max_amount=3500000, max_tenure=72,  processing_fee='2.75%', approval_time='Same day',min_cibil=700),
        # CAR LOANS
        dict(name='SBI',           loan_type='car', rate_min=8.85, rate_max=11.35, max_amount=2500000, max_tenure=84,  processing_fee='₹1,000', approval_time='2 days',  min_cibil=650, is_featured=True),
        dict(name='HDFC Bank',     loan_type='car', rate_min=9.00, rate_max=12.50, max_amount=2500000, max_tenure=84,  processing_fee='0.4%',   approval_time='24 hrs',  min_cibil=700),
        dict(name='ICICI Bank',    loan_type='car', rate_min=9.10, rate_max=12.75, max_amount=2500000, max_tenure=84,  processing_fee='1%',     approval_time='Same day',min_cibil=700),
        dict(name='Axis Bank',     loan_type='car', rate_min=9.20, rate_max=13.50, max_amount=2500000, max_tenure=84,  processing_fee='1%',     approval_time='48 hrs',  min_cibil=700),
        # BUSINESS LOANS
        dict(name='SBI',           loan_type='business', rate_min=10.90, rate_max=14.90, max_amount=5000000,  max_tenure=60, processing_fee='1%',    approval_time='5 days',  min_cibil=650, is_featured=True),
        dict(name='HDFC Bank',     loan_type='business', rate_min=11.00, rate_max=22.50, max_amount=5000000,  max_tenure=48, processing_fee='2%',    approval_time='72 hrs',  min_cibil=700),
        dict(name='Bajaj Finserv', loan_type='business', rate_min=14.00, rate_max=30.00, max_amount=5000000,  max_tenure=96, processing_fee='3.54%', approval_time='24 hrs',  min_cibil=685, is_featured=True),
        dict(name='Tata Capital',  loan_type='business', rate_min=12.00, rate_max=35.00, max_amount=7500000,  max_tenure=60, processing_fee='2.75%', approval_time='Same day',min_cibil=700),
        dict(name='ICICI Bank',    loan_type='business', rate_min=11.50, rate_max=17.00, max_amount=20000000, max_tenure=84, processing_fee='2%',    approval_time='72 hrs',  min_cibil=700),
        # GOLD LOANS
        dict(name='Muthoot Finance',loan_type='gold', rate_min=8.80,  rate_max=24.00, max_amount=5000000, max_tenure=24, processing_fee='₹0',    approval_time='30 min',  min_cibil=0, is_featured=True),
        dict(name='Manappuram',    loan_type='gold', rate_min=9.90,  rate_max=26.00, max_amount=5000000, max_tenure=12, processing_fee='₹0',    approval_time='30 min',  min_cibil=0),
        dict(name='SBI',           loan_type='gold', rate_min=9.00,  rate_max=9.00,  max_amount=2000000, max_tenure=36, processing_fee='0.5%',  approval_time='Same day',min_cibil=0),
        dict(name='HDFC Bank',     loan_type='gold', rate_min=9.50,  rate_max=17.55, max_amount=5000000, max_tenure=24, processing_fee='1%',    approval_time='1 hr',    min_cibil=0),
        # EDUCATION LOANS
        dict(name='SBI',           loan_type='education', rate_min=8.05, rate_max=11.15, max_amount=2000000,  max_tenure=180, processing_fee='₹0',   approval_time='7 days', min_cibil=0, is_featured=True),
        dict(name='Bank of Baroda',loan_type='education', rate_min=8.15, rate_max=9.85,  max_amount=4000000,  max_tenure=180, processing_fee='₹0',   approval_time='7 days', min_cibil=0),
        dict(name='HDFC Credila',  loan_type='education', rate_min=9.55, rate_max=13.25, max_amount=15000000, max_tenure=180, processing_fee='1%',   approval_time='5 days', min_cibil=650, is_featured=True),
        dict(name='Avanse',        loan_type='education', rate_min=9.90, rate_max=14.00, max_amount=7500000,  max_tenure=180, processing_fee='1%',   approval_time='5 days', min_cibil=650),
        # LAP — Loan Against Property
        dict(name='SBI',           loan_type='lap', rate_min=9.60,  rate_max=11.30, max_amount=75000000, max_tenure=180, processing_fee='1%',    approval_time='10 days', min_cibil=650, is_featured=True),
        dict(name='HDFC Bank',     loan_type='lap', rate_min=9.50,  rate_max=11.00, max_amount=50000000, max_tenure=180, processing_fee='1%',    approval_time='7 days',  min_cibil=700),
        dict(name='ICICI Bank',    loan_type='lap', rate_min=9.85,  rate_max=11.90, max_amount=50000000, max_tenure=180, processing_fee='1%',    approval_time='7 days',  min_cibil=700),
        dict(name='Bajaj Finserv', loan_type='lap', rate_min=9.75,  rate_max=18.00, max_amount=50000000, max_tenure=240, processing_fee='1.5%',  approval_time='5 days',  min_cibil=685),
    ]

    for ld in lenders_data:
        db.session.add(Lender(**ld))
    db.session.commit()
    print(f"✅ Seeded {len(lenders_data)} lenders")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_lenders()
        print("✅ Database ready")
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
