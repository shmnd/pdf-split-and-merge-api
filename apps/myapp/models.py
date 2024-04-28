from django.db import models
from django.utils.translation import gettext_lazy as _

import datetime
import os


# datetime.datetime.now().strftime('%y-%m')



#qr gernetator from erp_core
# from erp_core.helpers.qrcodegenarator import QrCodeGeneration
# from django.dispatch import receiver
# from django.db.models.signals import post_save


#jwt 
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    created_at    = models.DateTimeField(_('create_at'),auto_now_add=True,null=True,blank=True,editable=False)
    updated_at    = models.DateTimeField(_('updated_at'),auto_now=True,null=True,blank=True,editable=False)






#pdf ////////////////////////////////////////////////////////////////////


        

#pdf ////////////////////////////////////////////////////////////////////






def image_path(self,filename):
    date_tiem         = datetime.datetime.now()
    date_time_strf    = date_tiem.strftime('%Y%m%d_%H%M%S')
    image_path        = os.path.join('students_images',date_time_strf)
    return os.path.join(image_path,filename)

class Students(BaseModel):
    user          = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    student_id    = models.CharField(_('student_id'),blank=True,null=True,unique=True,max_length=225)
    name          = models.CharField(_('student_name'),blank=True,null=True,max_length=225)
    department    = models.CharField(_('department'),blank=True,null=True,max_length=50)

    image         = models.ImageField(_('student_image'),null=True,blank=True,upload_to=image_path)

    qr_code       = models.ImageField(_('qrcode'),null=True,blank=True,upload_to='qrcode')
    is_active     = models.BooleanField(_('is_active'),default=True)

    class Meta:
        verbose_name='student'
        verbose_name_plural='students'

    def __str__(self):
        return str(self.student_id)
    




#     def save(self,*args, **kwargs):
#         qrcode_img=qrcode.make(self.name)
#         canvas=Image.new('RGB',(290,290),'white')
#         canvas.paste(qrcode_img)
#         fname=f'qr_code-{self.name}.png'
#         buffer=BytesIO()
#         canvas.save(buffer,format='PNG')
#         self.qr_code.save(fname,File(buffer),save=False)
#         canvas.close
#         super(Students,self).save(*args, **kwargs)


# its calling from erp_core 
    
# @receiver(post_save, sender=Students)
# def generate_qr_code(sender, instance, created, **kwargs):
#     if created:  # Only generate QR code if the instance is newly created
#         qr_generator = QrCodeGeneration(name=instance.name)
#         qr_generator.generate_and_save_qr_code()