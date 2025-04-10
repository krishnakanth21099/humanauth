import math
import numpy as np
from django.conf import settings


class ScoringEngine:
    """
    Calculates trust scores based on challenge responses and behavior data.
    """

    # Threshold for failing a challenge
    FAIL_THRESHOLD = 0.65

    def __init__(self):
        # Weights for different scoring components
        self.weights = {
            'correctness': 0.4,
            'entropy': 0.3,
            'response_time': 0.3
        }

    def calculate_trust_score(self, challenge_data, response_data, behavior_data):
        """
        Calculate a trust score based on challenge response and behavior.

        Args:
            challenge_data: The original challenge data with answers
            response_data: The user's response to the challenge
            behavior_data: Tracking data about user behavior during the challenge

        Returns:
            float: A trust score between 0 and 1
        """
        # Calculate individual component scores
        correctness_score = self._calculate_correctness_score(challenge_data, response_data)
        entropy_score = self._calculate_entropy_score(behavior_data)

        # Get time_taken_ms from response_data or use a default value
        time_taken_ms = response_data.get('time_taken_ms')
        if time_taken_ms is None and 'behavior_data' in response_data:
            # Try to get it from behavior_data if available
            time_taken_ms = response_data['behavior_data'].get('total_tracking_time_ms')

        # Use a default value if still not found
        if time_taken_ms is None:
            time_taken_ms = 5000  # Default to 5 seconds

        # Add time_taken_ms to response_data for future reference
        response_data['time_taken_ms'] = time_taken_ms

        response_time_score = self._calculate_response_time_score(time_taken_ms, challenge_data['type'])

        # Calculate weighted total score
        total_score = (
            correctness_score * self.weights['correctness'] +
            entropy_score * self.weights['entropy'] +
            response_time_score * self.weights['response_time']
        )

        # Normalize to 0-1 range
        normalized_score = max(0, min(1, total_score))

        return normalized_score

    def _calculate_correctness_score(self, challenge_data, response_data):
        """
        Calculate a score based on the correctness of the response.
        """
        challenge_type = challenge_data['type']

        if challenge_type == 'drag-align':
            return self._score_drag_align(challenge_data, response_data)
        elif challenge_type == 'reverse-turing':
            return self._score_reverse_turing(challenge_data, response_data)
        elif challenge_type == 'reaction-tap':
            return self._score_reaction_tap(challenge_data, response_data)
        elif challenge_type == 'vibe-match':
            return self._score_vibe_match(challenge_data, response_data)
        elif challenge_type == 'pattern-completion':
            return self._score_pattern_completion(challenge_data, response_data)
        elif challenge_type == 'audio-captcha':
            return self._score_audio_captcha(challenge_data, response_data)
        elif challenge_type == 'semantic-grouping':
            return self._score_semantic_grouping(challenge_data, response_data)
        else:
            # Default fallback
            return 0.5

    def _score_drag_align(self, challenge_data, response_data):
        """
        Score drag-align challenge based on how close shapes are to their targets.
        """
        if 'positions' not in response_data:
            return 0

        total_distance = 0
        max_possible_distance = 0
        canvas_width = 400  # Default canvas width
        canvas_height = 300  # Default canvas height

        # Calculate diagonal of canvas for normalization
        canvas_diagonal = math.sqrt(canvas_width**2 + canvas_height**2)

        for shape in challenge_data['shapes']:
            shape_id = shape['id']

            # Find corresponding target
            target = next((t for t in challenge_data['targets']
                          if t['type'] == shape['type']), None)

            if not target or shape_id not in response_data['positions']:
                total_distance += canvas_diagonal  # Maximum penalty
                max_possible_distance += canvas_diagonal
                continue

            # Get final position of the shape
            final_pos = response_data['positions'][shape_id]

            # Calculate Euclidean distance to target
            distance = math.sqrt(
                (final_pos['x'] - target['x'])**2 +
                (final_pos['y'] - target['y'])**2
            )

            # Add to total distance
            total_distance += distance
            max_possible_distance += canvas_diagonal

        # Normalize score (0 = perfect alignment, 1 = maximum distance)
        normalized_distance = total_distance / max_possible_distance

        # Convert to score (1 = perfect, 0 = worst)
        return 1 - normalized_distance

    def _score_reverse_turing(self, challenge_data, response_data):
        """
        Score reverse-turing challenge based on correct identification.
        """
        if 'selected_id' not in response_data:
            return 0

        # Simple binary scoring
        if response_data['selected_id'] == challenge_data['answer']:
            return 1.0
        else:
            return 0.0

    def _score_reaction_tap(self, challenge_data, response_data):
        """
        Score reaction-tap challenge based on timing and accuracy.
        """
        if 'taps' not in response_data:
            return 0

        total_targets = len(challenge_data['targets'])
        if total_targets == 0:
            return 0

        taps = response_data['taps']
        correct_taps = 0
        reaction_times = []

        for target in challenge_data['targets']:
            target_id = target['id']

            # Check if this target was tapped
            if target_id in taps:
                tap_time = taps[target_id]
                appear_time = target['appear_after_ms']
                disappear_time = appear_time + target['disappear_after_ms']

                # Check if tap was within the valid time window
                if appear_time <= tap_time <= disappear_time:
                    correct_taps += 1
                    reaction_times.append(tap_time - appear_time)

        # Calculate accuracy score
        accuracy = correct_taps / total_targets

        # Calculate reaction time score if there were any correct taps
        if reaction_times:
            avg_reaction_time = sum(reaction_times) / len(reaction_times)
            # Normalize reaction time (faster is better)
            # Assume 800ms is excellent, 1500ms is average
            reaction_score = max(0, min(1, 1 - (avg_reaction_time - 300) / 1200))

            # Combine accuracy and reaction time
            return 0.7 * accuracy + 0.3 * reaction_score
        else:
            return accuracy

    def _score_vibe_match(self, challenge_data, response_data):
        """
        Score vibe-match challenge based on correct emotion identification.
        """
        if 'selected_emotion' not in response_data:
            return 0

        # Simple binary scoring
        if response_data['selected_emotion'] == challenge_data['answer']:
            return 1.0
        else:
            return 0.0

    def _score_pattern_completion(self, challenge_data, response_data):
        """
        Score pattern-completion challenge based on correct answer.
        """
        if 'selected_answer' not in response_data:
            return 0

        # Simple binary scoring
        if response_data['selected_answer'] == challenge_data['answer']:
            return 1.0
        else:
            return 0.0

    def _score_audio_captcha(self, challenge_data, response_data):
        """
        Score audio-captcha challenge based on correct word identification.
        """
        if 'selected_word' not in response_data:
            return 0

        # Simple binary scoring
        if response_data['selected_word'] == challenge_data['answer']:
            return 1.0
        else:
            return 0.0

    def _score_semantic_grouping(self, challenge_data, response_data):
        """
        Score semantic-grouping challenge based on correct categorization.
        """
        # Check if groupings exist in response data
        if 'groupings' not in response_data or not response_data['groupings']:
            print("No groupings found in response data:", response_data)
            return 0

        # Check if answer_map exists in challenge data
        if 'answer_map' not in challenge_data or not challenge_data['answer_map']:
            print("No answer_map found in challenge data:", challenge_data)
            return 0.5  # Default to neutral score if no answer map

        answer_map = challenge_data['answer_map']
        groupings = response_data['groupings']

        # Convert groupings to the right type if needed
        if isinstance(groupings, str):
            try:
                import json
                groupings = json.loads(groupings)
            except:
                print("Failed to parse groupings JSON:", groupings)
                return 0

        total_items = len(answer_map)
        if total_items == 0:
            return 0

        correct_groupings = 0

        for item_id, category in groupings.items():
            if item_id in answer_map and answer_map[item_id] == category:
                correct_groupings += 1

        score = correct_groupings / total_items
        print(f"Semantic grouping score: {score} ({correct_groupings}/{total_items} correct)")
        return score

    def _calculate_entropy_score(self, behavior_data):
        """
        Calculate entropy score based on user behavior data.

        Higher entropy (more natural, less predictable patterns) = higher score
        """
        if not behavior_data or 'mouse_movements' not in behavior_data:
            return 0.5  # Default score if no data

        mouse_movements = behavior_data.get('mouse_movements', [])
        keystroke_timings = behavior_data.get('keystroke_timings', [])

        # Calculate mouse movement entropy
        mouse_entropy = self._calculate_mouse_entropy(mouse_movements)

        # Calculate keystroke timing entropy if available
        if keystroke_timings:
            keystroke_entropy = self._calculate_keystroke_entropy(keystroke_timings)
            # Combine both entropy scores
            entropy_score = 0.7 * mouse_entropy + 0.3 * keystroke_entropy
        else:
            entropy_score = mouse_entropy

        return entropy_score

    def _calculate_mouse_entropy(self, mouse_movements):
        """
        Calculate entropy from mouse movement patterns.

        Bot-like movements tend to be too regular or too straight.
        """
        if len(mouse_movements) < 5:
            return 0.5  # Not enough data

        # Extract movement vectors (dx, dy)
        vectors = []
        for i in range(1, len(mouse_movements)):
            prev = mouse_movements[i-1]
            curr = mouse_movements[i]

            dx = curr['x'] - prev['x']
            dy = curr['y'] - prev['y']
            dt = curr['timestamp'] - prev['timestamp']

            if dt > 0:  # Avoid division by zero
                vectors.append({
                    'dx': dx,
                    'dy': dy,
                    'speed': math.sqrt(dx**2 + dy**2) / dt,
                    'dt': dt
                })

        if not vectors:
            return 0.5

        # Calculate statistics on movement vectors
        speeds = [v['speed'] for v in vectors]
        time_diffs = [v['dt'] for v in vectors]

        # Calculate variance in speed and timing
        speed_variance = np.var(speeds) if len(speeds) > 1 else 0
        timing_variance = np.var(time_diffs) if len(time_diffs) > 1 else 0

        # Calculate direction changes
        direction_changes = 0
        for i in range(1, len(vectors)):
            prev_angle = math.atan2(vectors[i-1]['dy'], vectors[i-1]['dx'])
            curr_angle = math.atan2(vectors[i]['dy'], vectors[i]['dx'])

            # Calculate angle difference
            angle_diff = abs(curr_angle - prev_angle)
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff

            # Count significant direction changes
            if angle_diff > 0.3:  # About 17 degrees
                direction_changes += 1

        direction_change_rate = direction_changes / len(vectors) if vectors else 0

        # Combine metrics into entropy score
        # Higher variance and moderate direction changes are more human-like

        # Normalize speed variance (higher is better, up to a point)
        speed_score = min(1.0, speed_variance / 5000)

        # Normalize timing variance (higher is better, up to a point)
        timing_score = min(1.0, timing_variance / 10000)

        # Direction changes should be in a "human" range
        # Too few or too many are suspicious
        direction_score = 1.0 - abs(direction_change_rate - 0.3) * 2
        direction_score = max(0, min(1, direction_score))

        # Combine scores
        entropy_score = 0.4 * speed_score + 0.3 * timing_score + 0.3 * direction_score

        return entropy_score

    def _calculate_keystroke_entropy(self, keystroke_timings):
        """
        Calculate entropy from keystroke timing patterns.
        """
        if len(keystroke_timings) < 3:
            return 0.5  # Not enough data

        # Calculate inter-key intervals
        intervals = []
        for i in range(1, len(keystroke_timings)):
            interval = keystroke_timings[i]['timestamp'] - keystroke_timings[i-1]['timestamp']
            intervals.append(interval)

        # Calculate variance in timing
        timing_variance = np.var(intervals) if len(intervals) > 1 else 0

        # Normalize (higher variance is more human-like, up to a point)
        entropy_score = min(1.0, timing_variance / 50000)

        return entropy_score

    def _calculate_response_time_score(self, time_taken_ms, challenge_type):
        """
        Calculate score based on response time.

        Too fast or too slow responses are suspicious.
        """
        # Define expected time ranges for different challenge types (in ms)
        expected_times = {
            'drag-align': {'min': 2000, 'max': 15000, 'optimal': 6000},
            'reverse-turing': {'min': 3000, 'max': 20000, 'optimal': 8000},
            'reaction-tap': {'min': 1500, 'max': 10000, 'optimal': 4000},
            'vibe-match': {'min': 2000, 'max': 12000, 'optimal': 5000},
            'pattern-completion': {'min': 3000, 'max': 20000, 'optimal': 8000},
            'audio-captcha': {'min': 2000, 'max': 15000, 'optimal': 6000},
            'semantic-grouping': {'min': 4000, 'max': 25000, 'optimal': 10000}
        }

        # Use default if challenge type not found
        time_range = expected_times.get(challenge_type, {'min': 2000, 'max': 15000, 'optimal': 6000})

        # Calculate score based on time taken
        if time_taken_ms < time_range['min']:
            # Too fast (suspicious)
            # Linear scaling from 0 at 0ms to 0.7 at min time
            return min(0.7, time_taken_ms / time_range['min'] * 0.7)

        elif time_taken_ms <= time_range['optimal']:
            # Optimal range (good)
            # Linear scaling from 0.7 at min time to 1.0 at optimal time
            progress = (time_taken_ms - time_range['min']) / (time_range['optimal'] - time_range['min'])
            return 0.7 + progress * 0.3

        elif time_taken_ms <= time_range['max']:
            # Slower than optimal but still acceptable
            # Linear scaling from 1.0 at optimal time to 0.7 at max time
            progress = (time_taken_ms - time_range['optimal']) / (time_range['max'] - time_range['optimal'])
            return 1.0 - progress * 0.3

        else:
            # Too slow (suspicious)
            # Linear scaling from 0.7 at max time to 0.3 at 2*max time
            if time_taken_ms <= 2 * time_range['max']:
                progress = (time_taken_ms - time_range['max']) / time_range['max']
                return 0.7 - progress * 0.4
            else:
                return 0.3

    def is_challenge_passed(self, trust_score):
        """
        Determine if a challenge is passed based on the trust score.
        """
        return trust_score >= self.FAIL_THRESHOLD
