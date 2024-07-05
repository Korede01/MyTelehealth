from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

## -------------- HOME VIEW ------------- ##

class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Welcome to the Healthco API'}, status=status.HTTP_200_OK)