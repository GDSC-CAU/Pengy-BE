from django.core.management.base import BaseCommand
from django_seed import Seed
from fireHazards.models import UserFireHazard, FireHazard
from spaces.models import MySpace

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num = 70  # 생성 수 정의
        seeder = Seed.seeder()

        # UserFireHazard 모델 시드 생성
        seeder.add_entity(UserFireHazard, num, {
            'my_space': lambda x: MySpace.objects.order_by('?').first(),
            'fire_hazard': lambda x: FireHazard.objects.order_by('?').first(),
            'thumbnail_image': lambda x: seeder.faker.image_url(),
            'nickname': lambda x: seeder.faker.first_name(),
            'capture_time': lambda x: seeder.faker.date_time(),
        })
        seeder.execute()
        print(f"UserFireHazard 데이터 생성 {num}개 완료!")
