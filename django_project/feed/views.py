from django.core.serializers import serialize
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Thread.objects.filter(participants__in=[self.request.user]).distinct()

    def create(self, request, *args, **kwargs):
        serializer = ThreadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        participants = serializer.validated_data.get("participants")
        existing_threads = Thread.objects.filter(participants__in=participants).distinct()
        for thread in existing_threads:
            if set(thread.participants.all()) == set(participants):
                return Response(ThreadSerializer(thread).data, status=status.HTTP_200_OK)

        thread = serializer.save()

        return Response(ThreadSerializer(thread).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        thread = self.get_object()
        if request.user in thread.participants.all():
            thread.delete()
            return Response(
                {"message": "Thread deleted."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response({"error": "You don't have permission to delete this thread."}, status=status.HTTP_403_FORBIDDEN)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        messages = Message.objects.filter(thread__participants=self.request.user)

        thread = self.request.query_params.get("thread", None)
        if thread:
            messages = messages.filter(thread=thread)

        return messages

    def perform_create(self, serializer):
        thread = serializer.validated_data.get("thread")

        if self.request.user not in thread.participants.all():
            return Response({"error": "You are not a participant of this thread."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def mark_as_read(self, request, pk=None):
        try:
            message = self.get_object()

            if request.user in message.thread.participants.all():
                message.is_read = True
                message.save()
                return Response({"status": "Message marked as read."}, status=status.HTTP_200_OK)

            return Response({"error": "You are not a participant in this thread."}, status=status.HTTP_403_FORBIDDEN)

        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["GET"])
    def unread_messages(self, request):
        unread_count = Message.objects.filter(thread__participants=request.user, is_read=False).count()
        return Response({"unread_messages": unread_count}, status=status.HTTP_200_OK)
