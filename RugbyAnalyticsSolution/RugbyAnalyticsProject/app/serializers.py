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
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamMatchStat
        fields = ['team_name', 'points_scored', 'tries_scored', 'offloads', 'meters_gained',
                  'defenders_beaten', 'clean_breaks', 'tackles_made', 'tackle_success',
                  'total_tackles_missed', 'turnovers_lost', 'turnovers_won', 'penalties_scored',
                  'penalties_missed', 'conversions_scored', 'conversions_missed', 'drop_goals_scored',
                  'drop_goals_missed', 'kicks_from_hand', 'kicks_retained', 'tries_from_kicks',
                  'kick_meters', 'yellow_cards', 'red_cards', 'penalties_conceded',
                  'scrum_offences', 'lineout_offences', 'lineout_won', 'lineout_steals',
                  'scrum_won', 'scrum_lost', 'scrums_won_percentage', 'lineout_success_percentage']
