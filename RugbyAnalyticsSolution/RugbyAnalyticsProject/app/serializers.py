# app/serializers.py
from rest_framework import serializers
from .models import Match, TeamStanding, Player, PlayerMatchStat

class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = '__all__'  # or list all fields manually + 'detail_url'

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