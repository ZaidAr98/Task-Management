from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Task 
from . import settings

class Command(BaseCommand):
    help = 'Send notifications for tasks due soon or overdue.'

    def handle(self, *args, **options):
        now = timezone.now()
        tomorrow = now.date() + timezone.timedelta(days=1)

        # Tasks due tomorrow
        upcoming_tasks = Task.objects.filter(
            due_date=tomorrow,
            status='Pending'
        )

        # Overdue tasks
        overdue_tasks = Task.objects.filter(
            due_date__lt=now.date(),
            status='Pending'
        )

        # Send notifications for upcoming tasks
        for task in upcoming_tasks:
            subject = f"Reminder: Task '{task.title}' is due tomorrow"
            message = f"Dear {task.owner.username},\n\nYour task '{task.title}' is due on {task.due_date}.\nPlease ensure it is completed on time.\n\nBest regards,\nTask Management Team"
            recipient_list = [task.owner.email]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

           
        for task in overdue_tasks:
            subject = f"Overdue: Task '{task.title}' was due on {task.due_date}"
            message = f"Dear {task.owner.username},\n\nYour task '{task.title}' was due on {task.due_date} and is now overdue.\nPlease take immediate action.\n\nBest regards,\nTask Management Team"
            recipient_list = [task.owner.email]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

          
        self.stdout.write(self.style.SUCCESS('Notifications sent successfully.'))
