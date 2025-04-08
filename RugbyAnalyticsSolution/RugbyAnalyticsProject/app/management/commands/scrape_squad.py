from django.core.management.base import BaseCommand
from RugbyAnalyticsProject.scraper.scraper import scrape_squad_sitemap

class Command(BaseCommand):
    help = 'Scrape Munster Rugby squad data'

    def handle(self, *args, **kwargs):
        scrape_squad_sitemap()
