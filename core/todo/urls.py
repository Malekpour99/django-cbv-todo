from django.urls import path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

app_name = "todo"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("todo:tasks")), name="home"),
    path("tasks", TemplateView.as_view(template_name="todo/task-list.html"), name="tasks"),
]
