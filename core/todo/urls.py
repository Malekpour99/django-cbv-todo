from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from .views import (
    TaskListView,
    TaskCreateView,
    TaskStatusView,
    TaskUpdateView,
    TaskDeleteView,
    weather_status_view,
)

app_name = "todo"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("todo:tasks")), name="home"),
    path("tasks", TaskListView.as_view(), name="tasks"),
    path("task/create/", TaskCreateView.as_view(), name="create-task"),
    path("task/<int:pk>/edit/", TaskUpdateView.as_view(), name="update-task"),
    path("task/<int:pk>/complete/", TaskStatusView.as_view(), name="complete-task"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="delete-task"),
    path("weather", weather_status_view, name="weather"),
    path("api/v1/", include("todo.api.v1.urls")),
]
