from django.test import TestCase
from rest_framework.test import APIClient
from .models import Team, Match, Player, PlayerMatchStat, TeamStanding
from datetime import datetime


class RealDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Teams
        self.ulster = Team.objects.create(name="Ulster", country="Ireland")
        self.glasgow = Team.objects.create(name="Glasgow Warriors", country="Scotland")
        self.benetton = Team.objects.create(name="benetton", country="Italy")
        self.leinster = Team.objects.create(name="Leinster", country="Ireland")

        # Match
        self.match = Match.objects.create(
            date=datetime.strptime("2024-09-20", "%Y-%m-%d").date(),
            home_team=self.ulster,
            away_team=self.glasgow,
            home_score=20,
            away_score=19,
            tv_coverage="BBC Northern Ireland",
            referee="Andrew Brace"
        )

        # Player
        self.player = Player.objects.create(
            url="https://www.unitedrugby.com/clubs/benetton/destiny-aminu",
            club="benetton",
            first_name="DESTINY",
            last_name="AMINU",
            position="PROP",
            age=21,
            height="6'1''",
            weight="122KG"
        )

        # Player stats
        PlayerMatchStat.objects.create(
            player=self.player,
            points_scored=51,
            tries_scored=3,
            tackles_made=7,
            tackle_success_percentage=76.8,
            scrums_won_percentage=66.6,
        )

        # Team standings
        TeamStanding.objects.create(
            team=self.leinster,
            played=12,
            wins=12,
            draws=0,
            losses=0,
            points_difference=194,
            bonus_points=9,
            points=57
        )

    def test_upcoming_fixtures_view(self):
        response = self.client.get("/api/fixtures/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(match['home_team'] == "Ulster" for match in response.data),
            msg=f"Expected 'Ulster' in home_team. Got: {response.data}"
        )

    def test_all_fixtures_view(self):
        response = self.client.get("/api/fixtures/all/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_fixture_detail_view(self):
        response = self.client.get(f"/api/fixtures/{self.match.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['referee'], "Andrew Brace")

    def test_standings_view(self):
        response = self.client.get("/api/standings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['team_name'], "Leinster")

    def test_player_search_view(self):
        response = self.client.get("/api/players/?q=destiny")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], "DESTINY")

    def test_player_detail_view(self):
        response = self.client.get(f"/api/players/{self.player.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['club'], "benetton")
