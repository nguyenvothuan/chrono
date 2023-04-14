from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
# Create your views here.

@authentication_classes([TokenAuthentication])
class Punch(APIView):
    def post(self, request):
        try:
            user = request.user
            print(user)
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)