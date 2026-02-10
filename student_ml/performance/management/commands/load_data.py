from django.core.management.base import BaseCommand
from performance.load_data import run


class Command(BaseCommand):
    help = 'Load dataset into database'

    def handle(self, *args, **options):
        self.stdout.write('Loading data from dataset.csv...')
        run()
        self.stdout.write(self.style.SUCCESS('✓ Data loaded successfully!'))
