from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, username, email, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field is required"))
        if not username:
            raise ValueError(_("The Username field is required"))

        email = self.normalize_email(email)  
        user = self.model(username=username, email=email, fullname=fullname, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)  
        return user

    def create_superuser(self, username, email, fullname, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, email, fullname, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=20, unique=True)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email', 'fullname']  

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['fullname', 'username']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the fullname of the user.
        """
        return self.fullname

    def get_short_name(self):
        """
        Returns a shorter name of the user (username in this case).
        """
        return self.username

class File(models.Model):
    owner          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name      = models.FileField(upload_to='uploads/')
    file_size      = models.PositiveIntegerField(null=True, blank=True)
    file_type      = models.CharField(max_length=50, null=True, blank=True)
    uploaded_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        
    def __str__(self):
        return self.file_name.name


