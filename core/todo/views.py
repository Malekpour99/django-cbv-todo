from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Task


# Create your views here.


class TaskCreateView(CreateView):
    template_name = "todo/task-list.html"
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:tasks")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
