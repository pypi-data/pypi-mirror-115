from app import settings
from django.db import models


class BaseModelTracker(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelTracker(BaseModelTracker):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        help_text='owner',
        related_name="%(app_label)s_%(class)s_created_by")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        help_text='owner',
        related_name="%(app_label)s_%(class)s_updated_by")

    class Meta:
        abstract = True
