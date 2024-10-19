

# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from tasks.models import Task, Notification


# class Command(BaseCommand):
#     help = 'Automatically send notifications for tasks due in less than 24 hours.'

#     def handle(self, *args, **options):
#         now = timezone.now().date()
#         time_threshold = now + timedelta(days=1)

       
#         tasks = Task.objects.filter(
#             due_date=time_threshold,
#             status='Pending' 
#         )

#         if not tasks.exists():
#             self.stdout.write("No tasks are due in the next 24 hours.")
#             return

#         notifications_sent = 0

#         for task in tasks:
#             user = task.owner


#             # Prepare the message
#             message = (
#                 f"Dear {user.username},\n\n"
#                 f"This is an urgent notification for your task '{task.title}'.\n\n"
#                 f"There is less than one day to finish your task. Please hurry up!\n\n"
#                 f"Best regards,\nTask Management Team"
#             )

#             subject = f"Notification: Task '{task.title}'"
#             recipient_list = [user.email]

#             try:
#                 # Send the email
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     recipient_list,
#                     fail_silently=False,
#                 )

               
#                 Notification.objects.create(
#                     user=user,
#                     task=task,
#                     message=message
#                 )

#                 notifications_sent += 1
#                 self.stdout.write(f"Notification sent to {user.username} for task '{task.title}'.")
#             except Exception as e:
#                 self.stderr.write(f"Failed to send notification to {user.username}: {e}")

#         self.stdout.write(f"Total notifications sent: {notifications_sent}")



from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Task, Notification

class Command(BaseCommand):
    help = 'Automatically send notifications for tasks due in less than 24 hours.'

    def handle(self, *args, **options):
        now = timezone.now()
        time_threshold = (now + timedelta(days=1)).date()

        tasks = Task.objects.filter(
            due_date = time_threshold,
            status='Pending'
        )

        if not tasks.exists():
            self.stdout.write("No tasks are due in the next 24 hours.")
            return

        notifications_sent = 0

        for task in tasks:
            user = task.owner

            # Prepare the message
            message = (
                f"Dear {user.username},\n\n"
                f"This is an urgent notification for your task '{task.title}'.\n\n"
                f"There is less than one day to finish your task. Please hurry up!\n\n"
                f"Best regards,\nTask Management Team"
            )

            subject = f"Notification: Task '{task.title}'"
            recipient_list = [user.email]

            try:
                # Send the email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    fail_silently=False,
                )

                Notification.objects.create(
                    user=user,
                    task=task,
                    message=message
                )

                notifications_sent += 1
                self.stdout.write(f"Notification sent to {user.username} for task '{task.title}'.")
            except Exception as e:
                self.stderr.write(f"Failed to send notification to {user.username}: {e}")

        self.stdout.write(f"Total notifications sent: {notifications_sent}")
