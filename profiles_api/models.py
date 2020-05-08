from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from datetime import datetime,timedelta
# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(default="nothing")

    def __str__(self):
        return self.name


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, roll, organization, password = None):
        if not email:
            raise ValueError('user must have an email adress')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,roll = roll, organization = organization)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, password):
        user = self.create_user(email= email, name= name, roll=Roll.ADMIN, organization=None, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Roll(models.TextChoices):
    ADMIN = 'AD', 'admin'
    MANAGER = 'MG', 'manager'
    WORKER = 'WK', 'worker'
    ORG_WORKER = 'OW', 'org_worker'

class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    roll = models.CharField(max_length=10, choices=Roll.choices, default=Roll.WORKER)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def __str__(self):
        return self.email

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(roll__in=Roll.values),
                name="%(app_label)s_%(class)s_roll_valid",
            )
        ]


class Request(models.Model):
    from_user = models.ForeignKey(UserProfile,related_name='requester', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255,choices=Roll.choices)
    to_see = models.CharField(max_length=255,choices=Roll.choices)
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)

    def __str__(self):
        return self.from_user.name +"  "+self.job_title
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(job_title__in=Roll.values),
                name="%(app_label)s_%(class)s_job_title_valid",
            ),
            models.CheckConstraint(
                check=models.Q(to_see__in=Roll.values),
                name="%(app_label)s_%(class)s_to_see_valid",
            )
        ]



class duty(models.Model):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="owner")
    persons = models.ManyToManyField(UserProfile,related_name="persons")
    title = models.CharField(max_length=255)
    duty_description = models.TextField(default="empty")
    date_posted = models.DateTimeField(default=datetime.now())
    deadline = models.DateTimeField(default=datetime.now()+timedelta(days=7))
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)



    def __str__(self):
        return self.title
