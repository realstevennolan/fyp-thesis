import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Player, PlayerMatchStat, Team, Match, TeamMatchStat, TeamStanding


class Command(BaseCommand):
    help = "Import all data from CSV files into the database."

    def add_arguments(self, parser):
        parser.add_argument("--players", type=str, help="Path to player stats CSV.")
        parser.add_argument("--fixtures", type=str, help="Path to fixtures CSV.")
        parser.add_argument("--match_stats", type=str, help="Path to team match stats CSV.")
        parser.add_argument("--standings", type=str, help="Path to league standings CSV.")

    def handle(self, *args, **options):
        if options["players"]:
            self.import_players(options["players"])
        if options["fixtures"]:
            self.import_fixtures(options["fixtures"])
        if options["match_stats"]:
            self.import_match_stats(options["match_stats"])
        if options["standings"]:
            self.import_standings(options["standings"])

    def import_players(self, filepath):
        self.stdout.write(f"Importing players from {filepath}")
        count = 0
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    player, _ = Player.objects.get_or_create(
                        first_name=row["First Name"].strip(),
                        last_name=row["Last Name"].strip(),
                        club=row["club"].strip(),
                        defaults={
                            "url": row["URL"].strip(),
                            "position": row["Position"].strip(),
                            "age": int(row["Age"]) if row["Age"] else None,
                            "height": row["Height"].strip(),
                            "weight": row["Weight"].strip(),
                        },
                    )

                    PlayerMatchStat.objects.create(
                        player=player,
                        points_scored=int(row["points_scored"] or 0),
                        tries_scored=int(row["tries_scored"] or 0),
                        offloads=int(row["offloads"] or 0),
                        meters_gained=int(row["meters_gained"] or 0),
                        defenders_beaten=int(row["defenders_beaten"] or 0),
                        clean_breaks=int(row["clean_breaks"] or 0),
                        tackles_made=int(row["tackles_made"] or 0),
                        tackle_success_percentage=float(row["tackle_success_percentage"] or 0),
                        total_tackles_missed=int(row["total_tackles_missed"] or 0),
                        turnovers_lost=int(row["turnovers_lost"] or 0),
                        turnovers_won=int(row["turnovers_won"] or 0),
                        penalties_scored=int(row["penalties_scored"] or 0),
                        penalties_missed=int(row["penalties_missed"] or 0),
                        conversions_scored=int(row["conversions_scored"] or 0),
                        conversions_missed=int(row["conversions_missed"] or 0),
                        drop_goals_scored=int(row["drop_goals_scored"] or 0),
                        drop_goals_missed=int(row["drop_goals_missed"] or 0),
                        kicks_from_hand=int(row["kicks_from_hand"] or 0),
                        kicks_retained=int(row["kicks_retained"] or 0),
                        tries_from_kicks=int(row["tries_from_kicks"] or 0),
                        kick_meters=int(row["kick_meters"] or 0),
                        yellow_cards=int(row["yellow_cards"] or 0),
                        red_cards=int(row["red_cards"] or 0),
                        penalties_conceded=int(row["penalties_conceded"] or 0),
                        scrum_offences=int(row["scrum_offences"] or 0),
                        lineout_offences=int(row["lineout_offences"] or 0),
                        lineouts_won=int(row["lineouts_won"] or 0),
                        lineouts_lost=int(row["lineouts_lost"] or 0),
                        lineout_success_percentage=float(row["lineout_success_percentage"] or 0),
                        lineout_steals=int(row["lineout_steals"] or 0),
                        scrums_won=int(row["scrums_won"] or 0),
                        scrums_lost=int(row["scrums_lost"] or 0),
                        scrums_won_percentage=float(row["scrums_won_percentage"] or 0),
                        scrum_penalties_won=int(row["scrum_penalties_won"] or 0),
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} players and stats."))

    def import_fixtures(self, filepath):
        self.stdout.write(f"Importing fixtures from {filepath}")
        count = 0
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    try:
                        match_date = datetime.strptime(row["Date"].strip(), "%Y-%m-%d").date()
                    except ValueError:
                        print(f"Invalid date format: {row['Date']}")
                        continue

                    home_team, _ = Team.objects.get_or_create(name=row["Home Team"].strip())
                    away_team, _ = Team.objects.get_or_create(name=row["Away Team"].strip())

                    Match.objects.create(
                        date=match_date,
                        home_team=home_team,
                        away_team=away_team,
                        home_score=int(float(row["Home Score"] or 0)),
                        away_score=int(float(row["Away Score"] or 0)),
                        tv_coverage=row["TV Coverage"].strip(),
                        referee=row["Referee"].strip(),
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} fixtures."))

    def import_match_stats(self, filepath):
        self.stdout.write(f"Importing team match stats from {filepath}")
        count = 0
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    team_name = row["club"].strip()
                    team, _ = Team.objects.get_or_create(name=team_name)

                    match = Match.objects.order_by("-date").first()
                    if not match:
                        continue

                    TeamMatchStat.objects.create(
                        match=match,
                        team=team,
                        points_scored=int(row["points_scored"] or 0),
                        tries_scored=int(row["tries_scored"] or 0),
                        tackles_made=int(row["tackles_made"] or 0),
                        total_tackles_missed=int(row["total_tackles_missed"] or 0),
                        turnovers_won=int(row["turnovers_won"] or 0),
                        turnovers_lost=int(row["turnovers_lost"] or 0),
                        lineouts_won=int(row["lineouts_won"] or 0),
                        lineouts_lost=int(row["lineouts_lost"] or 0),
                        scrums_won=int(row["scrums_won"] or 0),
                        scrums_lost=int(row["scrums_lost"] or 0),
                        penalties_conceded=int(row["penalties_conceded"] or 0),
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} team match stats."))

    def import_standings(self, filepath):
        self.stdout.write(f"Importing standings from {filepath}")
        count = 0
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    team_name = row["Team"].strip()
                    team, _ = Team.objects.get_or_create(name=team_name)

                    TeamStanding.objects.update_or_create(
                        team=team,
                        defaults={
                            "played": int(row["P"] or 0),
                            "wins": int(row["W"] or 0),
                            "draws": int(row["D"] or 0),
                            "losses": int(row["L"] or 0),
                            "points_difference": int(row["PD"] or 0),
                            "bonus_points": int(row["B"] or 0),
                            "points": int(row["Pts"] or 0),
                        },
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {count} standings."))
