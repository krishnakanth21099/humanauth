#!/usr/bin/env python
"""
Script to seed challenge data into the database or static files.
"""
import os
import sys
import json
import random
from pathlib import Path

# Add the project root to the path so we can import Django settings
sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'humanauth.settings')

import django
django.setup()

from django.conf import settings
from api.challenge_logic.generator import ChallengeGenerator


def generate_challenge_templates():
    """
    Generate template challenges and save them to static files.
    """
    generator = ChallengeGenerator()
    challenges_dir = Path(settings.BASE_DIR) / 'frontend' / 'static' / 'challenges'
    
    # Create directory if it doesn't exist
    challenges_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate templates for each challenge type
    for challenge_type in generator.CHALLENGE_TYPES:
        print(f"Generating templates for {challenge_type}...")
        
        # Generate multiple templates for each type
        templates = []
        for i in range(5):  # Generate 5 templates per type
            challenge = generator.generate_challenge(challenge_type)
            # Remove answers before saving as template
            client_challenge = generator.prepare_challenge_for_client(challenge)
            templates.append(client_challenge)
        
        # Save to JSON file
        output_file = challenges_dir / f"{challenge_type}_templates.json"
        with open(output_file, 'w') as f:
            json.dump(templates, f, indent=2)
        
        print(f"Saved {len(templates)} templates to {output_file}")


if __name__ == "__main__":
    print("Seeding challenge templates...")
    generate_challenge_templates()
    print("Done!")
