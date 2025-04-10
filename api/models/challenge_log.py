from django.db import models
from .user_session import UserSession


class ChallengeLog(models.Model):
    """
    Logs challenge attempts, responses, and results.
    """
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='challenge_logs')
    challenge_type = models.CharField(max_length=64)
    challenge_data = models.JSONField()
    response_data = models.JSONField()
    passed = models.BooleanField()
    time_taken_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.challenge_type} - {'Passed' if self.passed else 'Failed'} - {self.time_taken_ms}ms"
