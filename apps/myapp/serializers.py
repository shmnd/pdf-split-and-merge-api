from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Students,Pdf_Files



# pdf file things/////////////////////////////////////////////////////////////////////

class PdfUploadSerializer(serializers.ModelSerializer):
    pdf_file=serializers.FileField()

    class Meta:
        model=Pdf_Files
        fields=['pdf_file']


# Authentication using jwt//////////////////////////////////////////////////////////////////////////////////
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)


    class Meta:
        model=User
        fields=['username','password','email']

    def create(self, validated_data):
        pssword             = validated_data.get('password')
        instance            = User()
        instance.username   = validated_data.get('username')
        instance.email      = validated_data.get('email')
        instance.set_password(pssword)
        instance.save()
        return instance
    
class LoginSerializer(serializers.ModelSerializer):
    username    = serializers.CharField()
    password    = serializers.CharField()
    class Meta:
        model=User
        fields=['username','password']
    
    
class LogoutSerializer(serializers.ModelSerializer):
    token=serializers.CharField()


# crud///////////////////////////////////////////////////////////////////////////////////////////////////

class StudentSerializer(serializers.ModelSerializer):
    id            = serializers.IntegerField(allow_null=True,required=True)
    student_id    = serializers.IntegerField(required=True)
    name          = serializers.CharField(required=True)
    department    = serializers.CharField(required=True)
    image         = serializers.ImageField(required=True)

    class Meta:
        model=Students
        fields=['id','student_id','name','department','image']


        def validate(self, attrs):
            students_id   = attrs.get('students_id',None)
            student       = attrs.get('id',None)
            name          = attrs.get('name',None)
            

            student_query_set=Students.objects.filter(student_id=students_id)

            if not name.isalpha():
                raise serializers.ValidationError({'name':('Name only contains alphabet')})

            if student is not None:
                student_query_set=student_query_set.exclude(pk=student)

            if student_query_set.exists():
                raise serializers.ValidationError({'student_id':('student id is already exist')})

            return super().validate(attrs)
        
        def create(self, validated_data):

            instance=Students()
            instance.student_id    =validated_data.get('student_id',None)
            instance.name           =validated_data.get('name',None)
            instance.department     =validated_data.get('department',None)
            instance.image          =validated_data.get('image',None)
            instance.save()
            return instance
        

        def update(self, instance, validated_data):

            instance.student_id     =validated_data.get('student_id')
            instance.name           =validated_data.get('name')
            instance.department     =validated_data.get('department')
            instance.image          =validated_data.get('image')
            instance.save()
            return instance
        

    
