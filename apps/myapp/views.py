from django.shortcuts import render
from .serializers import StudentSerializer,RegisterSerializer,LoginSerializer,LogoutSerializer,PdfUploadSerializer
from .models import Students

from erp_core.helpers.response import ResponseInfo


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


import os
from PyPDF2 import PdfReader,PdfWriter
from PyPDF2 import PdfFileWriter,PdfFileReader
# Create your views here.


class PdfMerge(APIView):

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')
        page_range = request.data.get('pages')

        if not uploaded_file or not page_range:
            return Response({'error': 'You entered data is incorrect. Please choose a PDF file and page range'}, status=status.HTTP_400_BAD_REQUEST)

        # Call split_pdf method passing the uploaded_file and page_range
        result = self.split_pdf(uploaded_file, page_range)
        if isinstance(result, Response):
            return result

        # If split_pdf returns split_files, call merge_pdfs
        if result:
            merged_file = self.merge_pdfs(result)
            return Response({'merged_file': merged_file}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to split the PDF file'}, status=status.HTTP_400_BAD_REQUEST)

    def split_pdf(self, uploaded_file, page_range):
        if page_range is not None:
            page_lists = list(map(int, page_range.split(',')))
        else:
            return Response({'error': 'Page range is not given'}, status=status.HTTP_400_BAD_REQUEST)

        input_pdf = PdfReader(uploaded_file)

        split_files = []
        for page_num in page_lists:
            if 1 <= page_num <= len(input_pdf.pages):
                output_pdf = PdfWriter()
                output_pdf.add_page(input_pdf.pages[page_num - 1])
                output_file_path = os.path.join('media', 'split_pdfs', f'split_page_{page_num}.pdf')
                with open(output_file_path, 'wb') as output_pdf_file:
                    output_pdf.write(output_pdf_file)
                split_files.append(output_file_path)

        return split_files

    def merge_pdfs(self, split_files):
        output_pdf = PdfWriter()

        for uploaded_file in split_files:
            input_pdf = PdfReader(uploaded_file)
            for page in range(len(input_pdf.pages)):
                output_pdf.add_page(input_pdf.pages[page])

        output_file_path = os.path.join('media', 'merged_pdfs', 'merged_file.pdf')
        with open(output_file_path, 'wb') as output_pdf_file:
            output_pdf.write(output_pdf_file)

        return output_file_path





class StudentList(APIView):
    def __init__(self, **kwargs):
        self.response_format=ResponseInfo().response
        super(StudentList,self).__init__(**kwargs)

    serializer_class=StudentSerializer
    permission_classes=(IsAuthenticated,)

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
        

class LogoutApi(APIView):

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutApi, self).__init__(**kwargs)

    serilazer_class=LogoutSerializer
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        try:

            # refresh_token=request.data.get('token')
            refresh_token=request.data.get('refresh_token')
            # refresh_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzOTQzMTc4LCJpYXQiOjE3MTM5NDI4NzgsImp0aSI6ImRkMjNlZjA5N2ExODRiYTE5OWI1NzE0ZmRhMzUxMDcxIiwidXNlcl9pZCI6MTF9._NYwia1CF6gbfZbGc1j_rgP8OGWAntt6sQfCHeNpPms'
            print(refresh_token,'aaaaaaaaaaa')
            RefreshToken(refresh_token).blacklist()

            # print(refresh_token_obj,'bbbbbbbbbbbbbbbbbbbb')
            # refresh_token_obj.blacklist()
            # print(refresh_token_obj,'ccccccccccc')

            return Response({'details':'Logout sucessfuly'},status=status.HTTP_200_OK)
        except Exception as e:
             return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        










