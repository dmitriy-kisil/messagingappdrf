from django.contrib.auth.models import User
from .models import Message
from rest_framework import viewsets
from .serializers import UserSerializer, MessageSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from utils import prepare_queryset_to_json


class MessageList(generics.ListCreateAPIView):
    """
    API endpoint show all messages. If detect authenticated user - show all related to him messages,
    where he is sender or receiver of the message
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request):
        """If request user is here, return only those messages, which are related to him"""
        if request.user.is_authenticated:
            # Return only those messages, which have user as sender or receiver
            queryset = Message.objects.filter(Q(receiver__username=request.user) | Q(sender__username=request.user))
        else:
            queryset = Message.objects.all()
        if not queryset:
            return Response({"Don't found any messages. Please, try again later"})
        response = prepare_queryset_to_json(queryset)
        return Response(response)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint allow GET UPDATE and DELETE
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def delete(self, request, pk):
        """Only allow to delete if logged user is receiver or sender of the message"""
        message = Message.objects.get(pk=pk)
        if request.user == message.receiver or request.user == message.sender:
            message.delete()
            return Response({"This message was succesfully removed"})
        else:
            return Response({"You are not allowed to delete a message because you are not the sender or receiver"})


class UserList(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        """Return custom warning if there are not any users exists"""
        queryset = Message.objects.all()
        if not queryset:
            return Response({"Don't found any users. Please, try again later"})
        response = prepare_queryset_to_json(queryset)
        return Response(response)



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
        if not queryset:
            return Response({"Don't found any messages.Please, try again later"})
        # Spend 4 hours to make serializer works, didn't succeed. Request return sender_id, receiver_id and id
        # as Response(queryset.values()). When use MessageSerializer(queryset) - getting error, that field `sender`
        # not in this queryset. Finally, I used python and manually set values and fields in response. So, if you
        # run request to this endpoint, you should see sender and receiver fields as username and without ids
        response = prepare_queryset_to_json(queryset)
        return Response(response)


class ReadMessageSet(viewsets.ViewSet):
    """
    API endpoint to read message by logged user
    """
    def retrieve(self, request, pk=None):
        """Get message by id and update this status if user is receiver of the message"""
        queryset = Message.objects.all()
        if not queryset:
            return Response({"Don't found any messages.Please, again try later"})
        message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message)
        # When currently logged user is the receiver of the message, set is_readed to True, so message is readed
        if request.user == message.receiver:
            message.is_readed = True
            message.save()
        return Response(serializer.data)
