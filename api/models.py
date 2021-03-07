from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatusChoices(models.TextChoices):
    COMPLETE = "complete", _("complete")
    IN_PROGRESS = "in_progress", _("in progress")


class Task(models.Model):
    status = models.CharField(
        choices=TaskStatusChoices.choices,
        default=TaskStatusChoices.IN_PROGRESS,
        max_length=15,
    )
    name = models.CharField(blank=False, unique=True, max_length=200)
    result = models.IntegerField(blank=True, null=True)
    proc_id = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def is_available(cls):
        return not cls.objects.filter(status=TaskStatusChoices.IN_PROGRESS).exists()
