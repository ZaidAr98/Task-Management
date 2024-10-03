from django.urls import path

from . import views

urlpatterns = [
    path('users/admin/', views.UserListView.as_view(), name='user-list-admin'),
    path("tasks/<int:pk>/",views.PostRetrieveUpdateDeleteView.as_view(),name="post_detail"),
    path('tasks/<int:pk>/complete/',  views.MarkTaskCompleteView.as_view(), name='task-complete'),
    path('tasks/<int:pk>/incomplete/', views.MarkTaskIncompleteView.as_view(), name='task-incomplete'),
    path('tasks/own/', views.UserTaskListCreateView.as_view(), name='own-task-list'), 
   
]


# djaneiro