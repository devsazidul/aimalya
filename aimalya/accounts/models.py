from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Owner', 'Owner'),
        ('Staff', 'Staff'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Owner')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # OTP expires in 5 minutes
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.email}: {self.code}"

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='business/logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='business/covers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
