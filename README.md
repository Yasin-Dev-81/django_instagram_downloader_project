# django_instagram_downloader_project

# What is this project?
<span><img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=green" /></span>
<span><img src="https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white" /></span>
<span><img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white" /></span>

Instagram downloader website using Django and postgresSQL
Live project: https://django-instagram-downloader.herokuapp.com/

# How to use?

<strong>If you want to get notified about the future changes Follow my GitHub account.</strong>

First clone the project.

```bash
git clone https://github.com/Yasin-Dev-81/django_instagram_downloader_project.git
```

Then make sure Docker is running.
* If you are on Windows click on the Docker Desktop icon and wait for about a minute.

Then in the project directory run this command:

```bash
docker-compose up --build
```

Then migrate

```bash
docker-compose exec web python manage.py migrate
```

and create super user

```bash
docker-compose exec web python manage.py createsuperuser
```

It will create two containers:
One for Django and one for PostgresSql as the database for the project.
All the required packages will be installed.

### Install a new package.
* Attention:
If you want to install a package for django project you should run this command:

```bash
docker-compose exec web pip install <package-name>
``` 

Don't forget to add the new package to requirements.txt for further use:
```bash
docker-compose exec web pip freeze > requirements.txt
```
