# Generated by Django 4.1.7 on 2024-08-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentmanagement', '0002_remove_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
