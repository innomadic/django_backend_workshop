from django.db import models

# Create your models here.

class Todo(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200, blank=True, default='')
	description = models.TextField(blank=True, default='')
	is_completed = models.BooleanField(default=False)
	is_archived = models.BooleanField(default=False)

	class Meta:
		ordering = ['created']