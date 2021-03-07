from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet

from .models import Task
from .serializers import TaskSerializer
from .tasks import generate_random_number


class TaskViewset(
    CreateModelMixin, RetrieveModelMixin, ListModelMixin, GenericViewSet, ViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "name"

    def perform_create(self, serializer):
        if not Task.is_available():
            raise APIException(_("Another task is in progress, try again later."))

        proc = generate_random_number.apply_async(
            args=(serializer.validated_data["name"],)
        )
        serializer.save(proc_id=proc.id)
