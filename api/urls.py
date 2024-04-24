from django.urls import path, include
from api.views import ManageGameAPIView, GameStateAPIView, MoveAPIView

app_name = "urls"

urlpatterns = [
    path('manage', ManageGameAPIView.as_view(), name='manage'),
    path('<int:game_id>/board', GameStateAPIView.as_view(), name='game_state'),
    path('<int:game_id>/move', MoveAPIView.as_view(), name='move')
]
