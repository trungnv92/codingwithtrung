from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):#extends BaseUserManager
    def create_user(self, email, username, password=None):
        if not email: 
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser =True
        
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser): # extends AbstractBaseUser
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
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin
 
	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True