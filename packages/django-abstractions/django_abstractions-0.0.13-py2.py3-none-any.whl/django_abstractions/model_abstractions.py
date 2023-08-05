import logging
import uuid

from crum import get_current_user
from django.contrib.postgres.indexes import BrinIndex, BTreeIndex
from django.db.models import Model, DateTimeField, CharField, SlugField, UUIDField
from django.utils import timezone
from django.utils.translation import gettext as _
from uuslug import uuslug

from django_abstractions.manager_abstractions import BaseManager, AllManager

log = logging.getLogger(__name__)


class AbstractUUIDPKModel(Model):
    class Meta:
        abstract = True

    id = UUIDField(db_column='id', primary_key=True, default=uuid.uuid4, editable=False)


class AbstractTrackTimeModel(Model):
    created_at = DateTimeField(_("Created date"), auto_now_add=True, editable=False)
    updated_at = DateTimeField(_("Updated date"), auto_now=True, editable=False)
    deleted_at = DateTimeField(_("Deleted date"), default=False, editable=False)

    objects = BaseManager()
    objects_all = AllManager()

    class Meta:
        abstract = True
        indexes = (
            BrinIndex(fields=['created_at']),
            BTreeIndex(fields=['-updated_at']),
            BrinIndex(fields=['deleted_at'])
        )

    def delete(self, using=None, keep_parents=False):
        current_user = get_current_user()
        self.deleted_at = timezone.now()
        self.deleted_by = current_user.id if current_user else None
        self.save()


class AbstractTitleModel(Model):
    title = CharField("Заголовок", max_length=150, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AbstractTitleSlugModel(AbstractTitleModel):
    slug = SlugField(
        "Слог (url страницы)", max_length=150, db_index=True, unique=True, blank=True
    )

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = uuslug(self.title, instance=self)
        super().save()

    class Meta:
        abstract = True
