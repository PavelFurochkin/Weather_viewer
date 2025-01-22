import decimal

from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="locations",
                             on_delete=models.CASCADE, null=False, default=None)
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "latitude", "longitude"], name="unic_locations")
        ]

    def __str__(self):
        return self.name


class Meta:
    unique_together = (('latitude', 'longitude', 'user'),)
    verbose_name_plural = 'Locations'
    verbose_name = 'Location'
    ordering = ['-id']
