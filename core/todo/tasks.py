from celery import shared_task
from .models import Task


@shared_task
def delete_completed_tasks():
    """Deleting all the completed tasks all users included"""
    completed_tasks = Task.objects.filter(is_completed=True)
    completed_tasks.delete()
