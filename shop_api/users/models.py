from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True, null=True, region='KG')

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['phone_number']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email or ''

class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='confirmation_code'
    )
    code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.email}: {self.code}"