from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


# Manually mapping viewset actions to specific HTTP methods
category_list = views.CategoryViewSet.as_view({
    'get': 'list',      # Map GET requests to the list action
    'post': 'create',   # Map POST requests to the create action
})

category_detail = views.CategoryViewSet.as_view({
    'get': 'retrieve',  # Map GET request to retrieve action
    'put': 'update',    # Map PUT request to update action
    'delete': 'destroy' # Map DELETE request to destroy action
})

urlpatterns = [
    path('users/admin/', views.UserListView.as_view(), name='user-list-admin'),
    path("tasks/<int:pk>/",views.PostRetrieveUpdateDeleteView.as_view(),name="post_detail"),
    path('tasks/<int:pk>/complete/',  views.MarkTaskCompleteView.as_view(), name='task-complete'),
    path('tasks/<int:pk>/incomplete/', views.MarkTaskIncompleteView.as_view(), name='task-incomplete'),
    path('tasks/own/', views.UserTaskListCreateView.as_view(), name='own-task-list'), 
     path('category/', category_list, name='category-list'),
    path('category/<int:pk>/', category_detail, name='category-detail'),
   
]


# djaneiro