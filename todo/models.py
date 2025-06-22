from django.db import models

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.CharField(blank=True, null=True)
    remind_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name