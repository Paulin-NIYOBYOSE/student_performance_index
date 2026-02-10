from django.core.management.base import BaseCommand
from performance.generate_dataset import generate_dataset


class Command(BaseCommand):
    help = 'Generate enhanced dataset for training'

    def add_arguments(self, parser):
        parser.add_argument(
            '--samples',
            type=int,
            default=200,
            help='Number of samples to generate (default: 200)'
        )

    def handle(self, *args, **options):
        n_samples = options['samples']
        self.stdout.write(f'Generating {n_samples} samples...')
        
        df = generate_dataset(n_samples)
        df.to_csv("dataset.csv", index=False)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Generated {len(df)} samples'))
        self.stdout.write(self.style.SUCCESS(f'✓ Saved to dataset.csv'))
        self.stdout.write(f'\nPerformance range: {df["Performance Index"].min():.1f} - {df["Performance Index"].max():.1f}')
        self.stdout.write(f'Mean performance: {df["Performance Index"].mean():.1f}')
