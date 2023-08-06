from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(deleted_at__isnull=True)


class AllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class OrderedManager(models.Manager):
    def get_queryset(self):
        return super(OrderedManager, self).get_queryset().filter(deleted_at__isnull=True).order_by('-id')
