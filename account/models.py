from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, password, **extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",  # Prevents conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",  # Prevents conflicts
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Person(models.Model):
    cities = (
        ('خارج سوريا', 'خارج سوريا'),
        ('ادلب', 'ادلب'),
        ('دمشق', 'دمشق'),
        ('حلب', 'حلب'),
        ('ريف دمشق', 'ريف دمشق'),
        ('حماه', 'حماه'),
        ('حمص', 'حمص'),
        ('درعا', 'درعا'),
        ('القنيطرة', 'القنيطرة'),
        ('السويداء', 'السويداء'),
        ('دير الزور', 'دير الزور'),
        ('رقه', 'رقه'),
        ('الحسكة', 'الحسكة'),
        ('اللاذقية', 'اللاذقية'),
        ('طرطوس', 'طرطوس'),
    )
    phone = models.CharField(max_length=30, default="")
    city = models.CharField(max_length=30, null=True, choices=cities)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Now points to your CustomUser
        verbose_name='user',
        null=True,
        on_delete=models.CASCADE,
        related_name='person'
    )
    name = models.CharField(max_length=30, default="")
    note = models.TextField(default='')

    def __str__(self):
        return self.name
