from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
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

    # Reading Task List --------------------------------------------------
    def test_get_task_response_401_status(self, api_client):
        """Reading user's list of tasks without authentication"""
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_response_200_status(self, api_client, common_user):
        """Reading user's list of tasks with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    # Reading Single Task --------------------------------------------------
    def test_get_task_detail_response_401_status(self, api_client, common_task):
        """Reading a single task details without authentication"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_detail_response_200_status(
        self, api_client, common_user, common_task
    ):
        """Reading a single task details with an authenticated user"""
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": common_task.id})
        api_client.force_login(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    # Creating Single Task --------------------------------------------------
    def test_create_task_response_401_status(self, api_client):
        """Creating a task without authentication"""
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test task"}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 401

    def test_create_task_response_201_status(self, api_client, common_user):
        """Creating a task with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        data = {"title": "test task"}
        api_client.force_login(user=common_user)
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201

    def test_create_invalid_task_response_400_status(self, api_client, common_user):
        """Creating an invalid task with an authenticated user"""
        url = reverse("todo:api-v1:task-list")
        invalid_data = {"title": None}
        api_client.force_login(user=common_user)
        response = api_client.post(url, invalid_data, format="json")
        assert response.status_code == 400
