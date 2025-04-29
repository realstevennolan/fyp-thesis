from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from .models import Match, TeamStanding, Player, TeamMatchStat
from .serializers import (
    MatchSerializer,
    TeamStandingSerializer,
    PlayerSerializer,
    TeamMatchStatSerializer
)
from datetime import date
from django.db.models import Q


class UpcomingFixturesView(APIView):
    def get(self, request):
        fixtures = Match.objects.filter(date__gte=date.today()).order_by('date')
        return Response(MatchSerializer(fixtures, many=True).data)


class AllFixturesView(APIView):
    def get(self, request):
        fixtures = Match.objects.all().order_by('date')
        return Response(MatchSerializer(fixtures, many=True).data)


class FixtureDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'id'


class StandingsView(APIView):
    def get(self, request):
        standings = TeamStanding.objects.order_by('-points')
        return Response(TeamStandingSerializer(standings, many=True).data)


class PlayersListView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        players = Player.objects.all()
        if query:
            players = players.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(position__icontains=query) |
                Q(club__icontains=query)
            )
        return Response(PlayerSerializer(players, many=True).data)


class PlayerDetailView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'pk'


class ClubsListView(APIView):
    def get(self, request):
        clubs = Player.objects.values_list('club', flat=True).distinct()
        cleaned_clubs = [club.replace('team-', '') for club in clubs if club]
        return Response(cleaned_clubs)


class ClubDetailView(APIView):
    def get(self, request, club_name):
        full_name = f"team-{club_name.lower()}"
        players = Player.objects.filter(club__iexact=full_name)
        return Response(PlayerSerializer(players, many=True).data)


class ClubStandingView(APIView):
    def get(self, request, club_name):
        full_name = f"team-{club_name.lower()}"
        standing = TeamStanding.objects.filter(team__name=full_name).first()
        return Response(TeamStandingSerializer(standing).data if standing else {})


class ClubStatsView(APIView):
    def get(self, request, club_name):
        full_name = f"team-{club_name.lower()}"
        stats = TeamMatchStat.objects.filter(team__name=full_name)
        return Response(TeamMatchStatSerializer(stats, many=True).data)


class ClubUpcomingMatchesView(APIView):
    def get(self, request, club_name):
        full_name = f"team-{club_name.lower()}"
        matches = Match.objects.filter(home_team__name=full_name).order_by('date')[:5]
        return Response(MatchSerializer(matches, many=True).data)
