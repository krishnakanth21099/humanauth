import random
import json
import uuid
import os
from pathlib import Path
from django.conf import settings


class ChallengeGenerator:
    """
    Generates various types of CAPTCHA challenges.
    """
    
    CHALLENGE_TYPES = [
        'drag-align',
        'reverse-turing',
        'reaction-tap',
        'vibe-match',
        'pattern-completion',
        'audio-captcha',
        'semantic-grouping'
    ]
    
    def __init__(self):
        self.templates_dir = Path(settings.BASE_DIR) / 'frontend' / 'static' / 'challenges'
    
    def get_random_challenge(self):
        """
        Returns a random challenge from the available types.
        """
        challenge_type = random.choice(self.CHALLENGE_TYPES)
        return self.generate_challenge(challenge_type)
    
    def generate_challenge(self, challenge_type):
        """
        Generates a specific type of challenge.
        """
        if challenge_type not in self.CHALLENGE_TYPES:
            raise ValueError(f"Invalid challenge type: {challenge_type}")
        
        # Add entropy to each challenge
        entropy = str(uuid.uuid4())[:8]
        
        if challenge_type == 'drag-align':
            return self._generate_drag_align(entropy)
        elif challenge_type == 'reverse-turing':
            return self._generate_reverse_turing(entropy)
        elif challenge_type == 'reaction-tap':
            return self._generate_reaction_tap(entropy)
        elif challenge_type == 'vibe-match':
            return self._generate_vibe_match(entropy)
        elif challenge_type == 'pattern-completion':
            return self._generate_pattern_completion(entropy)
        elif challenge_type == 'audio-captcha':
            return self._generate_audio_captcha(entropy)
        elif challenge_type == 'semantic-grouping':
            return self._generate_semantic_grouping(entropy)
    
    def _generate_drag_align(self, entropy):
        """
        Generate a challenge where users drag shapes to align with outlines.
        """
        shapes = ['circle', 'square', 'triangle', 'star', 'hexagon']
        selected_shapes = random.sample(shapes, 3)
        
        challenge_data = {
            'type': 'drag-align',
            'entropy': entropy,
            'shapes': [],
            'targets': []
        }
        
        canvas_width = 400
        canvas_height = 300
        
        for i, shape in enumerate(selected_shapes):
            # Create a shape to drag
            shape_data = {
                'id': f'shape-{i}',
                'type': shape,
                'x': random.randint(50, canvas_width - 50),
                'y': random.randint(50, canvas_height - 50),
                'size': random.randint(30, 50)
            }
            challenge_data['shapes'].append(shape_data)
            
            # Create a target outline
            target_x = random.randint(50, canvas_width - 50)
            target_y = random.randint(50, canvas_height - 50)
            
            # Ensure targets don't overlap too much
            while any(abs(target_x - t['x']) < 60 and abs(target_y - t['y']) < 60 
                      for t in challenge_data['targets']):
                target_x = random.randint(50, canvas_width - 50)
                target_y = random.randint(50, canvas_height - 50)
            
            target_data = {
                'id': f'target-{i}',
                'type': shape,
                'x': target_x,
                'y': target_y,
                'size': shape_data['size'] + 5  # Slightly larger for outline
            }
            challenge_data['targets'].append(target_data)
        
        return challenge_data
    
    def _generate_reverse_turing(self, entropy):
        """
        Generate a challenge where users identify human vs AI-written text.
        """
        # Sample text pairs (human vs AI)
        text_pairs = [
            {
                'human': "I felt a mix of excitement and nervousness as I walked into the interview room, my hands slightly shaking.",
                'ai': "Upon entering the interview environment, I experienced a combination of anticipatory excitement and anxiety, with minor tremors in my upper extremities."
            },
            {
                'human': "The sunset painted the sky with streaks of orange and pink, reflecting off the calm water.",
                'ai': "The solar descent created a chromatic display of orange and pink hues across the celestial canvas, which was subsequently mirrored by the quiescent aquatic surface."
            },
            {
                'human': "My dog barked at the mailman again today, I really need to train him better.",
                'ai': "My canine companion vocalized at the postal service representative again during the current diurnal cycle, necessitating improved behavioral conditioning protocols."
            }
        ]
        
        selected_pair = random.choice(text_pairs)
        texts = [
            {'id': 'text-1', 'content': selected_pair['human']},
            {'id': 'text-2', 'content': selected_pair['ai']}
        ]
        random.shuffle(texts)
        
        # Store which one is human (for validation)
        human_text_id = texts[0]['id'] if texts[0]['content'] == selected_pair['human'] else texts[1]['id']
        
        challenge_data = {
            'type': 'reverse-turing',
            'entropy': entropy,
            'texts': texts,
            'instruction': "Select the text that was written by a human:",
            'answer': human_text_id  # This will be removed before sending to client
        }
        
        return challenge_data
    
    def _generate_reaction_tap(self, entropy):
        """
        Generate a challenge where users tap targets that appear at random intervals.
        """
        num_targets = random.randint(3, 5)
        canvas_width = 400
        canvas_height = 300
        
        targets = []
        for i in range(num_targets):
            target = {
                'id': f'target-{i}',
                'x': random.randint(50, canvas_width - 50),
                'y': random.randint(50, canvas_height - 50),
                'radius': random.randint(20, 40),
                'appear_after_ms': 500 + i * random.randint(800, 1200),
                'disappear_after_ms': 1000  # Time window to click
            }
            targets.append(target)
        
        challenge_data = {
            'type': 'reaction-tap',
            'entropy': entropy,
            'targets': targets,
            'canvas': {
                'width': canvas_width,
                'height': canvas_height
            },
            'instruction': "Tap each circle as quickly as you can after it appears"
        }
        
        return challenge_data
    
    def _generate_vibe_match(self, entropy):
        """
        Generate a challenge where users match the emotional tone of text samples.
        """
        emotions = ['happy', 'sad', 'angry', 'surprised', 'calm']
        text_samples = {
            'happy': [
                "Just got the best news ever! I can't stop smiling!",
                "What a beautiful day to be alive. Everything feels perfect."
            ],
            'sad': [
                "I miss how things used to be. Nothing feels the same anymore.",
                "Sometimes I just sit and remember better days."
            ],
            'angry': [
                "I can't believe they would do this after everything we've been through!",
                "This is absolutely unacceptable. I demand to speak to someone in charge."
            ],
            'surprised': [
                "Wait, what?! I never saw that coming!",
                "You're kidding me! That's absolutely incredible!"
            ],
            'calm': [
                "I'm at peace with whatever happens. It will all work out.",
                "Taking deep breaths and focusing on what matters."
            ]
        }
        
        # Select random emotion and text
        emotion = random.choice(emotions)
        text = random.choice(text_samples[emotion])
        
        # Create options (including the correct one)
        options = random.sample(emotions, 3)
        if emotion not in options:
            options[0] = emotion
        
        challenge_data = {
            'type': 'vibe-match',
            'entropy': entropy,
            'text': text,
            'options': options,
            'instruction': "What is the emotional tone of this text?",
            'answer': emotion  # This will be removed before sending to client
        }
        
        return challenge_data
    
    def _generate_pattern_completion(self, entropy):
        """
        Generate a challenge where users complete a visual or logical pattern.
        """
        pattern_types = ['sequence', 'grid']
        pattern_type = random.choice(pattern_types)
        
        if pattern_type == 'sequence':
            # Number sequence patterns
            patterns = [
                {
                    'sequence': [2, 4, 6, 8],
                    'next': 10,
                    'options': [9, 10, 12, 14],
                    'rule': 'Add 2'
                },
                {
                    'sequence': [3, 6, 12, 24],
                    'next': 48,
                    'options': [30, 36, 48, 54],
                    'rule': 'Multiply by 2'
                },
                {
                    'sequence': [1, 3, 6, 10],
                    'next': 15,
                    'options': [13, 14, 15, 16],
                    'rule': 'Triangular numbers'
                }
            ]
            
            selected_pattern = random.choice(patterns)
            
            challenge_data = {
                'type': 'pattern-completion',
                'entropy': entropy,
                'pattern_type': 'sequence',
                'sequence': selected_pattern['sequence'],
                'options': selected_pattern['options'],
                'instruction': "What number comes next in this sequence?",
                'answer': selected_pattern['next']  # This will be removed before sending to client
            }
        
        else:  # grid pattern
            # Simple 3x3 grid patterns with one missing cell
            grid_patterns = [
                {
                    'grid': [
                        ['circle', 'square', 'triangle'],
                        ['square', 'triangle', 'circle'],
                        ['triangle', None, 'square']
                    ],
                    'missing_value': 'circle',
                    'options': ['circle', 'square', 'triangle', 'star'],
                    'missing_position': [2, 1]
                },
                {
                    'grid': [
                        ['A', 'B', 'C'],
                        ['D', 'E', 'F'],
                        ['G', None, 'I']
                    ],
                    'missing_value': 'H',
                    'options': ['H', 'J', 'K', 'L'],
                    'missing_position': [2, 1]
                }
            ]
            
            selected_grid = random.choice(grid_patterns)
            
            challenge_data = {
                'type': 'pattern-completion',
                'entropy': entropy,
                'pattern_type': 'grid',
                'grid': selected_grid['grid'],
                'options': selected_grid['options'],
                'missing_position': selected_grid['missing_position'],
                'instruction': "What belongs in the empty cell?",
                'answer': selected_grid['missing_value']  # This will be removed before sending to client
            }
        
        return challenge_data
    
    def _generate_audio_captcha(self, entropy):
        """
        Generate a challenge where users identify spoken words or sounds.
        """
        # In a real implementation, this would reference actual audio files
        audio_options = [
            {'word': 'apple', 'file': 'apple.mp3', 'options': ['apple', 'orange', 'banana', 'grape']},
            {'word': 'seven', 'file': 'seven.mp3', 'options': ['seven', 'eleven', 'three', 'nine']},
            {'word': 'blue', 'file': 'blue.mp3', 'options': ['blue', 'red', 'green', 'yellow']}
        ]
        
        selected_audio = random.choice(audio_options)
        
        challenge_data = {
            'type': 'audio-captcha',
            'entropy': entropy,
            'audio_file': f"/static/challenges/audio/{selected_audio['file']}",
            'options': selected_audio['options'],
            'instruction': "Listen to the audio and select the word you hear",
            'answer': selected_audio['word']  # This will be removed before sending to client
        }
        
        return challenge_data
    
    def _generate_semantic_grouping(self, entropy):
        """
        Generate a challenge where users group related items together.
        """
        categories = [
            {
                'name': 'Fruits',
                'items': ['apple', 'banana', 'orange', 'grape']
            },
            {
                'name': 'Vehicles',
                'items': ['car', 'bus', 'train', 'bicycle']
            },
            {
                'name': 'Animals',
                'items': ['dog', 'cat', 'elephant', 'tiger']
            }
        ]
        
        # Select two random categories
        selected_categories = random.sample(categories, 2)
        
        # Mix items from both categories
        all_items = []
        for category in selected_categories:
            for item in category['items']:
                all_items.append({
                    'id': f"item-{len(all_items)}",
                    'text': item,
                    'category': category['name']
                })
        
        random.shuffle(all_items)
        
        challenge_data = {
            'type': 'semantic-grouping',
            'entropy': entropy,
            'items': all_items,
            'categories': [cat['name'] for cat in selected_categories],
            'instruction': "Group these items into their correct categories"
        }
        
        # Create a mapping of correct answers (will be removed before sending to client)
        answer_map = {}
        for item in all_items:
            answer_map[item['id']] = item['category']
        
        challenge_data['answer_map'] = answer_map
        
        return challenge_data
    
    def prepare_challenge_for_client(self, challenge_data):
        """
        Removes answer data before sending to client.
        """
        client_data = challenge_data.copy()
        
        # Remove answer keys that shouldn't be sent to client
        keys_to_remove = ['answer', 'answer_map']
        for key in keys_to_remove:
            if key in client_data:
                del client_data[key]
        
        # For reverse-turing challenges, remove the human/AI indicators
        if client_data['type'] == 'reverse-turing':
            for text in client_data['texts']:
                if 'is_human' in text:
                    del text['is_human']
        
        return client_data
