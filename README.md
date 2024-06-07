# django-cbv-todo
 A simple To Do app using Django CBV + bootstrap for templates and DRF for creating RESTful APIs

## Configurations
 - Customized user and profile
 - Creating, Editing and Deleting Tasks
 - Changing the status of task completion
 - Up and running Celery & Redis services
 - Customized caching based on Redis
 - smtp4dev development mailing service
 - CI based on GitHub actions
 - staging configuration based on Nginx and Gunicorn
 - load-testing by locust service

### Project Setup
 run below commands:
 ```
 docker compose up
 docker compose exec backend sh -c "python manage.py makemigrations"
 docker compose exec backend sh -c "python manage.py migrate"
 ```
 This will set you up for using this project.
 you can also include '-d' detach option to the first command for running the containers in detached mode.

### Creating a super-user
```
docker compose exec backend sh -c "python manage.py createsuperuser"
```
By creating super-user you can login with the super-user credentials and also access the admin-panel.

### For running tests
```
docker compose exec backend sh -c "pytest ."
```
You can test the functionality and performance of the project by using created tests and also adding your tests as well.
