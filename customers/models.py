import uuid
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
