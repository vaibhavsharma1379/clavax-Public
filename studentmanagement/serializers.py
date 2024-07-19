from rest_framework import serializers  
from .models import Student , Class
class StudentSerializer(serializers.ModelSerializer):
    class_assigned = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'email', 'password', 'date_of_birth', 'status', 'image', 'class_assigned']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("email number is required.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
# serializers.py
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("email number is required.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        return value
    
class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'phone', 'email', 'date_of_birth', 'image', 'class_assigned']
        extra_kwargs = {
            'email': {'required': False},
            'image': {'required': False},
        }