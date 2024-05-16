from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from todo.models import Task
from accounts.models import Profile


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        email="user@mail.com", password="commonPassword", is_verified=True
    )
    return user


@pytest.fixture
def common_profile(common_user):
    profile = Profile.objects.create(
        user=common_user, first_name="test first_name", last_name="test last_name"
    )
    return profile


@pytest.fixture
def common_task(common_profile):
    task = Task.objects.create(owner=common_profile, title="test task")
    return task


@pytest.mark.django_db
class TestTaskAPI:
    """API tests for todo app tasks"""

    # Reading Task List --------------------------------------------------
    def test_get_task_response_401_status(self, api_client):
        """Reading user's list of tasks without authentication"""
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_task_response_200_status(self, api_client, common_user):
        """Reading user's list of tasks with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # Reading Single Task --------------------------------------------------
    def test_get_task_detail_response_401_status(self, api_client, common_task):
        """Reading a single task details without authentication"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_task_detail_response_200_status(
        self, api_client, common_user, common_task
    ):
        """Reading a single task details with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    # Creating Single Task --------------------------------------------------
    def test_create_task_response_401_status(self, api_client):
        """Creating a task without authentication"""
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test task"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_response_201_status(self, api_client, common_user):
        """Creating a task with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test task"}
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_invalid_task_response_400_status(self, api_client, common_user):
        """Creating an invalid task with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        invalid_data = {"title": None}
        api_client.force_login(user=common_user)
        response = api_client.post(url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Updating Single Task --------------------------------------------------
    def test_update_task_response_401_status(self, api_client, common_task):
        """Updating a task without authentication"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        data = {"title": "updated task"}
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Task.objects.get(pk=common_task.id).title == common_task.title

    def test_update_task_invalid_data_response_400_status(
        self, api_client, common_user, common_task
    ):
        """Updating a task with invalid data with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        invalid_data = {"title": None}
        api_client.force_login(user=common_user)
        response = api_client.put(url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Task.objects.get(pk=common_task.id).title == common_task.title

    def test_update_not_owned_task_response_404_status(self, api_client, common_task):
        """Updating a task owned by common user"""
        another_user = get_user_model().objects.create_user(
            email="another_user@mail.com", password="anotherPassword", is_verified=True
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        data = {"title": "updated task"}
        api_client.force_login(user=another_user)
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task_response_200_status(
        self, api_client, common_user, common_task
    ):
        """Updating a task with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        data = {"title": "updated task", "is_completed": True}
        api_client.force_login(user=common_user)
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert not Task.objects.get(pk=common_task.id).title == common_task.title
        assert Task.objects.get(pk=common_task.id).title == "updated task"
        assert not Task.objects.get(pk=common_task.id).is_completed == common_task.title
        assert Task.objects.get(pk=common_task.id).is_completed == True

    def test_update_task_partial_update_response_200_status(
        self, api_client, common_user, common_task
    ):
        """Partially updating a task with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        data = {"title": "updated task"}
        api_client.force_login(user=common_user)
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Task.objects.get(pk=common_task.id).title == "updated task"

    # Deleting Single Task --------------------------------------------------
    def test_delete_task_response_401_status(self, api_client, common_task):
        """Deleting a task without authentication"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Task.objects.filter(pk=common_task.id).exists()

    def test_delete_task_response_204_status(
        self, api_client, common_user, common_task
    ):
        """Deleting a task with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        api_client.force_login(user=common_user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(pk=common_task.id).exists()

    def test_delete_task_invalid_id_response_404_status(self, api_client, common_user):
        """Deleting a task with an invalid task ID"""
        invalid_task_id = 99999
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": invalid_task_id})
        api_client.force_login(user=common_user)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
