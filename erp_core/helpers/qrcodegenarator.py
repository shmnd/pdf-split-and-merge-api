
from django.db.models import  #add db name
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from erp_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from rest_framework import status


class qr_codegenertor:

    def __init__(self, **kwargs):
        self.response_format=ResponseInfo().response
        super(qr_codegenertor,self).__init__(**kwargs)
        
    def generate_qr_code(self, qr_image):
        qr_image = qrcode.make(self.name) #add a db name to generate a qrwith model name from moded
        canvas = Image.new('RGB', (290, 290), 'white')
        canvas.paste(qr_image)
        qrname = f'qrcode-{self.name}.png' #add a db name to generate a qrwith model name from moded
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        buffer.close()   # Close the BytesIO object after saving the image otherwise it take space permently
        return qrname,buffer
    

        # self.qrcode.save(qrname, File(buffer), save=False)
        # canvas.close()


    def save_qr_code(self):
        qrname, buffer = self.generate_qr_code()
        # Save QR code to file or database
        # Example: self.qrcode.save(qrname, File(buffer), save=False)
        # Return whatever information you need, or None if not needed

    def save(self, *args, **kwargs):
        self.save_qr_code()
        # Perform other save operations if needed
        # Return whatever information you need, or None if not needed

        # super(qr_codegenertor, self).save(*args, **kwargs)

        self.response_format['status_code'] = status.HTTP_200_OK
        self.response_format["status"] = True

        return Response(self.response_format, status=status.HTTP_200_OK)