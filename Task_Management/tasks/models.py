# api/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    PRIORITY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
   

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title


class Category(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name