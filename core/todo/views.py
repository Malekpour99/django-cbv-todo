from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Task


# Create your views here.
class TaskListView(ListView):
    template_name = "todo/task-list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.filter(owner=self.request.user)
        return tasks


class TaskCreateView(CreateView):
    template_name = "todo/task-list.html"
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:tasks")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
