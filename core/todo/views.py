from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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


class TaskStatusView(LoginRequiredMixin, View):
    """
    Updating task is_completed field status
    """

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get("pk"))
        if not task.is_completed:
            task.is_completed = True
        else:
            task.is_completed = False
        task.save()
        return redirect(reverse_lazy("todo:tasks"))


class TaskUpdateView(UpdateView):
    """
    Updating a specific task
    """

    template_name = "todo/update-task.html"
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:tasks")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deleting specified task
    """

    model = Task
    template_name = "todo/task-list.html"
    success_url = reverse_lazy("todo:tasks")

    def get(self, request, *args, **kwargs):
        # returning a post request to by-pass the delete confirmation
        return self.post(request, *args, **kwargs)
