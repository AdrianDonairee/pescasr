from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValueError("Email inválido")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    # AbstractUser ya tiene: username, first_name, last_name, email, password, etc.
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    objects = UserManager()  # Asigná el manager personalizado

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    # Podés agregar más campos específicos de cliente acá si querés

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
