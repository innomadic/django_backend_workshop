from .models import Todo
from rest_framework import viewsets
from todo_project.todo_backend_app.serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer