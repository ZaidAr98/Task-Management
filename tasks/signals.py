# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from dateutil.relativedelta import relativedelta
# from datetime import timedelta
# from .models import Task

# @receiver(post_save, sender=Task)
# def create_recurring_task(sender, instance, created, **kwargs):
#     if instance.status == 'Completed':
#         if instance.recurrence == 'None':
#             return

      
#         if instance.recurrence == 'Daily':
#             next_due_date = instance.due_date + timedelta(days=1)
#         elif instance.recurrence == 'Weekly':
#             next_due_date = instance.due_date + timedelta(weeks=1)
#         elif instance.recurrence == 'Monthly':
#             next_due_date = instance.due_date + relativedelta(months=1)
#         else:
#             return  
        
#         Task.objects.create(
#             title=instance.title,
#             description=instance.description,
#             due_date=next_due_date,
#             priority=instance.priority,
#             status='Pending',
#             owner=instance.owner,
#             recurrence=instance.recurrence,
#             next_due_date=next_due_date
#         )
