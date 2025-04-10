#!/bin/bash

# Bash script to test the Humanauth API

# Base URL
BASE_URL="http://localhost:8000/api"

# Step 1: Initialize Session
echo -e "\e[36mInitializing session...\e[0m"
SESSION_RESPONSE=$(curl -s -X POST "$BASE_URL/init-session/" \
  -H "Content-Type: application/json" \
  -d '{
    "fingerprint_id": "test-fingerprint-123",
    "fingerprint": {
      "browser": "Chrome",
      "os": "Linux",
      "headless": false,
      "entropy_score": 0.85
    }
  }')

echo -e "\e[32mSession Response:\e[0m"
echo "$SESSION_RESPONSE" | json_pp 2>/dev/null || echo "$SESSION_RESPONSE"

# Extract session ID (requires jq)
if command -v jq &> /dev/null; then
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
    echo -e "\e[33mSession ID: $SESSION_ID\e[0m"
else
    echo "jq not found. Please manually set SESSION_ID from the response above."
    read -p "Enter session ID: " SESSION_ID
fi

# Step 2: Get Challenge
echo -e "\n\e[36mGetting challenge...\e[0m"
CHALLENGE_RESPONSE=$(curl -s -X GET "$BASE_URL/get-challenge/?session_id=$SESSION_ID")
echo -e "\e[32mChallenge Response:\e[0m"
echo "$CHALLENGE_RESPONSE" | json_pp 2>/dev/null || echo "$CHALLENGE_RESPONSE"

# Extract challenge type (requires jq)
if command -v jq &> /dev/null; then
    CHALLENGE_TYPE=$(echo "$CHALLENGE_RESPONSE" | jq -r '.challenge.type')
    echo -e "\e[33mChallenge type: $CHALLENGE_TYPE\e[0m"
else
    echo "jq not found. Please manually set CHALLENGE_TYPE from the response above."
    read -p "Enter challenge type: " CHALLENGE_TYPE
fi

# Step 3: Submit Challenge
echo -e "\n\e[36mSubmitting challenge response...\e[0m"

# Prepare response data based on challenge type
RESPONSE_DATA=""
case "$CHALLENGE_TYPE" in
    "drag-align")
        RESPONSE_DATA='"positions": {
            "shape-0": {"x": 250, "y": 200},
            "shape-1": {"x": 150, "y": 250}
          }'
        ;;
    "reverse-turing")
        RESPONSE_DATA='"selected_id": "text-1"'
        ;;
    "reaction-tap")
        RESPONSE_DATA='"taps": {
            "target-0": 1620000001200,
            "target-1": 1620000002500,
            "target-2": 1620000003800
          }'
        ;;
    "vibe-match")
        RESPONSE_DATA='"selected_emotion": "happy"'
        ;;
    "pattern-completion")
        RESPONSE_DATA='"selected_answer": 48'
        ;;
    "audio-captcha")
        RESPONSE_DATA='"selected_word": "apple"'
        ;;
    "semantic-grouping")
        RESPONSE_DATA='"groupings": {
            "item-0": "Fruits",
            "item-1": "Vehicles",
            "item-2": "Fruits",
            "item-3": "Vehicles"
          }'
        ;;
    *)
        echo -e "\e[31mUnknown challenge type: $CHALLENGE_TYPE\e[0m"
        exit 1
        ;;
esac

SUBMIT_RESPONSE=$(curl -s -X POST "$BASE_URL/submit-challenge/" \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"challenge_type\": \"$CHALLENGE_TYPE\",
    \"response_data\": {
      $RESPONSE_DATA
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

echo -e "\e[32mSubmit Response:\e[0m"
echo "$SUBMIT_RESPONSE" | json_pp 2>/dev/null || echo "$SUBMIT_RESPONSE"

# Step 4: Get Trust Score
echo -e "\n\e[36mGetting trust score...\e[0m"
TRUST_SCORE_RESPONSE=$(curl -s -X GET "$BASE_URL/trust-score/$SESSION_ID/")
echo -e "\e[32mTrust Score Response:\e[0m"
echo "$TRUST_SCORE_RESPONSE" | json_pp 2>/dev/null || echo "$TRUST_SCORE_RESPONSE"

echo -e "\n\e[36mTest completed!\e[0m"
