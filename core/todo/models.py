from django.db import models

# Create your models here.


class Task(models.Model):
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
