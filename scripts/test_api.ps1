# PowerShell script to test the Humanauth API

# Base URL
$BASE_URL = "http://localhost:8000/api"

# Step 1: Initialize Session
Write-Host "Initializing session..." -ForegroundColor Cyan
$sessionData = @{
    fingerprint_id = "test-fingerprint-123"
    fingerprint = @{
        browser = "Chrome"
        os = "Windows"
        headless = $false
        entropy_score = 0.85
    }
} | ConvertTo-Json

$sessionResponse = Invoke-RestMethod -Uri "$BASE_URL/init-session/" -Method Post -ContentType "application/json" -Body $sessionData
Write-Host "Session Response:" -ForegroundColor Green
$sessionResponse | ConvertTo-Json
$SESSION_ID = $sessionResponse.session_id
Write-Host "Session ID: $SESSION_ID" -ForegroundColor Yellow

# Step 2: Get Challenge
Write-Host "`nGetting challenge..." -ForegroundColor Cyan
$challengeResponse = Invoke-RestMethod -Uri "$BASE_URL/get-challenge/?session_id=$SESSION_ID" -Method Get
Write-Host "Challenge Response:" -ForegroundColor Green
$challengeResponse | ConvertTo-Json -Depth 5
$CHALLENGE_TYPE = $challengeResponse.challenge.type
Write-Host "Challenge Type: $CHALLENGE_TYPE" -ForegroundColor Yellow

# Step 3: Submit Challenge
Write-Host "`nSubmitting challenge response..." -ForegroundColor Cyan

# Prepare response data based on challenge type
$responseData = @{}
$behaviorData = @{
    mouse_movements = @(
        @{ x = 100; y = 100; timestamp = 1620000000000 },
        @{ x = 150; y = 120; timestamp = 1620000000100 },
        @{ x = 200; y = 150; timestamp = 1620000000200 },
        @{ x = 250; y = 200; timestamp = 1620000000300 }
    )
    keystroke_timings = @()
    scroll_events = @()
    touch_events = @()
    total_tracking_time_ms = 5000
    entropy_score = 0.78
}

switch ($CHALLENGE_TYPE) {
    "drag-align" {
        $responseData = @{
            positions = @{
                "shape-0" = @{ x = 250; y = 200 }
                "shape-1" = @{ x = 150; y = 250 }
            }
        }
    }
    "reverse-turing" {
        $responseData = @{
            selected_id = "text-1"
        }
    }
    "reaction-tap" {
        $responseData = @{
            taps = @{
                "target-0" = 1620000001200
                "target-1" = 1620000002500
                "target-2" = 1620000003800
            }
        }
    }
    "vibe-match" {
        $responseData = @{
            selected_emotion = "happy"
        }
    }
    "pattern-completion" {
        $responseData = @{
            selected_answer = 48
        }
    }
    "audio-captcha" {
        $responseData = @{
            selected_word = "apple"
        }
    }
    "semantic-grouping" {
        $responseData = @{
            groupings = @{
                "item-0" = "Fruits"
                "item-1" = "Vehicles"
                "item-2" = "Fruits"
                "item-3" = "Vehicles"
            }
        }
    }
    default {
        Write-Host "Unknown challenge type: $CHALLENGE_TYPE" -ForegroundColor Red
        exit
    }
}

$submitData = @{
    session_id = $SESSION_ID
    challenge_type = $CHALLENGE_TYPE
    response_data = $responseData
    behavior_data = $behaviorData
    time_taken_ms = 5000
} | ConvertTo-Json -Depth 5

$submitResponse = Invoke-RestMethod -Uri "$BASE_URL/submit-challenge/" -Method Post -ContentType "application/json" -Body $submitData
Write-Host "Submit Response:" -ForegroundColor Green
$submitResponse | ConvertTo-Json

# Step 4: Get Trust Score
Write-Host "`nGetting trust score..." -ForegroundColor Cyan
$trustScoreResponse = Invoke-RestMethod -Uri "$BASE_URL/trust-score/$SESSION_ID/" -Method Get
Write-Host "Trust Score Response:" -ForegroundColor Green
$trustScoreResponse | ConvertTo-Json

Write-Host "`nTest completed!" -ForegroundColor Cyan
