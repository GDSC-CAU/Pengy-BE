from django.core.management.base import BaseCommand
from django_seed import Seed
from spaces.models import MySpace, SpaceCategory
from users.models import MyUser

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num = 50 # 생성 수 정의
        seeder = Seed.seeder()
        seeder.add_entity(MySpace, num, {
            'FirebaseUID': lambda x: MyUser.objects.order_by('?').first(),
            'category': lambda x: SpaceCategory.objects.order_by('?').first(),
            'spaceName': lambda x: seeder.faker.street_name(),
            'coordinates': lambda x: f"{seeder.faker.latitude()}, {seeder.faker.longitude()}",
        })
        seeder.execute()
        print(f"MySpace 데이터 생성 {num}개 완료!")
