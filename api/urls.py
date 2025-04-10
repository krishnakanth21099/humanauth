from django.urls import path
from api.views import (
    InitSessionView, GetChallengeView, SubmitChallengeView, TrustScoreView
)

urlpatterns = [
    path('init-session/', InitSessionView.as_view(), name='init-session'),
    path('get-challenge/', GetChallengeView.as_view(), name='get-challenge'),
    path('submit-challenge/', SubmitChallengeView.as_view(), name='submit-challenge'),
    path('trust-score/<uuid:session_id>/', TrustScoreView.as_view(), name='trust-score'),
]
