import uuid
from django.db import models
from .user_session import UserSession


class Fingerprint(models.Model):
    """
    Stores browser fingerprinting data for a user session.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(UserSession, on_delete=models.CASCADE, related_name='fingerprint')
    browser = models.CharField(max_length=128)
    os = models.CharField(max_length=128)
    headless = models.BooleanField()
    entropy_score = models.FloatField()

    def __str__(self):
        return f"Fingerprint {self.id} - {self.browser} - {self.os}"
