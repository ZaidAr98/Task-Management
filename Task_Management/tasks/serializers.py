from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'owner', 'completed_at']
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


