from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Add validation for the username field
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[A-Za-z0-9]+$')],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )


class Connection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    config_file = models.FileField(upload_to='configs/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.active}'
