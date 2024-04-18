from rest_framework import viewsets
from .serializers import TaskSerializer
from .permissions import IsAuthenticatedOwner
from .paginations import CustomDefaultPagination
from todo.models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TaskModelViewSet(viewsets.ModelViewSet):
    """
    Retrieving task and creating a task \n
    Retrieving, Updating and Deleting a single task
    """

    permission_classes = [IsAuthenticatedOwner]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomDefaultPagination
    filterset_fields = ["is_completed", "created_date"]
    search_fields = ["title"]
    ordering_fields = ["created_date", "is_completed"]
    
    def get_queryset(self):
        return Task.objects.filter(owner__user__id=self.request.user.id)
