from rest_framework import serializers  
from .models import Student , Class
from rest_framework_simplejwt.tokens import RefreshToken
import re
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
        student.status = True 
        student.is_superuser = False  
        student.is_staff=True
        student.save()
        return student
    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Last name is required.")
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("email is required.")
        return value
    def validate_phone(self, value):
        if not value:
           raise serializers.ValidationError("phone is required.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        if not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone or not password:
            raise serializers.ValidationError("Phone and password are required.")
        try:
            student = Student.objects.get(phone=phone)
        except Student.DoesNotExist:
            raise serializers.ValidationError("User with this phone number does not exist or inactive")

        if not student.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not student.status:
            raise serializers.ValidationError("Account is inactive.")

        refresh = RefreshToken.for_user(student)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'phone':phone
        }
        
class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'class_assigned']
        
    

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model=Class
        fields = '__all__'