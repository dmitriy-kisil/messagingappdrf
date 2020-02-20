from django.contrib.auth.models import User
from .models import Message
from rest_framework import viewsets
from .serializers import UserSerializer, MessageSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404


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


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allow GET UPDATE DELETE on users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageViewSpecificUserSet(viewsets.ViewSet):
    """
    API endpoint that allow to see messages with filter by user or is_readed.
    """

    def list(self, request):
        """Override GET request"""
        specific_user = request.data.get("user")
        check_if_readed = request.data.get("is_readed")
        custom_filter = Q()
        if specific_user or check_if_readed:
            if specific_user:
                custom_filter.add(Q(receiver__username=specific_user), Q.AND)
            if check_if_readed:
                custom_filter.add(Q(is_readed=check_if_readed), Q.AND)
            queryset = Message.objects.filter(custom_filter)
        else:
            queryset = Message.objects.all()
        # Spend 4 hours to make serializer works, didn't succeed. Request return sender_id, receiver_id and id
        # as Response(queryset.values()). When use MessageSerializer(queryset) - getting error, that field `sender`
        # not in this queryset. Finally, I used python and manually set values and fields in response. So, if you
        # run request to this endpoint, you should see sender and receiver fields as username and without ids
        response = []
        for message in queryset.values():
            sender_id, receiver_id = message["sender_id"], message["receiver_id"]
            del message["id"], message["sender_id"], message["receiver_id"]
            message["sender"] = User.objects.filter(id=sender_id).values('username')[0]['username']
            message["receiver"] = User.objects.filter(id=receiver_id).values('username')[0]['username']
            response.append(message)
        return Response(response)


class ReadMessageSet(viewsets.ViewSet):
    """
    API endpoint to read message. After get any message by id, is_readed will be set to True to this message
    """
    def retrieve(self, request, pk=None):
        """After get any message which exists, set is_readed to True to this message"""
        queryset = Message.objects.all()
        message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message)
        message.is_readed = True
        message.save()
        return Response(serializer.data)
