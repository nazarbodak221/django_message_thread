from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Thread, Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'thread', 'user', 'text', 'created_at']


class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Thread
        fields = ['id', 'title', 'created_at', 'participants', 'messages']

    def validate_participants(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("A thread can have only two participants.")
        return value