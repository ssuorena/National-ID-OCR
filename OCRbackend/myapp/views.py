from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from PIL import Image
import io
from .OCR import ID_OCR

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_file = io.BytesIO(image.read())
            img = Image.open(image_file)
            path='User_ID_Card/'+'input.jpg'
            img.save(path)
            info,img,s,prtrate = ID_OCR(path,width=900)
            return Response({'Info':info,'Prtrate':prtrate}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)