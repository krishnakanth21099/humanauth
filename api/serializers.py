from rest_framework import serializers
from api.models import UserSession, ChallengeLog, Fingerprint


class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprint
        fields = ['id', 'browser', 'os', 'headless', 'entropy_score']
        read_only_fields = ['id']


class UserSessionSerializer(serializers.ModelSerializer):
    fingerprint = FingerprintSerializer(required=False)

    class Meta:
        model = UserSession
        fields = ['id', 'fingerprint_id', 'ip_address', 'trust_score', 'created_at', 'fingerprint']
        read_only_fields = ['id', 'created_at', 'trust_score']

    def create(self, validated_data):
        fingerprint_data = validated_data.pop('fingerprint', None)
        session = UserSession.objects.create(**validated_data)

        if fingerprint_data:
            Fingerprint.objects.create(session=session, **fingerprint_data)

        return session


class ChallengeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeLog
        fields = ['id', 'session', 'challenge_type', 'challenge_data', 'response_data',
                  'passed', 'time_taken_ms', 'created_at']
        read_only_fields = ['id', 'created_at']


class TrustScoreSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    trust_score = serializers.FloatField(read_only=True)
    passed = serializers.BooleanField(read_only=True)


class ChallengeRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()


class ChallengeResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    challenge_type = serializers.CharField()
    response_data = serializers.JSONField()
    behavior_data = serializers.JSONField()
    time_taken_ms = serializers.IntegerField(required=False)
