from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# this class creates users, both regular and superusers. All regular users' accounts
# are inactive until an administrator can approve
class MyAccountManager(BaseUserManager):

    # this is for regular users
    def create_user(self, email, username,first_name,last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        if not username:
            raise ValueError("Users must have a username!")
        if not first_name:
            raise ValueError("Users must have a first name!")
        if not last_name:
            raise ValueError("Users must have a last name!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # this is for superusers - there should only be one
    def create_superuser(self,email,username,first_name,last_name,password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

# this model is the template for all user accounts
class Account(AbstractBaseUser):
    custodian_id            = models.AutoField(primary_key=True)
    email                   = models.EmailField(verbose_name="email",max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    first_name              = models.CharField(max_length=45)
    last_name               = models.CharField(max_length=45)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name','last_name',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
