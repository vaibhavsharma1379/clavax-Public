from django.contrib import admin
from .models import Class,Student
from django.core.mail import send_mail
from student import settings  
from django.contrib.auth.models import User
# Register your models here.

class ClassAdmin(admin.ModelAdmin):
    list_display=['class_room_id','class_name']
    search_fields = ['class_name']


class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','date_of_birth','status','is_superuser']
    search_fields = ['first_name']
    list_filter = ['status']
    actions = ['activate_students', 'deactivate_students']
    def activate_students(self, request,queryset):
        queryset.update(status=True)
        for student in queryset:
            send_mail(
                'Account Activated',
                'Your account has been activated.',
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=False,
            )
            
        self.message_user(request, "Selected students have been activated.")
    def deactivate_students(self, request, queryset):
        queryset.update(status=False)
        for student in queryset:
            send_mail(
                'Account Deactivated',
                'Your account has been deactivated.',
                settings.EMAIL_HOST_USER,
                [
                    student.email
                ],
                fail_silently=False
            )
        self.message_user(request, "Selected students have been deactivated.")
    activate_students.short_description = "Activate selected students"
    deactivate_students.short_description = "Deactivate selected students"

        
admin.site.register(Class, ClassAdmin)
admin.site.register(Student,StudentAdmin)