# tasks/management/commands/send_notifications.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta

from tasks.models import Task, Notification
from tasks.serializers import NotificationSerializer
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send notifications for tasks nearing their due dates.'

    def handle(self, *args, **options):
       
        time_threshold = timedelta(days=1)

       
        today = timezone.localdate()
        tomorrow = today + time_threshold

        self.stdout.write(f"Today's date: {today}")
        self.stdout.write(f"Tomorrow's date: {tomorrow}")

        
        tasks_to_notify = Task.objects.filter(
            status='Pending',
            is_notified=False
        ).filter(
            Q(due_date__gte=today, due_date__lte=tomorrow) |
            Q(next_due_date__gte=today, next_due_date__lte=tomorrow)
        ).select_related('owner')

        self.stdout.write(f"Total tasks found for notification: {tasks_to_notify.count()}")

        if not tasks_to_notify.exists():
            self.stdout.write(self.style.WARNING('No tasks found for sending notifications.'))
            return

        notifications = []

        for task in tasks_to_notify:
            user = task.owner

            
            due_date = task.due_date
            if task.next_due_date:
                due_date = task.next_due_date

           
            if isinstance(due_date, timezone.datetime):
                due_date = due_date.date()

            time_difference = due_date - today 

            if time_difference < timedelta(days=1):
                message = (
                    f"Dear {user.username},\n\n"
                    f"This is an urgent notification for your task '{task.title}'.\n"
                    f"There is less than one day to finish your task. Please hurry up!\n\n"
                    f"Best regards,\nTask Management Team"
                )
            else:
                message = (
                    f"Dear {user.username},\n\n"
                    f"This is a notification for your task '{task.title}'.\n\n"
                    f"Best regards,\nTask Management Team"
                )

            subject = f"Notification: Task '{task.title}'"
            recipient_list = [user.email]

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"Notification sent to {user.email} for task '{task.title}'."))

                
                notification = Notification.objects.create(
                    user=user,
                    task=task,
                    message=message
                )
                notifications.append(notification)

               
                task.is_notified = True
                task.save()

                
                if task.recurrence != 'None':
                    if task.recurrence == 'Daily':
                        task.next_due_date = due_date + timedelta(days=1)
                    elif task.recurrence == 'Weekly':
                        task.next_due_date = due_date + timedelta(weeks=1)
                    elif task.recurrence == 'Monthly':
                        task.next_due_date = due_date + timedelta(days=30)
                    task.is_notified = False 
                    task.save()

            except Exception as e:
                error_message = f"Failed to send email to {user.email} for task '{task.title}': {e}"
                self.stdout.write(self.style.ERROR(error_message))
                logger.error(error_message)

        if notifications:
            notification_serializer = NotificationSerializer(notifications, many=True)
            self.stdout.write(self.style.SUCCESS("All notifications have been processed."))
