# app/serializers.py
from rest_framework import serializers
from .models import Match, TeamStanding, Player, PlayerMatchStat, Team, TeamMatchStat

class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = '__all__'

    def get_detail_url(self, obj):
        return f"/api/fixtures/{obj.id}/"


class TeamStandingSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamStanding
        fields = ['team_name', 'played', 'wins', 'draws', 'losses', 'points_difference', 'bonus_points', 'points']


class PlayerMatchStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMatchStat
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'position', 'age', 'height', 'weight', 'club', 'stats']

    def get_stats(self, obj):
        stats = PlayerMatchStat.objects.filter(player=obj).first()
        return PlayerMatchStatSerializer(stats).data if stats else {}


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class TeamMatchStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatchStat
        fields = [
            'id',
            'team',
            'points_scored',
            'tries_scored',
            'tackles_made',
            'total_tackles_missed',
            'turnovers_lost',
            'turnovers_won',
            'lineouts_won',
            'lineouts_lost',
            'scrums_won',
            'scrums_lost',
        ]