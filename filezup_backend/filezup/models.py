from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Custom user manager to handle user creation."""
    def create_user(self, user_name, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field is required"))
        if not user_name:
            raise ValueError(_("The Username field is required"))

        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(user_name, email, full_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
    user_name   = models.CharField(max_length=20, unique=True)
    full_name   = models.CharField(max_length=200)
    email       = models.EmailField(unique=True)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['full_name', 'user_name']

    def __str__(self):
        return self.user_name