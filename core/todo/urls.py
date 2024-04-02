from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .views import TaskListView, TaskCreateView, TaskDeleteView

app_name = "todo"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("todo:tasks")), name="home"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("task/create/", TaskCreateView.as_view(), name="create-task"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete-task"),
]
