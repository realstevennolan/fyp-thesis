"""
Definition of views.
"""

# app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView 
from .models import Match, TeamStanding, Player
from .serializers import MatchSerializer, TeamStandingSerializer, PlayerSerializer
from datetime import date
from django.db.models import Q


class UpcomingFixturesView(APIView):
    def get(self, request):
        fixtures = Match.objects.filter(date__gte=date.today()).order_by('date')
        return Response(MatchSerializer(fixtures, many=True).data)

class StandingsView(APIView):
    def get(self, request):
        standings = TeamStanding.objects.order_by('-points')
        return Response(TeamStandingSerializer(standings, many=True).data)

# All fixtures (no limit)
class AllFixturesView(APIView):
    def get(self, request):
        fixtures = Match.objects.all().order_by('date')  # order by date
        return Response(MatchSerializer(fixtures, many=True).data)

    
# Fixture detail by ID
class FixtureDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    lookup_field = 'id'

# player search
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

        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

# Player detail by ID
class PlayerDetailView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = 'pk'