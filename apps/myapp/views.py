from django.shortcuts import render
from .serializers import StudentSerializer,RegisterSerializer,LoginSerializer
from .models import Students

from erp_core.helpers.response import ResponseInfo

# from rest_framework.permissions import IsAuthenticated


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.






class StudentList(APIView):
    def __init__(self, **kwargs):
        self.response_format=ResponseInfo().response
        super(StudentList,self).__init__(**kwargs)

    serializer_class=StudentSerializer
    def get(self,request):
        queryset=Students.objects.all()
        serializer=StudentSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        try:
            serializer=self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']=status.HTTP_400_BAD_REQUEST
                self.response_format['status']=False
                self.response_format['errors']=serializer.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = 'sucess'
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentData(APIView):
    def __init__(self, **kwargs):
        self.response_format=ResponseInfo().response
        super(StudentData,self).__init__(**kwargs)

    def get(self,request,id):
        stu=get_object_or_404(Students,pk=id)
        serializer=StudentSerializer(stu,data=request.data)
        serializer.is_valid()
        return Response(serializer.data)
    
    def post(self,request,id):
        stu=get_object_or_404(Students,pk=id)
        serializer=StudentSerializer(stu,data=request.data)
        try:
            if not serializer.is_valid():
                self.response_format['status_code']=status.HTTP_400_BAD_REQUEST
                self.response_format['status']=False
                self.response_format['errors']=serializer.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = 'sucess'
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id):
        stu=get_object_or_404(Students,pk=id)
        stu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserRegisterApi(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class LoginApi(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response({
                    'refresh': str(refresh),
                    'access': str(token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials ,cannot acces user'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
