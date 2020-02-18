from django.contrib.auth.models import User
from .models import Message
from rest_framework import serializers


#
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


#
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'subject', 'creation_date']
