from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # AbstractUser ya tiene: username, first_name, last_name, email, password, etc.
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    # Podés agregar más campos específicos de cliente acá si querés

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
