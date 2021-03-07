import random
import time

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Task, TaskStatusChoices

logger = get_task_logger(__name__)


@shared_task
def generate_random_number(task_name, seconds=100):
    number = random.randint(10 ** 6, 10 ** 7)

    logger.info(f'"{task_name}" sleeping for {seconds} seconds')
    time.sleep(seconds)

    task = Task.objects.filter(name=task_name).first()

    if task:
        task.status = TaskStatusChoices.COMPLETE
        task.result = number
        task.save()
        logger.info(f'"{task_name}" is complete')
    else:
        logger.warning(f'Task "{task_name}" not found!')
