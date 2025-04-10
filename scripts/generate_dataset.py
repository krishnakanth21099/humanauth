#!/usr/bin/env python
"""
Script to generate datasets for machine learning model training.
"""
import os
import sys
import json
import random
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the path so we can import Django settings
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'humanauth.settings')

import django
django.setup()

from api.models import UserSession, ChallengeLog


def generate_dataset():
    """
    Generate a dataset from challenge logs for ML training.
    """
    # Get all challenge logs
    challenge_logs = ChallengeLog.objects.all().select_related('session')
    
    if not challenge_logs:
        print("No challenge logs found in the database.")
        return
    
    # Prepare data for DataFrame
    data = []
    for log in challenge_logs:
        # Extract behavior data if available
        behavior_data = log.response_data.get('behavior_data', {})
        
        # Basic features
        row = {
            'session_id': str(log.session.id),
            'challenge_type': log.challenge_type,
            'passed': log.passed,
            'time_taken_ms': log.time_taken_ms,
            'trust_score': log.session.trust_score or 0.5,
            'created_at': log.created_at.isoformat(),
        }
        
        # Add browser fingerprint data if available
        try:
            fingerprint = log.session.fingerprint
            row.update({
                'browser': fingerprint.browser,
                'os': fingerprint.os,
                'headless': fingerprint.headless,
                'entropy_score': fingerprint.entropy_score,
            })
        except:
            pass
        
        # Add mouse movement features if available
        mouse_movements = behavior_data.get('mouse_movements', [])
        if mouse_movements:
            # Calculate movement statistics
            speeds = []
            angles = []
            for i in range(1, len(mouse_movements)):
                prev = mouse_movements[i-1]
                curr = mouse_movements[i]
                
                dx = curr['x'] - prev['x']
                dy = curr['y'] - prev['y']
                dt = curr['timestamp'] - prev['timestamp']
                
                if dt > 0:
                    speed = (dx**2 + dy**2)**0.5 / dt
                    speeds.append(speed)
                
                # Calculate angle
                import math
                angle = math.atan2(dy, dx)
                angles.append(angle)
            
            if speeds:
                row.update({
                    'mouse_speed_mean': sum(speeds) / len(speeds),
                    'mouse_speed_std': pd.Series(speeds).std() if len(speeds) > 1 else 0,
                    'mouse_speed_max': max(speeds),
                    'mouse_movements_count': len(mouse_movements),
                })
            
            if angles and len(angles) > 1:
                # Calculate angle changes
                angle_changes = []
                for i in range(1, len(angles)):
                    change = abs(angles[i] - angles[i-1])
                    if change > math.pi:
                        change = 2 * math.pi - change
                    angle_changes.append(change)
                
                row.update({
                    'mouse_angle_change_mean': sum(angle_changes) / len(angle_changes),
                    'mouse_angle_change_std': pd.Series(angle_changes).std(),
                    'mouse_angle_change_max': max(angle_changes),
                })
        
        # Add keystroke features if available
        keystroke_timings = behavior_data.get('keystroke_timings', [])
        if keystroke_timings and len(keystroke_timings) > 1:
            intervals = []
            for i in range(1, len(keystroke_timings)):
                interval = keystroke_timings[i]['timestamp'] - keystroke_timings[i-1]['timestamp']
                intervals.append(interval)
            
            row.update({
                'keystroke_interval_mean': sum(intervals) / len(intervals),
                'keystroke_interval_std': pd.Series(intervals).std(),
                'keystroke_count': len(keystroke_timings),
            })
        
        data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_dir = Path(settings.BASE_DIR) / 'scripts' / 'datasets'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"challenge_dataset_{timestamp}.csv"
    
    df.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file}")
    print(f"Total records: {len(df)}")


if __name__ == "__main__":
    print("Generating dataset from challenge logs...")
    generate_dataset()
    print("Done!")
