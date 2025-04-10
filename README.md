# Humanauth - Advanced CAPTCHA System

Humanauth is a complete fullstack CAPTCHA system that distinguishes humans from bots and AI agents using behavior, cognition, and interaction patterns.

## Features

- Multiple challenge types:
  - Drag-align: Drag shapes to align with their outlines
  - Reverse-turing: Identify which text was written by a human vs AI
  - Reaction-tap: Tap/click targets that appear at random intervals
  - Vibe-match: Match the emotional tone of provided text samples
  - Pattern-completion: Complete a visual or logical pattern sequence
  - Audio-captcha: Identify spoken words or sounds in background noise
  - Semantic-grouping: Group related items together based on meaning

- Advanced behavior tracking:
  - Mouse movement analysis
  - Keystroke timing patterns
  - Touch interaction patterns
  - Scroll behavior

- Sophisticated scoring engine:
  - Combines correctness, behavior entropy, and response time
  - Customizable weights and thresholds
  - Machine learning ready

- Browser fingerprinting:
  - Headless browser detection
  - Device and browser identification
  - Entropy scoring

## Technology Stack

- **Backend**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Caching**: Redis
- **Frontend**: Vanilla JavaScript with HTML5 Canvas
- **Styling**: Custom CSS

## Project Structure

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

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (optional)
- Redis (optional)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/humanauth.git
   cd humanauth
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   
   # Database settings (optional)
   DATABASE_URL=postgres://user:password@localhost:5432/humanauth
   
   # Redis settings (optional)
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Seed challenge templates:
   ```
   python scripts/seed_challenges.py
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the CAPTCHA demo at:
   ```
   http://localhost:8000/frontend/public/captcha.html
   ```

## API Endpoints

- `POST /api/init-session/`: Initialize a user session
- `GET /api/get-challenge/`: Get a random challenge
- `POST /api/submit-challenge/`: Submit a challenge response
- `GET /api/trust-score/{session_id}/`: Get the trust score for a session

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FingerprintJS](https://fingerprint.com) for browser fingerprinting
- [Django REST Framework](https://www.django-rest-framework.org/) for API development
