# config/management/commands/update_edu_content_batch.py

from django.conf import settings
from django.core.management.base import BaseCommand
from eduContents.utils import update_edu_content
from fireHazards.models import FireHazard

class Command(BaseCommand):
    help = 'Updates educational content for all fire hazards every N minutes.'

    def handle(self, *args, **kwargs):
        fire_hazards = FireHazard.objects.all()
        for hazard in fire_hazards:
            update_edu_content(hazard.id)
            self.stdout.write(self.style.SUCCESS(f'Successfully updated content for FireHazard {hazard.id}'))

        print('Successfully updated educational content for all fire hazards.')