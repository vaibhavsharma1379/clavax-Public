from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

class Class(models.Model):
    class_name = models.CharField(max_length=200)
    class_room_id=models.IntegerField()
    REQUIRED_FIELD=['class_name','class_room_id']
    def __str__(self):
        return self.class_name


class StudentManager(BaseUserManager):
    def create_user(self, phone, email, first_name, last_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        student = self.model(phone=phone, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

    def create_superuser(self, phone, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is True:
            raise ValueError('Superuser must have not is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, first_name, last_name, password, **extra_fields)

class Student(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth']
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    objects = StudentManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
       
        return self.is_superuser

    def has_module_perms(self, app_label):
        
        return self.is_superuser

    @property
    def is_authenticated(self):
       
        return True