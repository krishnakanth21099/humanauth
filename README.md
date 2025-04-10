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
├── api/                      # Django API app
│   ├── challenge_logic/      # Challenge generation and scoring
│   ├── models/               # Database models
│   ├── views.py              # API views
│   ├── serializers.py        # API serializers
│   └── urls.py               # API URL routing
├── frontend/                 # Frontend files
│   ├── static/               # Static assets
│   │   ├── challenges/       # Challenge templates and assets
│   │   ├── tracker.js        # Behavior tracking
│   │   ├── puzzle.js         # Challenge rendering
│   │   └── styles.css        # CSS styles
│   └── public/               # Public HTML files
├── humanauth/                # Django project settings
├── scripts/                  # Utility scripts
│   ├── seed_challenges.py    # Generate challenge templates
│   ├── generate_dataset.py   # Generate ML training datasets
│   ├── scoring_model.py      # ML model for trust scoring
│   ├── test_api.ps1          # PowerShell API test script
│   └── test_api.sh           # Bash API test script
├── templates/                # Django templates
├── tests/                    # Test files
├── .env                      # Environment variables
├── .gitignore                # Git ignore file
├── API_DOCUMENTATION.md      # API documentation
├── manage.py                 # Django management script
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/humanauth.git
   cd humanauth
   ```

2. Create a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   # Django settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here

   # Database settings
   # PostgreSQL configuration
   DATABASE_URL=postgres://postgres:password@localhost:5432/humanauth
   DB_NAME=humanauth
   DB_USER=postgres
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=5432

   # Redis settings
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   ```

5. Set up the database:
   ```bash
   # Create the PostgreSQL database
   # On Windows:
   # Use pgAdmin or run in PostgreSQL shell:
   # CREATE DATABASE humanauth;

   # On macOS/Linux:
   createdb humanauth

   # Run migrations
   python manage.py migrate
   ```

6. Seed challenge templates:
   ```bash
   python scripts/seed_challenges.py
   ```

### Running the Application

1. Start Redis Server:
   Make sure Redis is running on your system:

   ```bash
   # On Windows:
   # Start Redis server using the Redis Windows Service or Redis CLI

   # On macOS (using Homebrew):
   brew services start redis

   # On Linux:
   sudo service redis-server start
   # or
   sudo systemctl start redis
   ```

2. Start the Django Development Server:
   ```bash
   python manage.py runserver
   ```

3. Access the application:
   - CAPTCHA Demo: http://localhost:8000/captcha/ or http://localhost:8000/
   - API Endpoints: http://localhost:8000/api/

## API Documentation

The API documentation is available in the `API_DOCUMENTATION.md` file, which includes details on all endpoints and example requests.

### Quick API Overview

- `POST /api/init-session/`: Initialize a user session
- `GET /api/get-challenge/`: Get a random challenge
- `POST /api/submit-challenge/`: Submit a challenge response
- `GET /api/trust-score/{session_id}/`: Get the trust score for a session

### Testing the API

The project includes test scripts for both PowerShell and Bash:

```bash
# PowerShell
.\scripts\test_api.ps1

# Bash
./scripts/test_api.sh
```

You can also test the API manually using the cURL commands provided in the API documentation.

## Development

### Adding New Challenge Types

To add a new challenge type:

1. Add the challenge type to `CHALLENGE_TYPES` in `api/challenge_logic/generator.py`
2. Create a new generator method in the `ChallengeGenerator` class
3. Add a scoring method in the `ScoringEngine` class
4. Implement the frontend rendering in `frontend/static/puzzle.js`

### Customizing Scoring

You can customize the scoring weights in the `ScoringEngine` class:

```python
# api/challenge_logic/scoring.py
self.weights = {
    'correctness': 0.4,
    'entropy': 0.3,
    'response_time': 0.3
}
```

## Troubleshooting

### Redis Connection Issues

If you encounter Redis connection errors:

1. Make sure Redis is running on your system
2. Check the Redis connection settings in your `.env` file
3. Try connecting to Redis manually to verify it's working

### Database Issues

If you encounter database connection issues:

1. Verify your PostgreSQL server is running
2. Check the database connection settings in your `.env` file
3. Make sure the database exists and the user has appropriate permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FingerprintJS](https://fingerprint.com) for browser fingerprinting
- [Django REST Framework](https://www.django-rest-framework.org/) for API development
