from django.core.management.base import BaseCommand
from django_seed import Seed
from spaces.models import SpaceCategory

class Command(BaseCommand):
    help = "Seeds the database with SpaceCategory data"

    def handle(self, *args, **kwargs):
        num = 5 # 생성 수 정의
        seeder = Seed.seeder()
        seeder.add_entity(SpaceCategory, num, {
            'categoryName': lambda x: seeder.faker.word(),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS('Successfully seeded SpaceCategory'))
        print(f"SpaceCategory 데이터 생성 {num}개 완료!")
