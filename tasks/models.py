from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10,choices=[
        ('low', 'Past'),
        ('medium', 'O‘rta'),
        ('high', 'Yuqori'),
    ])
    completed = models.BooleanField(default=False)


    def __str__(self):
        return self.title