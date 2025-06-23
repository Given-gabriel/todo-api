from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from .models import Task
import pytz

scheduler = BackgroundScheduler()
scheduler.start()

def send_task_reminder(task_id):
    try:
        task = Task.objects.get(id=task_id)
        if not task.completed:
            print(f"⏰ [Reminder] Task '{task.name}' starts at {task.start_time}")
            # Future: call a Firebase/Socket API from here
    except Task.DoesNotExist:
        print(f"Task {task_id} not found for reminder.")

def schedule_task_reminder(task):
    if task.reminder_time and task.reminder_time > now():
        job_id = f"task_{task.id}_reminder"
        scheduler.add_job(
            send_task_reminder,
            trigger='date',
            run_date=task.reminder_time,
            args=[task.id],
            id=job_id,
            replace_existing=True
        )