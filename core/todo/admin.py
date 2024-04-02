from django.contrib import admin
from .models import Task

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "created_date", "is_completed"]
    list_filter = ["owner", "is_completed"]
    search_fields = ["title", "owner"]
    date_hierarchy = "created_date"
