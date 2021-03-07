from collections import OrderedDict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Task


class OmitNulMixin:
    def to_representation(self, instance):
        fields = super().to_representation(instance)
        return OrderedDict(i for i in fields.items() if i[1] is not None)


class TaskSerializer(OmitNulMixin, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task

    def get_field_names(self, declared_fields, info):
        request = self.context.get("request")
        fields = [
            "name",
        ]

        if request.method == "GET":
            fields += [
                "status",
                "result",
            ]

        return fields
