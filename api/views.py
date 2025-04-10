from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings

from api.models import UserSession, ChallengeLog
from api.serializers import (
    UserSessionSerializer, ChallengeLogSerializer, TrustScoreSerializer,
    ChallengeRequestSerializer, ChallengeResponseSerializer
)
from api.challenge_logic.generator import ChallengeGenerator
from api.challenge_logic.scoring import ScoringEngine


class InitSessionView(APIView):
    """
    Initialize a new user session with fingerprint data.
    """
    def post(self, request):
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Add IP to request data
        data = request.data.copy()
        data['ip_address'] = ip_address

        serializer = UserSessionSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save()
            return Response({
                'session_id': session.id,
                'message': 'Session initialized successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetChallengeView(APIView):
    """
    Get a random challenge for the user.
    """
    def get(self, request):
        serializer = ChallengeRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        session_id = serializer.validated_data['session_id']

        # Check if session exists
        try:
            session = UserSession.objects.get(id=session_id)
        except UserSession.DoesNotExist:
            return Response({
                'error': 'Session not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Generate a random challenge
        generator = ChallengeGenerator()
        challenge_data = generator.get_random_challenge()

        # Store the original challenge with answers for later verification
        challenge_with_answers = challenge_data.copy()

        # Remove answers before sending to client
        client_challenge = generator.prepare_challenge_for_client(challenge_data)

        # Store challenge data in session or cache for later verification
        # In a production system, you'd want to store this securely
        # For simplicity, we'll store it in the session object's cache
        from django.core.cache import cache
        cache_key = f"challenge_{session_id}"
        cache.set(cache_key, challenge_with_answers, timeout=3600)  # 1 hour timeout

        return Response({
            'challenge': client_challenge
        }, status=status.HTTP_200_OK)


class SubmitChallengeView(APIView):
    """
    Submit a challenge response and calculate trust score.
    """
    def post(self, request):
        serializer = ChallengeResponseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        session_id = data['session_id']
        challenge_type = data['challenge_type']
        response_data = data['response_data']
        behavior_data = data['behavior_data']

        # Get time_taken_ms from the request data or use a default value
        time_taken_ms = data.get('time_taken_ms')
        if time_taken_ms is None and 'total_tracking_time_ms' in behavior_data:
            time_taken_ms = behavior_data['total_tracking_time_ms']
        if time_taken_ms is None:
            time_taken_ms = 5000  # Default to 5 seconds

        # Add time_taken_ms to response_data for scoring
        response_data['time_taken_ms'] = time_taken_ms

        # Get session
        try:
            session = UserSession.objects.get(id=session_id)
        except UserSession.DoesNotExist:
            return Response({
                'error': 'Session not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Retrieve original challenge data with answers
        from django.core.cache import cache
        cache_key = f"challenge_{session_id}"
        challenge_data = cache.get(cache_key)

        if not challenge_data:
            return Response({
                'error': 'Challenge expired or not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verify challenge type matches
        if challenge_data['type'] != challenge_type:
            return Response({
                'error': 'Challenge type mismatch'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate trust score
        scoring_engine = ScoringEngine()
        trust_score = scoring_engine.calculate_trust_score(
            challenge_data, response_data, behavior_data
        )

        # Determine if challenge passed
        passed = scoring_engine.is_challenge_passed(trust_score)

        # Log the challenge attempt
        challenge_log = ChallengeLog.objects.create(
            session=session,
            challenge_type=challenge_type,
            challenge_data=challenge_data,
            response_data=response_data,
            passed=passed,
            time_taken_ms=time_taken_ms
        )

        # Update session trust score
        # If multiple challenges, we could average or use the most recent
        session.trust_score = trust_score
        session.save()

        # Clear the challenge from cache
        cache.delete(cache_key)

        return Response({
            'trust_score': trust_score,
            'passed': passed
        }, status=status.HTTP_200_OK)


class TrustScoreView(APIView):
    """
    Get the trust score for a session.
    """
    def get(self, request, session_id):
        session = get_object_or_404(UserSession, id=session_id)

        # If no trust score yet, return a default
        if session.trust_score is None:
            return Response({
                'session_id': session_id,
                'trust_score': 0.5,  # Default neutral score
                'passed': False
            }, status=status.HTTP_200_OK)

        # Determine if the score passes the threshold
        scoring_engine = ScoringEngine()
        passed = scoring_engine.is_challenge_passed(session.trust_score)

        return Response({
            'session_id': session_id,
            'trust_score': session.trust_score,
            'passed': passed
        }, status=status.HTTP_200_OK)