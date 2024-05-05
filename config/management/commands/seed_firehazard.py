from django.core.management.base import BaseCommand
from django_seed import Seed
from fireHazards.models import FireHazard

class Command(BaseCommand):
    help = "Seed database for FireHazard model"

    def handle(self, *args, **kwargs):
        num = 100  # Number of FireHazard entries to create
        seeder = Seed.seeder()

        # Seed FireHazard model
        seeder.add_entity(FireHazard, num, {
            'object': lambda x: seeder.faker.word()
        })

        inserted_pks = seeder.execute()  # This will execute and return the primary keys of the inserted objects
        print(f"Created {num} FireHazard entries.")
