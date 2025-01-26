from django.contrib.auth import get_user_model
from django.db import models


class Location(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="locations",
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=10, null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "latitude", "longitude"], name="unic_locations")
        ]

    def __str__(self):
        return self.name

