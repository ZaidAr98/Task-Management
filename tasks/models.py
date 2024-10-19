# api/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import timedelta
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

    RECURRENCE_CHOICES = [
        ('None', 'None'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]
   

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='Pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    recurrence = models.CharField(max_length=7, choices=RECURRENCE_CHOICES, default='None')
    next_due_date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        current_time = timezone.now()
        if self.recurrence == "Daily" and self.due_date:
            self.next_due_date = (current_time + timedelta(days=1)).date()
        elif self.recurrence == "Weekly" and self.due_date:
            self.next_due_date = (current_time + timedelta(days=7)).date()
        elif self.recurrence == "Monthly" and self.due_date:
            self.next_due_date = (current_time + timedelta(days=30)).date()
        else:
            self.next_due_date = None
        super().save(*args, **kwargs)


class Category(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"