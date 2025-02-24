from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
from .manager import UserManager



class ProfileIcon(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the icon
    image = models.ImageField(upload_to='profile_icons/', help_text="Upload a PNG image.")

    def __str__(self):
        return self.name
    

class User(AbstractBaseUser, PermissionsMixin):
    selected_icon   =   models.ForeignKey(ProfileIcon, on_delete=models.SET_NULL, null=True, blank=True)
    GENDER = (
        ('male','Male'),
        ('female','Female')
    )
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    id_number   = models.CharField(max_length=14)
    mobile_number = models.CharField(max_length=15, unique=True)
    email       = models.EmailField(verbose_name='email address',max_length=80,unique=True,)
    gender      = models.CharField(choices=GENDER, max_length=7, default='male')
    date_joined =   models.DateTimeField(auto_now_add=datetime.now(), null=True)

    main_balance =  models.DecimalField(decimal_places=2, max_digits=10,default=0.00)
    revenue_share = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False)

    max_clan_create = models.IntegerField(default=3)
    max_clans_joined = models.IntegerField(default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']# Email & Password are required by default.
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        ordering = ('first_name','last_name','email')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_full_name()




class Profile(models.Model):
    user        =   models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance     =   models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    interest    =   models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    working_capital = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total_interest  =   models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    revenue_share = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    updated_on  =   models.DateTimeField(auto_now=True)
    created_on  =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
    

    def get_total_netsave(self):
        return self.balance + self.interest