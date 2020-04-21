from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

class MyAccountManager(BaseUserManager):#extends BaseUserManager
    def create_user(self, phone, email, username, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError("Users must have a phone number")
        if not email: 
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone
        )
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            phone = phone,
            is_staff = True,
        )
        user.is_superuser =False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            phone = phone,
            is_admin = True,
            is_staff = True,
        )
        user.is_superuser =True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser): # extends AbstractBaseUser
    phone_regex = RegexValidator(regex=r'^\d{8,10}$', message="phone number must be entered in the format: +84999999. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    email = models.EmailField(verbose_name="email", max_length=254, unique=True)
    username = models.CharField(verbose_name="username", max_length=50, unique=True)
    full_name = models.CharField(verbose_name="full name", max_length=100)
    description = models.CharField(verbose_name="description", max_length=1000)
    skills = models.CharField(verbose_name="skill", max_length=1000)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_login = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','username']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin
 
	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

#create auth_token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)