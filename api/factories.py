from factory.django import DjangoModelFactory


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = "api.Task"
        django_get_or_create = ("name",)
