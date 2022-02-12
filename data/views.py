from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from data.serializers import DataFieldSerializer


class CricketDataRetrieveAPI(generics.CreateAPIView):
    """Retrieve data related to cricket stats based on passed parameters"""

    serializer_class = DataFieldSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
