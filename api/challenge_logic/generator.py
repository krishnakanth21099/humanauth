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
            },
            {
                'human': "I couldn't believe how crowded the beach was on such a cold day.",
                'ai': "The density of human presence at the coastal recreational area was remarkably incongruent with the suboptimal thermal conditions."
            },
            {
                'human': "The coffee shop was my favorite place to work because of the comfy chairs and free wifi.",
                'ai': "The caffeinated beverage establishment represented my preferred location for professional activities due to the ergonomically satisfactory seating arrangements and complimentary wireless internet connectivity."
            },
            {
                'human': "I missed the bus this morning and had to run all the way to school.",
                'ai': "I failed to synchronize with the public transportation vehicle during the ante-meridian hours, necessitating rapid bipedal locomotion to the educational institution."
            },
            {
                'human': "The movie was so boring that I fell asleep halfway through.",
                'ai': "The cinematic presentation exhibited such a profound absence of engaging qualities that it induced an involuntary state of unconsciousness at approximately the median point of its duration."
            },
            {
                'human': "She smiled when she saw the birthday cake with all the candles lit up.",
                'ai': "The female subject exhibited facial musculature contraction indicative of positive affect upon visual perception of the anniversary pastry adorned with illuminated wax cylinders."
            },
            {
                'human': "The old car broke down again on the highway during our road trip.",
                'ai': "The antiquated automotive conveyance experienced mechanical failure once more on the high-speed thoroughfare during our extended vehicular excursion."
            }
        ]

        # Generate a new pair if needed using patterns
        if random.random() < 0.3:  # 30% chance to generate a new pair
            human_templates = [
                "I {feeling} when {event}.",
                "The {object} was {adjective} because {reason}.",
                "We {action} at the {location} last {time_period}.",
                "{person} {action} and then {consequence}."
            ]

            ai_templates = [
                "This individual experienced {complex_feeling} upon the occurrence of {formal_event}.",
                "The aforementioned {formal_object} exhibited {complex_adjective} qualities attributable to {formal_reason}.",
                "We engaged in {formal_action} at the designated {formal_location} during the previous {formal_time_period}.",
                "The {person_formal} {formal_action} subsequently resulting in {formal_consequence}."
            ]

            # Word banks
            feelings = ["laughed", "cried", "smiled", "worried", "panicked", "relaxed"]
            complex_feelings = ["heightened amusement", "lachrymose response", "facial musculature contraction indicative of positive affect", "elevated anxiety", "acute stress response", "diminished tension"]

            events = ["I saw the puppy", "the test results came back", "we reached the top of the mountain", "the plane took off"]
            formal_events = ["visual perception of the juvenile canine", "receipt of the examination outcomes", "attainment of the summit of the geological elevation", "commencement of aerial transportation"]

            # Select templates and generate texts
            human_template = random.choice(human_templates)
            ai_template = random.choice(ai_templates)

            if "{feeling}" in human_template:
                feeling = random.choice(feelings)
                complex_feeling = random.choice(complex_feelings)
                event = random.choice(events)
                formal_event = random.choice(formal_events)

                human_text = human_template.format(feeling=feeling, event=event)
                ai_text = ai_template.format(complex_feeling=complex_feeling, formal_event=formal_event)

                # Add to text pairs
                text_pairs.append({
                    'human': human_text,
                    'ai': ai_text
                })

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
        emotions = ['happy', 'sad', 'angry', 'surprised', 'calm', 'excited', 'fearful', 'disgusted', 'confused', 'nostalgic']
        text_samples = {
            'happy': [
                "Just got the best news ever! I can't stop smiling!",
                "What a beautiful day to be alive. Everything feels perfect.",
                "I aced my exam! All that studying paid off!",
                "My best friend is coming to visit after two years apart!",
                "The party last night was amazing, I had so much fun!"
            ],
            'sad': [
                "I miss how things used to be. Nothing feels the same anymore.",
                "Sometimes I just sit and remember better days.",
                "The movie's ending made me cry for hours.",
                "I feel so alone even when I'm surrounded by people.",
                "It's been a year since we lost him, and it still hurts every day."
            ],
            'angry': [
                "I can't believe they would do this after everything we've been through!",
                "This is absolutely unacceptable. I demand to speak to someone in charge.",
                "They promised to fix it three weeks ago and still nothing!",
                "How dare they speak to me like that? Who do they think they are?",
                "I'm so fed up with being treated like I don't matter!"
            ],
            'surprised': [
                "Wait, what?! I never saw that coming!",
                "You're kidding me! That's absolutely incredible!",
                "No way! After all this time, they finally did it?",
                "I can't believe my eyes! Is this really happening?",
                "Whoa! That plot twist completely blindsided me!"
            ],
            'calm': [
                "I'm at peace with whatever happens. It will all work out.",
                "Taking deep breaths and focusing on what matters.",
                "The gentle sound of rain helps me find my center.",
                "One step at a time, no need to rush through life.",
                "I've learned to accept things I cannot change."
            ],
            'excited': [
                "I can't wait for the concert tomorrow! I've been counting down for months!",
                "Just booked tickets for my dream vacation! This is happening!",
                "The package I've been waiting for is finally out for delivery!",
                "Only one more day until the season finale! I have so many theories!",
                "We're launching the project next week and I'm so pumped!"
            ],
            'fearful': [
                "I keep hearing strange noises from the basement when I'm alone.",
                "The deadline is tomorrow and I'm nowhere near finished.",
                "What if they find out I made a huge mistake?",
                "The turbulence on this flight is getting worse and worse.",
                "I'm terrified of what the test results might show."
            ],
            'disgusted': [
                "I found mold growing all over the leftovers in the fridge. Gross!",
                "The public bathroom was absolutely revolting. I couldn't even use it.",
                "Who would leave their trash all over the beach like this?",
                "That smell is making me sick to my stomach.",
                "I can't believe people actually eat that. It looks horrible."
            ],
            'confused': [
                "Wait, so who is related to whom? I'm completely lost.",
                "I've read the instructions three times and still don't understand.",
                "How did I end up on this website? I was looking for something completely different.",
                "The professor's explanation just made me more confused than before.",
                "I thought we agreed to meet at 7, but now they're saying 8?"
            ],
            'nostalgic': [
                "Finding my old yearbook brought back so many memories.",
                "That song always takes me back to summer camp when I was 12.",
                "The smell of fresh cookies reminds me of weekends at grandma's house.",
                "Looking through these old photos makes me miss simpler times.",
                "I wish I could go back to those carefree college days just once."
            ]
        }

        # Decide whether to use a template or a predefined text
        if random.random() < 0.3:  # 30% chance to generate a new text
            # Templates for different emotions
            templates = {
                'happy': [
                    "I just {positive_action} and now I'm {positive_feeling}!",
                    "What a {positive_adjective} day! Everything is {positive_state}.",
                    "I can't believe I finally {achievement}! {celebration}!"
                ],
                'sad': [
                    "I {negative_action} and now I feel so {sad_feeling}.",
                    "Everything seems so {sad_adjective} lately. I just want to {sad_action}.",
                    "I miss {missed_thing} so much. Nothing is the same without {it_them}."
                ],
                'angry': [
                    "I can't believe they {bad_action}! After all the {good_thing} I've done!",
                    "This is completely {negative_adjective}! I'm going to {angry_action}!",
                    "How many times do I have to tell them not to {annoying_action}?!"
                ],
                'surprised': [
                    "Wait, what?! Did you just say {unexpected_thing}?!",
                    "I can't believe {unexpected_event} actually happened!",
                    "No way! {person} did WHAT?! That's {surprising_adjective}!"
                ],
                'calm': [
                    "I'm {peaceful_state} with whatever happens. {philosophical_statement}.",
                    "{peaceful_action} helps me stay centered and {positive_state}.",
                    "One day at a time. {calm_philosophy}."
                ]
            }

            # Word banks for templates
            word_banks = {
                'positive_action': ['got a promotion', 'won the lottery', 'finished my project', 'met my idol', 'adopted a puppy'],
                'positive_feeling': ['over the moon', 'ecstatic', 'so happy', 'thrilled', 'on cloud nine'],
                'positive_adjective': ['wonderful', 'amazing', 'fantastic', 'beautiful', 'perfect', 'glorious'],
                'positive_state': ['going great', 'better than ever', 'absolutely perfect', 'falling into place', 'bringing me joy'],
                'achievement': ['got my dream job', 'finished my novel', 'ran a marathon', 'learned to play the guitar', 'graduated'],
                'celebration': ["I can't stop smiling", "This calls for a celebration", "I'm so proud of myself", "Dreams do come true", "Hard work pays off"],

                'negative_action': ['lost my job', 'failed my exam', 'missed my chance', 'broke my favorite mug', 'argued with my best friend'],
                'sad_feeling': ['empty', 'heartbroken', 'down', 'miserable', 'hopeless'],
                'sad_adjective': ['gray', 'meaningless', 'pointless', 'lonely', 'bleak'],
                'sad_action': ['be alone', 'cry', 'sleep all day', 'give up', 'disappear'],
                'missed_thing': ['how things used to be', 'my old friends', 'simpler times', 'the way we were', 'that feeling'],
                'it_them': ['it', 'them', 'those days', 'that person', 'what we had'],

                'bad_action': ['lied to me', 'broke their promise', 'took credit for my work', 'ignored my messages', 'betrayed my trust'],
                'good_thing': ['help', 'support', 'hard work', 'loyalty', 'kindness'],
                'negative_adjective': ['unacceptable', 'ridiculous', 'outrageous', 'infuriating', 'insulting'],
                'angry_action': ['demand a refund', 'speak to the manager', 'file a complaint', 'tell everyone about this', 'never shop there again'],
                'annoying_action': ['leave dirty dishes in the sink', 'interrupt me', 'borrow my things without asking', 'be late', 'ignore the rules'],

                'unexpected_thing': ["we won the championship", "you're getting married", "they're moving to Paris", "the company is shutting down", "he's actually a secret agent"],
                'unexpected_event': ['the underdog team winning', 'the surprise ending', 'the plot twist', 'the sudden announcement', 'the shocking revelation'],
                'person': ['My quiet neighbor', 'The new intern', 'Our strict teacher', 'The shy classmate', 'That celebrity'],
                'surprising_adjective': ['unbelievable', 'mind-blowing', 'shocking', 'incredible', 'insane'],

                'peaceful_state': ['at peace', 'content', 'accepting', 'serene', 'tranquil'],
                'philosophical_statement': ['Everything happens for a reason', 'This too shall pass', 'Life finds a way', 'The universe has a plan', 'We are where we need to be'],
                'peaceful_action': ['Meditation', 'Deep breathing', 'Yoga', 'Walking in nature', 'Mindfulness'],
                'calm_philosophy': ['Focus on what you can control', 'Accept what cannot be changed', 'Find joy in small things', 'The present is a gift', 'Patience brings wisdom']
            }

            # Select a random emotion from the available templates
            available_emotions = list(templates.keys())
            emotion = random.choice(available_emotions)

            # Select a random template for that emotion
            template = random.choice(templates[emotion])

            # Fill in the template with random words from the word banks
            text = template
            for placeholder, options in word_banks.items():
                if '{' + placeholder + '}' in text:
                    text = text.replace('{' + placeholder + '}', random.choice(options))

            # Add the generated text to the samples
            text_samples[emotion].append(text)
        else:
            # Select random emotion and text from predefined samples
            emotion = random.choice(emotions)
            text = random.choice(text_samples[emotion])

        # Create options (including the correct one)
        num_options = min(4, len(emotions))  # Use 4 options or fewer if not enough emotions
        options = random.sample(emotions, num_options)
        if emotion not in options:
            options[0] = emotion
        random.shuffle(options)

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
            # Decide whether to use a predefined pattern or generate one
            if random.random() < 0.6:  # 60% chance to generate a new sequence
                # Generate a new sequence based on common mathematical patterns
                sequence_types = [
                    'arithmetic',  # Add/subtract a constant
                    'geometric',  # Multiply/divide by a constant
                    'fibonacci',  # Each number is the sum of the two preceding ones
                    'square',     # Square numbers
                    'cube',       # Cube numbers
                    'alternating' # Alternating between two patterns
                ]

                seq_type = random.choice(sequence_types)
                sequence = []
                next_value = 0
                rule = ""

                if seq_type == 'arithmetic':
                    # Arithmetic sequence: a, a+d, a+2d, a+3d, ...
                    start = random.randint(1, 10)
                    diff = random.randint(2, 5)
                    sequence = [start + i * diff for i in range(4)]
                    next_value = start + 4 * diff
                    rule = f"Add {diff}"

                elif seq_type == 'geometric':
                    # Geometric sequence: a, ar, ar², ar³, ...
                    start = random.randint(1, 3)
                    ratio = random.randint(2, 3)
                    sequence = [start * (ratio ** i) for i in range(4)]
                    next_value = start * (ratio ** 4)
                    rule = f"Multiply by {ratio}"

                elif seq_type == 'fibonacci':
                    # Fibonacci-like sequence: a, b, a+b, a+2b, 2a+3b, ...
                    a = random.randint(1, 5)
                    b = random.randint(1, 5)
                    sequence = [a, b]
                    for i in range(2):
                        sequence.append(sequence[i] + sequence[i+1])
                    next_value = sequence[2] + sequence[3]
                    rule = "Each number is the sum of the two preceding ones"

                elif seq_type == 'square':
                    # Square numbers with offset: a, a+b², a+b²+c², ...
                    offset = random.randint(1, 5)
                    sequence = [offset + i**2 for i in range(1, 5)]
                    next_value = offset + 5**2
                    rule = "Add the square of the position number"

                elif seq_type == 'cube':
                    # Cube numbers: 1³, 2³, 3³, 4³, ...
                    sequence = [i**3 for i in range(1, 5)]
                    next_value = 5**3
                    rule = "Cube of position number"

                elif seq_type == 'alternating':
                    # Alternating pattern: +a, -b, +a, -b, ...
                    start = random.randint(5, 15)
                    add = random.randint(3, 8)
                    subtract = random.randint(1, 5)
                    sequence = [start]
                    for i in range(3):
                        if i % 2 == 0:
                            sequence.append(sequence[-1] - subtract)
                        else:
                            sequence.append(sequence[-1] + add)

                    if len(sequence) % 2 == 1:  # If last operation was subtract
                        next_value = sequence[-1] + add
                    else:  # If last operation was add
                        next_value = sequence[-1] - subtract
                    rule = f"Alternating: +{add}, -{subtract}"

                # Generate plausible wrong options
                options = [next_value]
                while len(options) < 4:
                    # Add some plausible wrong answers
                    if seq_type == 'arithmetic':
                        wrong = next_value + random.choice([-diff*2, -diff, diff, diff*2])
                    elif seq_type == 'geometric':
                        wrong = next_value * random.choice([0.5, 0.75, 1.25, 1.5])
                        wrong = int(wrong)
                    else:
                        # For other types, add/subtract a small amount
                        wrong = next_value + random.choice([-3, -2, -1, 1, 2, 3])

                    if wrong not in options and wrong > 0:
                        options.append(wrong)

                random.shuffle(options)
            else:
                # Use predefined patterns
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
                    },
                    {
                        'sequence': [1, 4, 9, 16],
                        'next': 25,
                        'options': [20, 25, 30, 36],
                        'rule': 'Square numbers'
                    },
                    {
                        'sequence': [1, 8, 27, 64],
                        'next': 125,
                        'options': [100, 125, 150, 216],
                        'rule': 'Cube numbers'
                    },
                    {
                        'sequence': [2, 3, 5, 8],
                        'next': 13,
                        'options': [11, 12, 13, 15],
                        'rule': 'Fibonacci sequence'
                    }
                ]

                selected_pattern = random.choice(patterns)
                sequence = selected_pattern['sequence']
                next_value = selected_pattern['next']
                options = selected_pattern['options']

            challenge_data = {
                'type': 'pattern-completion',
                'entropy': entropy,
                'pattern_type': 'sequence',
                'sequence': sequence,
                'options': options,
                'instruction': "What number comes next in this sequence?",
                'answer': next_value  # This will be removed before sending to client
            }

        else:  # grid pattern
            # Decide whether to use a predefined grid or generate one
            if random.random() < 0.5:  # 50% chance to generate a new grid
                # Generate a new grid pattern
                grid_size = 3  # 3x3 grid
                grid_types = ['rotation', 'symbol_pattern', 'letter_pattern']
                grid_type = random.choice(grid_types)

                if grid_type == 'rotation':
                    # Create a pattern where symbols rotate through positions
                    symbols = ['circle', 'square', 'triangle', 'star', 'hexagon', 'diamond']
                    selected_symbols = random.sample(symbols, 3)

                    # Create the grid with a rotation pattern
                    grid = [
                        [selected_symbols[0], selected_symbols[1], selected_symbols[2]],
                        [selected_symbols[2], selected_symbols[0], selected_symbols[1]],
                        [selected_symbols[1], None, selected_symbols[0]]
                    ]

                    missing_value = selected_symbols[2]
                    options = selected_symbols + [random.choice([s for s in symbols if s not in selected_symbols])]
                    missing_position = [2, 1]

                elif grid_type == 'symbol_pattern':
                    # Create a pattern based on symbol relationships
                    symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

                    # Select 8 symbols for the grid (the 9th will be missing)
                    selected_symbols = random.sample(symbols, 9)

                    # Create the grid with a pattern (e.g., alphabetical order)
                    grid = [
                        [selected_symbols[0], selected_symbols[1], selected_symbols[2]],
                        [selected_symbols[3], selected_symbols[4], selected_symbols[5]],
                        [selected_symbols[6], None, selected_symbols[8]]
                    ]

                    missing_value = selected_symbols[7]
                    options = [missing_value] + random.sample([s for s in symbols if s not in selected_symbols], 3)
                    missing_position = [2, 1]

                else:  # letter_pattern
                    # Create a pattern with letters
                    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

                    # Choose a starting letter
                    start_idx = random.randint(0, 20)  # Leave room for pattern

                    # Create a sequential pattern
                    grid = [
                        [letters[start_idx], letters[start_idx+1], letters[start_idx+2]],
                        [letters[start_idx+3], letters[start_idx+4], letters[start_idx+5]],
                        [letters[start_idx+6], None, letters[start_idx+8]]
                    ]

                    missing_value = letters[start_idx+7]
                    options = [missing_value] + random.sample([letters[i] for i in range(26) if letters[i] not in [letters[j] for j in range(start_idx, start_idx+9)]], 3)
                    missing_position = [2, 1]
            else:
                # Use predefined grid patterns
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
                    },
                    {
                        'grid': [
                            ['1', '2', '3'],
                            ['4', '5', '6'],
                            ['7', None, '9']
                        ],
                        'missing_value': '8',
                        'options': ['8', '0', 'X', 'Y'],
                        'missing_position': [2, 1]
                    },
                    {
                        'grid': [
                            ['red', 'blue', 'green'],
                            ['blue', 'green', 'red'],
                            ['green', None, 'blue']
                        ],
                        'missing_value': 'red',
                        'options': ['red', 'blue', 'green', 'yellow'],
                        'missing_position': [2, 1]
                    }
                ]

                selected_grid = random.choice(grid_patterns)
                grid = selected_grid['grid']
                missing_value = selected_grid['missing_value']
                options = selected_grid['options']
                missing_position = selected_grid['missing_position']

            challenge_data = {
                'type': 'pattern-completion',
                'entropy': entropy,
                'pattern_type': 'grid',
                'grid': grid,
                'options': options,
                'missing_position': missing_position,
                'instruction': "What belongs in the empty cell?",
                'answer': missing_value  # This will be removed before sending to client
            }

        return challenge_data

    def _generate_audio_captcha(self, entropy):
        """
        Generate a challenge where users identify spoken words or sounds.
        """
        # Since we don't have actual audio files, we'll use a text-based fallback
        # In a production environment, you would use real audio files
        audio_options = [
            {
                'word': 'apple',
                'file': 'apple.txt',
                'options': ['apple', 'orange', 'banana', 'grape'],
                'description': 'A common red or green fruit with a crisp texture'
            },
            {
                'word': 'seven',
                'file': 'seven.txt',
                'options': ['seven', 'eleven', 'three', 'nine'],
                'description': 'A number between six and eight'
            },
            {
                'word': 'blue',
                'file': 'blue.txt',
                'options': ['blue', 'red', 'green', 'yellow'],
                'description': 'The color of the sky on a clear day'
            },
            {
                'word': 'dog',
                'file': 'dog.txt',
                'options': ['dog', 'cat', 'bird', 'fish'],
                'description': 'A common pet that barks'
            },
            {
                'word': 'piano',
                'file': 'piano.txt',
                'options': ['piano', 'guitar', 'drums', 'violin'],
                'description': 'A musical instrument with black and white keys'
            },
            {
                'word': 'car',
                'file': 'car.txt',
                'options': ['car', 'bus', 'train', 'bike'],
                'description': 'A four-wheeled vehicle for personal transportation'
            }
        ]

        selected_audio = random.choice(audio_options)

        # Create a text file with the description if it doesn't exist
        audio_dir = Path(settings.BASE_DIR) / 'frontend' / 'static' / 'challenges' / 'audio'
        audio_file_path = audio_dir / selected_audio['file']

        if not audio_file_path.exists():
            try:
                with open(audio_file_path, 'w') as f:
                    f.write(selected_audio['description'])
            except Exception as e:
                print(f"Error creating audio text file: {e}")

        challenge_data = {
            'type': 'audio-captcha',
            'entropy': entropy,
            'audio_file': f"/static/challenges/audio/{selected_audio['file']}",
            'options': selected_audio['options'],
            'instruction': "AUDIO SIMULATION: " + selected_audio['description'] + ". Select the word being described:",
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
                'items': ['apple', 'banana', 'orange', 'grape', 'strawberry', 'pineapple', 'watermelon', 'kiwi', 'mango', 'peach']
            },
            {
                'name': 'Vegetables',
                'items': ['carrot', 'broccoli', 'spinach', 'potato', 'tomato', 'cucumber', 'lettuce', 'onion', 'pepper', 'corn']
            },
            {
                'name': 'Animals',
                'items': ['dog', 'cat', 'elephant', 'tiger', 'lion', 'giraffe', 'zebra', 'monkey', 'bear', 'wolf']
            },
            {
                'name': 'Birds',
                'items': ['eagle', 'sparrow', 'penguin', 'owl', 'parrot', 'flamingo', 'hawk', 'robin', 'swan', 'peacock']
            },
            {
                'name': 'Vehicles',
                'items': ['car', 'bus', 'train', 'bicycle', 'motorcycle', 'truck', 'airplane', 'helicopter', 'boat', 'submarine']
            },
            {
                'name': 'Furniture',
                'items': ['chair', 'table', 'bed', 'sofa', 'desk', 'bookshelf', 'cabinet', 'dresser', 'stool', 'wardrobe']
            },
            {
                'name': 'Countries',
                'items': ['USA', 'Canada', 'France', 'Japan', 'Brazil', 'Australia', 'India', 'Egypt', 'Mexico', 'Italy']
            },
            {
                'name': 'Sports',
                'items': ['soccer', 'basketball', 'tennis', 'swimming', 'baseball', 'golf', 'volleyball', 'hockey', 'skiing', 'boxing']
            },
            {
                'name': 'Instruments',
                'items': ['guitar', 'piano', 'violin', 'drums', 'flute', 'trumpet', 'saxophone', 'cello', 'harp', 'clarinet']
            },
            {
                'name': 'Professions',
                'items': ['doctor', 'teacher', 'engineer', 'chef', 'artist', 'pilot', 'firefighter', 'lawyer', 'scientist', 'actor']
            },
            {
                'name': 'Colors',
                'items': ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black', 'white']
            },
            {
                'name': 'Planets',
                'items': ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Moon']
            }
        ]

        # Decide how many categories to use (2 or 3)
        num_categories = random.choice([2, 3])

        # Select random categories
        selected_categories = random.sample(categories, num_categories)

        # Decide how many items per category (3-5)
        items_per_category = random.randint(3, 5)

        # Mix items from all selected categories
        all_items = []
        for category in selected_categories:
            # Select a subset of items from each category
            selected_items = random.sample(category['items'], items_per_category)
            for item in selected_items:
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
