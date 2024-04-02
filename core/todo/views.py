from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from .models import Task


# Create your views here.
class TaskListView(LoginRequiredMixin, ListView):
    """
    Showing a list of tasks based on the current user's list of tasks
    """

    template_name = "todo/task-list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.filter(owner=self.request.user)
        return tasks


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Creating a new task and dedicating this task to the current user
    """

    template_name = "todo/task-list.html"
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:tasks")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deleting specified task
    """

    model = Task
    template_name = "todo/task-list.html"
    success_url = reverse_lazy("todo:tasks")
