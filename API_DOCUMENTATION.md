# Humanauth API Documentation

This document provides details on all the API endpoints available in the Humanauth CAPTCHA system.

## Base URL

All API endpoints are prefixed with `/api/`.

## Authentication

Currently, the API does not require authentication for testing purposes.

## API Endpoints

### 1. Initialize Session

Creates a new user session and stores fingerprint data.

- **URL**: `/api/init-session/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "fingerprint_id": "unique-browser-fingerprint-id",
    "fingerprint": {
      "browser": "Chrome",
      "os": "Windows",
      "headless": false,
      "entropy_score": 0.85
    }
  }
  ```
- **Response**:
  ```json
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Session initialized successfully"
  }
  ```
- **Status Codes**:
  - `201 Created`: Session created successfully
  - `400 Bad Request`: Invalid request data

### 2. Get Challenge

Retrieves a random CAPTCHA challenge.

- **URL**: `/api/get-challenge/`
- **Method**: `GET`
- **Query Parameters**:
  - `session_id`: UUID of the session
- **Example**: `/api/get-challenge/?session_id=550e8400-e29b-41d4-a716-446655440000`
- **Response**:
  ```json
  {
    "challenge": {
      "type": "drag-align",
      "entropy": "a1b2c3d4",
      "shapes": [
        {
          "id": "shape-0",
          "type": "circle",
          "x": 100,
          "y": 150,
          "size": 40
        },
        {
          "id": "shape-1",
          "type": "square",
          "x": 200,
          "y": 100,
          "size": 35
        }
      ],
      "targets": [
        {
          "id": "target-0",
          "type": "circle",
          "x": 250,
          "y": 200,
          "size": 45
        },
        {
          "id": "target-1",
          "type": "square",
          "x": 150,
          "y": 250,
          "size": 40
        }
      ]
    }
  }
  ```
- **Status Codes**:
  - `200 OK`: Challenge retrieved successfully
  - `400 Bad Request`: Invalid session ID format
  - `404 Not Found`: Session not found

### 3. Submit Challenge

Submits a challenge response and calculates trust score.

- **URL**: `/api/submit-challenge/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "challenge_type": "drag-align",
    "response_data": {
      "positions": {
        "shape-0": {"x": 250, "y": 200},
        "shape-1": {"x": 150, "y": 250}
      }
    },
    "behavior_data": {
      "mouse_movements": [
        {"x": 100, "y": 100, "timestamp": 1620000000000},
        {"x": 150, "y": 120, "timestamp": 1620000000100},
        {"x": 200, "y": 150, "timestamp": 1620000000200}
      ],
      "keystroke_timings": [
        {"timestamp": 1620000000300},
        {"timestamp": 1620000000450}
      ],
      "entropy_score": 0.78
    },
    "time_taken_ms": 5000
  }
  ```
- **Response**:
  ```json
  {
    "trust_score": 0.85,
    "passed": true
  }
  ```
- **Status Codes**:
  - `200 OK`: Challenge submitted successfully
  - `400 Bad Request`: Invalid request data or challenge expired
  - `404 Not Found`: Session not found

### 4. Get Trust Score

Retrieves the trust score for a session.

- **URL**: `/api/trust-score/{session_id}/`
- **Method**: `GET`
- **URL Parameters**:
  - `session_id`: UUID of the session
- **Example**: `/api/trust-score/550e8400-e29b-41d4-a716-446655440000/`
- **Response**:
  ```json
  {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "trust_score": 0.85,
    "passed": true
  }
  ```
- **Status Codes**:
  - `200 OK`: Trust score retrieved successfully
  - `404 Not Found`: Session not found

## Testing with cURL

Here are detailed examples of how to test the API using cURL. You can save these commands to a script file for easy testing.

### Initialize Session

```bash
# Initialize a new session and save the response to a file
curl -X POST http://localhost:8000/api/init-session/ \
  -H "Content-Type: application/json" \
  -d '{
    "fingerprint_id": "test-fingerprint-123",
    "fingerprint": {
      "browser": "Chrome",
      "os": "Windows",
      "headless": false,
      "entropy_score": 0.85
    }
  }' | tee session_response.json

# Extract the session_id from the response (requires jq)
SESSION_ID=$(cat session_response.json | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# Or manually set the session ID if you don't have jq
# SESSION_ID="your-session-id-here"
```

### Get Challenge

```bash
# Get a challenge for the session
curl -X GET "http://localhost:8000/api/get-challenge/?session_id=$SESSION_ID" | tee challenge_response.json

# For Windows PowerShell
# curl -X GET "http://localhost:8000/api/get-challenge/?session_id=$env:SESSION_ID" | Tee-Object -FilePath challenge_response.json
```

### Submit Challenge - Drag-Align

```bash
# Submit a drag-align challenge response
curl -X POST http://localhost:8000/api/submit-challenge/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"drag-align\",
    \"response_data\": {
      \"positions\": {
        \"shape-0\": {\"x\": 250, \"y\": 200},
        \"shape-1\": {\"x\": 150, \"y\": 250}
      }
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000000000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000000100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000000200},
        {\"x\": 250, \"y\": 200, \"timestamp\": 1620000000300}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 5000,
      \"entropy_score\": 0.78
    },
    \"time_taken_ms\": 5000
  }" | tee submit_response.json
```

### Submit Challenge - Reverse-Turing

```bash
# Submit a reverse-turing challenge response
curl -X POST http://localhost:8000/api/submit-challenge/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"reverse-turing\",
    \"response_data\": {
      \"selected_id\": \"text-1\"
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000000000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000000100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000000200}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [
        {\"scrollX\": 0, \"scrollY\": 100, \"timestamp\": 1620000000150}
      ],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 8000,
      \"entropy_score\": 0.82
    },
    \"time_taken_ms\": 8000
  }" | tee submit_response.json
```

### Submit Challenge - Reaction-Tap

```bash
# Submit a reaction-tap challenge response
curl -X POST http://localhost:8000/api/submit-challenge/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"reaction-tap\",
    \"response_data\": {
      \"taps\": {
        \"target-0\": 1620000001200,
        \"target-1\": 1620000002500,
        \"target-2\": 1620000003800
      }
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000001000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000001100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000002300},
        {\"x\": 250, \"y\": 200, \"timestamp\": 1620000003600}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 4000,
      \"entropy_score\": 0.75
    },
    \"time_taken_ms\": 4000
  }" | tee submit_response.json
```

### Submit Challenge - Vibe-Match

```bash
# Submit a vibe-match challenge response
curl -X POST http://localhost:8000/api/submit-challenge/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"vibe-match\",
    \"response_data\": {
      \"selected_emotion\": \"happy\"
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000000000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000000100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000000200}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 5000,
      \"entropy_score\": 0.80
    },
    \"time_taken_ms\": 5000
  }" | tee submit_response.json
```

### Submit Challenge - Pattern-Completion

```bash
# Submit a pattern-completion challenge response
curl -X POST http://localhost:8000/api/submit-challenge/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"pattern-completion\",
    \"response_data\": {
      \"selected_answer\": 48
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000000000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000000100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000000200}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 7000,
      \"entropy_score\": 0.76
    },
    \"time_taken_ms\": 7000
  }" | tee submit_response.json
```

### Get Trust Score

```bash
# Get the trust score for the session
curl -X GET "http://localhost:8000/api/trust-score/$SESSION_ID/" | tee trust_score_response.json

# For Windows PowerShell
# curl -X GET "http://localhost:8000/api/trust-score/$env:SESSION_ID/" | Tee-Object -FilePath trust_score_response.json
```

### Complete Test Script

Here's a complete bash script that tests all endpoints in sequence:

```bash
#!/bin/bash

# Base URL
BASE_URL="http://localhost:8000/api"

# Step 1: Initialize Session
echo "Initializing session..."
SESSION_RESPONSE=$(curl -s -X POST "$BASE_URL/init-session/" \
  -H "Content-Type: application/json" \
  -d '{
    "fingerprint_id": "test-fingerprint-123",
    "fingerprint": {
      "browser": "Chrome",
      "os": "Windows",
      "headless": false,
      "entropy_score": 0.85
    }
  }')

echo "$SESSION_RESPONSE"

# Extract session ID (requires jq)
if command -v jq &> /dev/null; then
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
    echo "Session ID: $SESSION_ID"
else
    echo "jq not found. Please manually set SESSION_ID from the response above."
    read -p "Enter session ID: " SESSION_ID
fi

# Step 2: Get Challenge
echo "\nGetting challenge..."
CHALLENGE_RESPONSE=$(curl -s -X GET "$BASE_URL/get-challenge/?session_id=$SESSION_ID")
echo "$CHALLENGE_RESPONSE"

# Extract challenge type (requires jq)
if command -v jq &> /dev/null; then
    CHALLENGE_TYPE=$(echo "$CHALLENGE_RESPONSE" | jq -r '.challenge.type')
    echo "Challenge type: $CHALLENGE_TYPE"
else
    echo "jq not found. Please manually set CHALLENGE_TYPE from the response above."
    read -p "Enter challenge type: " CHALLENGE_TYPE
fi

# Step 3: Submit Challenge
echo "\nSubmitting challenge response..."
SUBMIT_RESPONSE=$(curl -s -X POST "$BASE_URL/submit-challenge/" \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"$CHALLENGE_TYPE\",
    \"response_data\": {
      \"positions\": {
        \"shape-0\": {\"x\": 250, \"y\": 200},
        \"shape-1\": {\"x\": 150, \"y\": 250}
      }
    },
    \"behavior_data\": {
      \"mouse_movements\": [
        {\"x\": 100, \"y\": 100, \"timestamp\": 1620000000000},
        {\"x\": 150, \"y\": 120, \"timestamp\": 1620000000100},
        {\"x\": 200, \"y\": 150, \"timestamp\": 1620000000200}
      ],
      \"keystroke_timings\": [],
      \"scroll_events\": [],
      \"touch_events\": [],
      \"total_tracking_time_ms\": 5000,
      \"entropy_score\": 0.78
    },
    \"time_taken_ms\": 5000
  }")

echo "$SUBMIT_RESPONSE"

# Step 4: Get Trust Score
echo "\nGetting trust score..."
TRUST_SCORE_RESPONSE=$(curl -s -X GET "$BASE_URL/trust-score/$SESSION_ID/")
echo "$TRUST_SCORE_RESPONSE"

echo "\nTest completed!"
```

## Testing with Postman

You can also import the following Postman collection to test the API:

1. Create a new collection in Postman
2. Set up environment variables:
   - `base_url`: `http://localhost:8000`
   - `session_id`: (will be populated after initializing a session)

3. Add the following requests:

### Initialize Session
- Method: POST
- URL: {{base_url}}/api/init-session/
- Body (raw JSON):
```json
{
  "fingerprint_id": "test-fingerprint-123",
  "fingerprint": {
    "browser": "Chrome",
    "os": "Windows",
    "headless": false,
    "entropy_score": 0.85
  }
}
```
- Tests:
```javascript
var jsonData = JSON.parse(responseBody);
pm.environment.set("session_id", jsonData.session_id);
```

### Get Challenge
- Method: GET
- URL: {{base_url}}/api/get-challenge/?session_id={{session_id}}

### Submit Challenge
- Method: POST
- URL: {{base_url}}/api/submit-challenge/
- Body (raw JSON):
```json
{
  "session_id": "{{session_id}}",
  "challenge_type": "drag-align",
  "response_data": {
    "positions": {
      "shape-0": {"x": 250, "y": 200},
      "shape-1": {"x": 150, "y": 250}
    }
  },
  "behavior_data": {
    "mouse_movements": [
      {"x": 100, "y": 100, "timestamp": 1620000000000},
      {"x": 150, "y": 120, "timestamp": 1620000000100}
    ],
    "entropy_score": 0.78
  },
  "time_taken_ms": 5000
}
```

### Get Trust Score
- Method: GET
- URL: {{base_url}}/api/trust-score/{{session_id}}/
