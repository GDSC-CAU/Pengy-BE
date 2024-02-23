from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import MyUser
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        num = 10 # 생성 수 정의
        seeder = Seed.seeder()
        seeder.add_entity(MyUser, num, {
            'FirebaseUID': lambda x: seeder.faker.unique.uuid4(),
            'username': lambda x: seeder.faker.user_name(),
            'email': lambda x: seeder.faker.email(),
            'password': lambda x: seeder.faker.password(),
            'last_login': lambda x: timezone.make_aware(seeder.faker.date_time()),
        })
        seeder.execute()
        print(f"MyUser 데이터 생성 {num}개 완료!")
