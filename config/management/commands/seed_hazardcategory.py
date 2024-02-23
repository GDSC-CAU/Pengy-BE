from django.core.management.base import BaseCommand
from django_seed import Seed
from fireHazards.models import HazardCategory

class Command(BaseCommand):
    help = "Seeds the database with HazardCategory data"

    def handle(self, *args, **kwargs):
        num = 10 # 생성 수 정의
        seeder = Seed.seeder()
        seeder.add_entity(HazardCategory, num, {
            'name': lambda x: seeder.faker.word(),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS('Successfully seeded HazardCategory'))
        print(f"HazardCategory 데이터 생성 {num}개 완료!")
