import uuid
from django.db import models


class UserSession(models.Model):
    """
    Represents a user session with fingerprinting and trust score data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fingerprint_id = models.CharField(max_length=128)
    ip_address = models.GenericIPAddressField()
    trust_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - Trust: {self.trust_score or 'N/A'}"
