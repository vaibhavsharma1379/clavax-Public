from django.shortcuts import render
from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer,LoginSerializer,StudentProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated  
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']  
        password = serializer.validated_data['password']
        if email and password:
            try:
                student=Student.objects.get(email=email)
                if student.check_password(password) and student.status == True:
                    refresh=RefreshToken.for_user(student)
                   
                    return Response({
                        'refresh':str(refresh),
                        'access':str(refresh.access_token),
                        
                    })  
                return Response({'detail': f'Invalid credentials or account is inactive,{email} ,{password},{student.check_password(password)}'}, status=400)                              
            except student.DoesNotExist:
                return Response({'detail':'User does not exist'}, status=400)
        return Response({'detail': 'email and password required'}, status=400)


class StudentProfileUpdateView(generics.UpdateAPIView):
    serializer_class = StudentProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure that students can only update their own profiles
        return self.request.user