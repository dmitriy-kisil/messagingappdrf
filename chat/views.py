from django.contrib.auth.models import User
from .models import Message
from rest_framework import viewsets
from .serializers import UserSerializer, MessageSerializer
from rest_framework import generics


class MessageList(generics.ListCreateAPIView):
    """
    API endpoint show all messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint allow GET UPDATE and DELETE
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

