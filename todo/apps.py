from django.apps import AppConfig
import os


class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'
    
    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import scheduler, check_reminders
            scheduler.add_job(check_reminders, 'interval', minutes=1)
            scheduler.start()