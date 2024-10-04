from rest_framework import serializers
from django.utils import timezone
from .models import Task, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = User
        
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    category =  CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )



    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'owner', 'completed_at','category','category_id','recurrence']
        read_only_fields = ['owner'] 

    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate(self, data):
        if self.instance and self.instance.status == 'Completed':
            if 'status' in data and data['status'] != 'Pending':
                raise serializers.ValidationError("Cannot edit a completed task unless reverted to incomplete.")
        return data
    def validate_category(self,data):
        category = data.get('category')
        user = self.context['request'].user
        if category and category.user != user:
            raise serializers.ValidationError("You do not own this category.")
        return data


