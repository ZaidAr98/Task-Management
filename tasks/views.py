from rest_framework import generics, permissions,viewsets,status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, mixins
from .permissions import  AuthorOrReadOnly,IsSuperUser
from .models import Task,Category
from rest_framework.views import APIView
from .serializers import UserSerializer, TaskSerializer,CategorySerializer,SendNotificationSerializer
from django.utils import timezone
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from .models import Task, Notification
from django.contrib.auth import get_user_model

User = get_user_model()



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]




class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated,AuthorOrReadOnly]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    




class MarkTaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated,AuthorOrReadOnly]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            self.check_object_permissions(request, task)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if task.status == 'Completed':
            return Response({'detail': 'Task is already completed.'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = 'Completed'
        task.completed_at = timezone.now()
        task.save()
        return Response({'status': 'Task marked as complete.'}, status=status.HTTP_200_OK)





class MarkTaskIncompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated,AuthorOrReadOnly]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            self.check_object_permissions(request, task)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if task.status == 'Pending':
            return Response({'detail': 'Task is already pending.'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = 'Pending'
        task.completed_at = None
        task.save()
        return Response({'status': 'Task marked as incomplete.'}, status=status.HTTP_200_OK)
    



class UserTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,AuthorOrReadOnly]
    filterset_fields = ['status', 'priority', 'due_date', 'category']
    ordering_fields = ['due_date', 'priority']
    



    def get_queryset(self):
            return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)




class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom actions if needed, for example:
    @action(detail=False, methods=['get'])
    def my_custom_action(self, request):
        # Custom logic here
        return Response({"message": "Custom action response"}, status=status.HTTP_200_OK)
    



class OnDemandNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_ids = serializer.validated_data['task_ids']
        custom_message = serializer.validated_data.get('message', '')

     
        tasks = Task.objects.filter(id__in=task_ids, owner=request.user)

        if not tasks.exists():
            return Response(
                {"detail": "No tasks found for the given IDs."},
                status=status.HTTP_404_NOT_FOUND
            )

        notifications = []

        for task in tasks:
            subject = f"Notification: Task '{task.title}'"
            if custom_message:
                message = custom_message
            else:
                message = f"Dear {request.user.username},\n\nThis is a notification for your task '{task.title}'.\n\nBest regards,\nTask Management Team"

            recipient_list = [request.user.email]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

           
            notification = Notification.objects.create(
                user=request.user,
                task=task,
                message=message
            )
            notifications.append(notification)


        from .serializers import NotificationSerializer
        notification_serializer = NotificationSerializer(notifications, many=True)

        return Response(notification_serializer.data, status=status.HTTP_200_OK)
    
