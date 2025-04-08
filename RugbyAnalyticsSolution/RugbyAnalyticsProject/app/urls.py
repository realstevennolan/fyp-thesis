# app/urls.py
from django.urls import path
from .views import UpcomingFixturesView, AllFixturesView, FixtureDetailView, StandingsView, PlayersListView, PlayerDetailView

urlpatterns = [
    path('api/fixtures/', UpcomingFixturesView.as_view()),
    path('api/fixtures/all/', AllFixturesView.as_view()),
    path('api/fixtures/<int:id>/', FixtureDetailView.as_view()),
    path('api/standings/', StandingsView.as_view()),
    path('api/players/', PlayersListView.as_view()),
    path('api/players/<int:pk>/', PlayerDetailView.as_view()),  # For detail page
]
