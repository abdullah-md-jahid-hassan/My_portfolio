from django.db import models
from django.db.models import BooleanField, Case, When, Value, IntegerField



class CustomProjectOrder(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            featured_order=Case(
                When(is_featured=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            ),
            no_end_date_order=Case(
                When(end_date=None, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('featured_order', 'no_end_date_order', '-end_date')
