---
title: Web APIs with Django
name:  Nick P.
date: September 12, 2019
---

# Welcome

* Download slides at:
* innomadic.github.io/django_backend_workshop/

# Today's Agenda

* Learn how to build a simple web application backend in Django 

# First, Think

> * Ask yourself, what problem are we trying to solve?
> * We will build a todo list application
> * What basic features should a todo list application have?
> * A minimalist implementation would include a task name, a task description, a boolean for completion status

# Architecture

* We will build a three-tiered web application: a web-based front-end, a web/ReST API backend, and a database
* The Django web application framework enables us to quickly build a web application like this

# Architecture 

* Today's workshop is focused on building the backend Web API using Django
* The next step will be to consume the API from a client -- in this example, a React-based web application
* The same API could also be used as the backend for a mobile application



# Django 

* At it heart, Django is basically a series of scripts that automatically generates the code to respond to web (HTTP) requests against the classes ("models") that we define
* We will repeatedly make calls to `python manage.py <KEYWORD>`

# Database Overview

* Django has a built-in Object-Relational Mapping (ORM) tool
* This means that we define our objects, and the ORM automatically generates the code to connect to the relational database
* Django supports a variety of popular databases
* By default, it will create a SQLite server, and we will use that for this exercise

# Database Overview

* The most important thing to remember about the database is that when we change our underlying data model, we have to generate the database changes (called "migrations") and apply them to the database, e.g.:

```python
python manage.py makemigrations
python manage.py migrate
```

# Development Environment

# Prerequisites

* Python 3.x

```bash 
pip install pipenv
pipenv shell
pipenv install django
pipenv install djangorestframework
```

# Django Config

```
export DJANGO_SETTINGS_MODULE=todo_project.settings
django-admin startproject todo_project . 
cd todo_project
django-admin startapp todo_backend_app
cd ..
python manage.py migrate
```

# Authentication

* Django provides a built-in user/group system for authentication
* For now, we will simply create a superuser that we will use for browsing the API


# Create superuser 

```bash
python manage.py createsuperuser --email admin@example.com 
 --username admin
```

# App Configuration 

* edit ./todo_project/settings.py

```python 
INSTALLED_APPS = [
    ...
    'rest_framework',
    'todo_project.todo_backend_app',
]
```

# Implementation

* Now we have set up our project and we are ready to begin implementation
* There are four main parts of a Django ReST Framework Application:
    * Models
    * Serializers
    * Views 
    * URL Routing 

# Model

./todo_project/todo_backend_app

```python
from django.db import models

class Todo(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200, blank=True, default='')
	description = models.TextField(blank=True, default='')
	is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
```

# Model 

* We changed our model, therefore we must...

```bash 
python manage.py makemigrations
python manage.py migrate 
```

# Serializers

* create ./todo_backend_app/serializers.py 

```python
from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'description']

```

# Views 

* edit ./todo_backend_app/views.py 

```python
from .models import Todo
from rest_framework import viewsets
from todo_project.todo_backend_app.serializers 
    import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
```

# URLS 

* edit ./todo_project/urls.py

```python
from django.urls import include, path
from rest_framework import routers
from todo_project.todo_backend_app import views

router = routers.DefaultRouter()
router.register(r'todos', views.TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', 
        namespace='rest_framework'))
]
```

# Testing

* `python manage.py runserver`
* Open http://127.0.0.1:8000 


# What have we accomplished?

* We have a Web API using the Django and the Django Request Framework
* We can create todo items
* We can see a list of the todo items
* We need to be able to delete and edit todos

# Embedding URLs

* The web is based on links, and our API should be no different
* Let's add a URL to our todo serializer, which will be our way of identifying the resource
* Because we're changing the serializer, not the model, we don't need to run migrations again

# Add URL to serializer

```python
fields = ['url', 'title', 'description']
```

# Basic Backend Complete!

> * Let's add two more features
> * Pagination
> * Archived todos 

# Pagination

* Edit .todo_project/settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}
```

# Test Pagination

# Archiving

```python
from django.db import models

class Todo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
```

# Archiving

* Update the serializer to send the archive flag in responxes
* Change ./todo_project/serializers.py 

```python
from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.HyperlinkedModelSerializer):
		class Meta:
			model = Todo
			fields = ['title', 'description', 'is_completed', 'url', 'is_archived']
```


# Archiving Test 

> * Test the new feature!
> * Oh no, it's broken!
> * We changed our model.  What did we forget?
> * Make and run migrations!


# Archiving 

```python
python manage.py makemigrations
python manage.py migrate
```

# Archiving Test

# Wrapping up

* We built a simple web app using Django and the Django ReST Framework
* Our data is being stored locally in a SQLite database 
* We provide a web API that returns hyperlinked, JSON-formatted responses and responses to HTTP requests like GET, PUT, POST, DELETE
* Our todo list provides pagination 

# Ideas for Expansion

* Link lists to user authentication
* Add search and sort capabilities 
* Allow users to put their todo items into multiple lists
* Create a mobile application which will use the backend

# Additional Resources

* [Django Project](http://djangoproject.com)
* [Django Rest Framework](http://django-rest-framework.org)

# Thank You

* If you haven't registered, please register at [waxqabso.com/workshop](http://waxqabso.com/workshop) for updates on future workshops