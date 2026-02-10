from django.core.management.base import BaseCommand
from performance.train_model import train


class Command(BaseCommand):
    help = 'Train the advanced student performance prediction model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting model training...'))
        train()
        self.stdout.write(self.style.SUCCESS('Model training completed!'))
