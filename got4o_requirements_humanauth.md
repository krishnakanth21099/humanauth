
# got4o_requirements.md for Humanauth

### Goal
Build a complete fullstack CAPTCHA system ("Humanauth") that distinguishes humans from bots and AI agents using behavior, cognition, and interaction patterns.

---

## PART 1: Backend Setup (Django + DRF)

### 1.1 Django Project
- Create Django project: `humanauth`
- Create Django app: `api`
- Use Django REST Framework for all endpoints.
- Enable PostgreSQL as the primary DB.
- Add Redis support (for session caching and future ML task queue).
- Set up CORS for localhost:3000

### 1.2 Models
Implement the following models inside `api/models/`:

#### UserSession
```python
id: UUIDField (primary key)
fingerprint_id: CharField(128)
ip_address: GenericIPAddressField
trust_score: FloatField (nullable)
created_at: DateTimeField(auto_now_add=True)
```

#### ChallengeLog
```python
session: FK to UserSession
challenge_type: CharField(64)
challenge_data: JSONField
response_data: JSONField
passed: BooleanField
time_taken_ms: IntegerField
created_at: DateTimeField(auto_now_add=True)
```

#### Fingerprint
```python
id: UUIDField (primary key)
session: OneToOneField to UserSession
browser: CharField(128)
os: CharField(128)
headless: BooleanField
entropy_score: FloatField
```

---

## PART 2: API Endpoints (REST)

### 2.1 Init Session
`POST /api/init-session/`
Creates a user session and stores fingerprint + IP + headless info.

### 2.2 Get Challenge
`GET /api/get-challenge/`
Returns a randomized challenge from the pool.

### 2.3 Submit Challenge
`POST /api/submit-challenge/`
Validates response, calculates score, logs result.

### 2.4 Get Trust Score
`GET /api/trust-score/{session_id}/`
Returns the normalized trust score (float between 0–1).

---

## PART 3: Challenge Generator

### Generate puzzles dynamically using:
- JS-compatible JSON payloads (coordinates, shape IDs, etc.)
- Use a Python utility `challenge_logic/generator.py` to generate:
  - `drag-align`: Drag shapes to align with their outlines
  - `reverse-turing`: Identify which text was written by a human vs AI
  - `reaction-tap`: Tap/click targets that appear at random intervals
  - `vibe-match`: Match the emotional tone of provided text samples
  - `pattern-completion`: Complete a visual or logical pattern sequence
  - `audio-captcha`: Identify spoken words or sounds in background noise
  - `semantic-grouping`: Group related items together based on meaning

Store JSON templates under `static/challenges/` and rotate seeds.

---

## PART 4: Scoring Engine

### In `challenge_logic/scoring.py`:
- Accepts: behavior data, correctness, and time
- Calculates:
```python
total_score = (
    correctness * 0.4 +
    entropy_score * 0.3 +
    response_time_score * 0.3
)
```
- Returns trust score (float)
- Fail threshold: `score < 0.65`

---

## PART 5: Frontend (Vanilla JS or React)

- Track mouse, keystroke, scroll, and touch behavior
- Scripts:
  - `tracker.js`: behavior collector, entropy calc
  - `puzzle.js`: renders challenges (canvas / DOM)
- Use TailwindCSS for layout/styling

### Pages:
- `captcha.html`:
  - Loads challenge
  - Captures response
  - Sends behavior + result to backend

### Use fingerprinting:
- Add [FingerprintJS](https://fingerprint.com) integration
- Call during `/api/init-session/`

---

## PART 6: Static Assets

- Store all assets under `frontend/static/`
- Use `canvas` or `WebGL` for drawing if needed
- All challenge images (for reverse Turing) stored in `/static/challenges/img/`

---

## PART 7: Scripts

Create the following under `/scripts/`:
- `seed_challenges.py`: loads base challenge data
- `generate_dataset.py`: for future ML modeling
- `scoring_model.py`: prototype behavior scoring

---

## PART 8: Security Measures

- Obfuscate client-side JS
- No static challenge reuse (add seed entropy)
- Validate that users aren’t headless (browser flag detection)
- Rate limit challenge attempts per session/IP
- Use HTTPS, sign challenge payloads (optional)

---

## PART 9: Project Scaffolding

Directory should look like:

```
humanauth/
├── backend/
│   └── api/
│       ├── models/
│       ├── challenge_logic/
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
├── frontend/
│   ├── static/
│   │   ├── tracker.js
│   │   ├── puzzle.js
│   │   └── styles.css
│   ├── public/
│   │   └── captcha.html
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

---

## PART 10: Optional Enhancements

- Real-time trust re-scoring via WebSockets
- ML model training notebook with behavioral datasets
- Admin dashboard for monitoring sessions
- Auto-banning mechanism for low-trust agents
- Progressive difficulty adjustment based on user performance
- Multi-factor challenge sequences for high-security applications
- Behavioral biometrics analysis (typing patterns, mouse movements)
- Accessibility modes for users with disabilities
- Internationalization support for challenges
- Challenge difficulty scaling based on threat assessment

---

## Environment
- Python 3.11+
- Django 5.x
- PostgreSQL 14+
- Redis
- Node.js (if React used)

---

**Build Instructions:**
Build all parts above **in modular fashion**. Focus on clean separation:
- Challenge logic is independent
- Frontend JS calls API cleanly
- Models are extensible
- Future AI hooks should be scaffolded
