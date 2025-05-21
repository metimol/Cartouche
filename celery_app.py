"""
Celery configuration and task definitions for the Cartouche Bot Service.
"""
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

from config import settings

# Create Celery app
app = Celery('cartouche_bot_service',
             broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULT_BACKEND)

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    worker_max_tasks_per_child=200,
    worker_prefetch_multiplier=1,
)

# Define periodic tasks
# Note: These will only run if Celery beat is available
app.conf.beat_schedule = {
    'grow-bots-daily': {
        'task': 'tasks.bot_tasks.grow_bots',
        'schedule': crontab(hour=0, minute=0),  # Run at midnight
        'args': (),
    },
    'generate-bot-posts': {
        'task': 'tasks.post_tasks.generate_bot_posts',
        'schedule': timedelta(hours=3),  # Run every 3 hours
        'args': (),
    },
    'process-subscriptions': {
        'task': 'tasks.subscription_tasks.process_subscriptions',
        'schedule': timedelta(hours=6),  # Run every 6 hours
        'args': (),
    },
    'cleanup-old-data': {
        'task': 'tasks.maintenance_tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Run at 2 AM
        'args': (),
    },
}

# Import tasks to ensure they're registered
import tasks.bot_tasks
import tasks.post_tasks
import tasks.reaction_tasks
import tasks.subscription_tasks
import tasks.maintenance_tasks
