from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model
    """
    @property
    def upper_name(self):
        return self.username.upper()
