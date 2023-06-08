"""
Databse models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users."""
    #default password is none, this allows us to test various cases with an unusable user
    #extra fields can provide any keyword arguements
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        #provide the minimum required fields. Email and pw, 
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #assign a user manager to user model
    objects = UserManager()

    USERNAME_FIELD = 'email'