from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from .models import Task
import pytz

scheduler = BackgroundScheduler()

def check_reminders():
    current_time = now()
    due_tasks = Task.objects.filter(
        remind_at__lte = current_time,
        completed = False
    )

    for task in due_tasks:
        print(f"Reminder: {task.title} is starting soon at {task.start_time}!")
        # to prevent repeating, you could:
        # mark task as reminded
        # or clear remind_at

        task.remind_at = None
        task.save()