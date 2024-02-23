from django.core.management.base import BaseCommand
from django_seed import Seed
from fireHazards.models import FireHazard, HazardCategory

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num = 100  # 생성 수 정의
        seeder = Seed.seeder()

        # HazardCategory 모델 시드 생성
        seeder.add_entity(HazardCategory, num, {
            'name': lambda x: seeder.faker.word()
        })

        # FireHazard 모델 시드 생성
        seeder.add_entity(FireHazard, num, {
            'hazard_category': lambda x: HazardCategory.objects.order_by('?').first(),
            'object': lambda x: seeder.faker.word(),
        })
        seeder.execute()
        print(f"FireHazard 데이터 생성 {num}개 완료!")
