from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The Email must be Set!")

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superadmin',True)
        extra_fields.setdefault('is_seller',False)
        extra_fields.setdefault('is_active',True)

        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True') 
        if extra_fields.get('is_superadmin') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_superadmin') is not True:
            raise ValueError('Superuser must have is_superadmin=True')
        return self._create_user(email, password, **extra_fields)
   

class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)
    is_seller       = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    def full_name(self):
        return f'{ self.first_name} { self.last_name }'
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=50,blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    profile_picture =models.ImageField(blank=True, upload_to='userprofile',default='avatar2.png' )
    country = models.CharField(blank=True,max_length=50)
    state = models.CharField(blank=True,max_length=50)
    city = models.CharField(blank=True,max_length=50)
    
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
@receiver(post_save, sender=Account)
def create_profile(sender, instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user = instance)

@receiver(post_save, sender=Account)
def profile(sender, instance, **kwargs):
    instance.userprofile.save()