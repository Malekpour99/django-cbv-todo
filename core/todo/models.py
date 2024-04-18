from django.db import models
from django.urls import reverse

# Create your models here.


class Task(models.Model):
    owner = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def get_relative_api_url(self):
        return reverse("todo:api-v1:task-detail", kwargs={"pk": self.pk})
