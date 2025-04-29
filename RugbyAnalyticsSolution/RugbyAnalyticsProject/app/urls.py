# app/urls.py
from django.urls import path
from .views import (
    UpcomingFixturesView,
    AllFixturesView,
    FixtureDetailView,
    StandingsView,
    PlayersListView,
    PlayerDetailView,
    ClubsListView,
    ClubDetailView,
    ClubStandingView,
    ClubStatsView,
    ClubUpcomingMatchesView
)

urlpatterns = [
    path('api/fixtures/', UpcomingFixturesView.as_view()),
    path('api/fixtures/all/', AllFixturesView.as_view()),
    path('api/fixtures/<int:id>/', FixtureDetailView.as_view()),

    path('api/standings/', StandingsView.as_view()),

    path('api/players/', PlayersListView.as_view()),
    path('api/players/<int:pk>/', PlayerDetailView.as_view()),

    path('api/clubs/', ClubsListView.as_view()),
    path('api/clubs/<str:club_name>/', ClubDetailView.as_view()),
    path('api/clubs/<str:club_name>/standing/', ClubStandingView.as_view()),
    path('api/clubs/<str:club_name>/stats/', ClubStatsView.as_view()),
    path('api/clubs/<str:club_name>/matches/', ClubUpcomingMatchesView.as_view()),
]
