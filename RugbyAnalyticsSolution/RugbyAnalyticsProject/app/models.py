from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    url = models.URLField(max_length=200, blank=True)
    club = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PlayerMatchStat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points_scored = models.IntegerField(default=0)
    tries_scored = models.IntegerField(default=0)
    offloads = models.IntegerField(default=0)
    meters_gained = models.IntegerField(default=0)
    defenders_beaten = models.IntegerField(default=0)
    clean_breaks = models.IntegerField(default=0)
    tackles_made = models.IntegerField(default=0)
    tackle_success_percentage = models.FloatField(default=0)
    total_tackles_missed = models.IntegerField(default=0)
    turnovers_lost = models.IntegerField(default=0)
    turnovers_won = models.IntegerField(default=0)
    penalties_scored = models.IntegerField(default=0)
    penalties_missed = models.IntegerField(default=0)
    conversions_scored = models.IntegerField(default=0)
    conversions_missed = models.IntegerField(default=0)
    drop_goals_scored = models.IntegerField(default=0)
    drop_goals_missed = models.IntegerField(default=0)
    kicks_from_hand = models.IntegerField(default=0)
    kicks_retained = models.IntegerField(default=0)
    tries_from_kicks = models.IntegerField(default=0)
    kick_meters = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    penalties_conceded = models.IntegerField(default=0)
    scrum_offences = models.IntegerField(default=0)
    lineout_offences = models.IntegerField(default=0)
    lineouts_won = models.IntegerField(default=0)
    lineouts_lost = models.IntegerField(default=0)
    lineout_success_percentage = models.FloatField(default=0)
    lineout_steals = models.IntegerField(default=0)
    scrums_won = models.IntegerField(default=0)
    scrums_lost = models.IntegerField(default=0)
    scrums_won_percentage = models.FloatField(default=0)
    scrum_penalties_won = models.IntegerField(default=0)

class Match(models.Model):
    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    tv_coverage = models.CharField(max_length=100, blank=True)
    referee = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"
class TeamMatchStat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Fix for migration
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points_scored = models.IntegerField(default=0)
    tries_scored = models.IntegerField(default=0)
    tackles_made = models.IntegerField(default=0)
    total_tackles_missed = models.IntegerField(default=0)
    turnovers_won = models.IntegerField(default=0)
    turnovers_lost = models.IntegerField(default=0)
    lineouts_won = models.IntegerField(default=0)
    lineouts_lost = models.IntegerField(default=0)
    scrums_won = models.IntegerField(default=0)
    scrums_lost = models.IntegerField(default=0)
    penalties_conceded = models.IntegerField(default=0)

class TeamStanding(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points_difference = models.IntegerField(default=0)
    bonus_points = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
