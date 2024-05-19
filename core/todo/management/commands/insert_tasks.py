from django.core.management.base import BaseCommand
from faker import Faker
import random
from accounts.models import User, Profile
from todo.models import Task


class Command(BaseCommand):
    help = "Inserting dummy tasks into the database"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="fake@test")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.bio = self.fake.paragraph(nb_sentences=3)
        profile.save()

        for _ in range(5):
            Task.objects.create(
                owner=profile,
                title=self.fake.sentence(nb_words=12),
                is_completed=random.choice([True, False]),
            )
