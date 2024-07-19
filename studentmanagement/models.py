from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=200)
    class_room_id=models.IntegerField()
    def __str__(self):
        return self.class_name


class StudentManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        student = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        student.set_password(password)
        student.save(using=self._db)
        return student

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class Student(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    status = models.BooleanField(default=False)
    image = models.ImageField(upload_to='student_images/',blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    objects = StudentManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
