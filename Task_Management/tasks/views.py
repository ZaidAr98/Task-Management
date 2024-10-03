from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import generics, mixins
from .permissions import  AuthorOrReadOnly,IsSuperUser
from .models import Task
from rest_framework.views import APIView
from .serializers import UserSerializer
from .serializers import TaskSerializer
from django.utils import timezone

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
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']




    def get_queryset(self):
            return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


















# class TaskListCreateView(
#     generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
# ):


#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated]
 
#     queryset = Task.objects.all()

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(owner=user)
#         return super().perform_create(serializer)

#     def get(self, request: Request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request: Request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
