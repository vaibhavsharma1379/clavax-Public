from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status,serializers
from django.http import JsonResponse
from .models import Student,Class
from rest_framework.decorators import api_view,permission_classes
from .serializers import StudentSerializer,LoginSerializer,StudentProfileUpdateSerializer,ClassSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.views import TokenObtainPairView

def AddClassForm(request):
    return render(request,'class.html')


def registerStudent_page(request):          
    classes = Class.objects.all()
    return render(request, 'register.html', {'classes': classes})

def LoginForm(request):
    return render(request, 'login.html')

def StudentUpdateForm(request):
    classes = Class.objects.all()
    return render(request, 'update-profile.html',{'classes': classes})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'Registration successful'}, status=201)
    return JsonResponse({'error': serializer.errors}, status=400)

@api_view(['POST'])
def AddClass(request):
    serializer=ClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'success': "class added successfully"}, status=200)
    return JsonResponse({'error': serializer.errors}, status=400)

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@api_view(['POST'])
def StudentLoginView(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        validated_data = serializer.validated_data
       
        student = Student.objects.get(phone=validated_data['phone'])
        print(student.is_superuser)
        print("frgegtehetht")
        return Response({
            'refresh': validated_data['refresh'],
            'access': validated_data['access'],
            'is_superuser': student.is_superuser,
        }, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_superuser(request):
    user = request.user
    return Response({'is_superuser': user.is_superuser}, status=status.HTTP_200_OK)

class StudentProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            student = Student.objects.get(phone=user.phone)
        except Student.DoesNotExist:
            raise NotFound("Student profile not found.")
        return student
       