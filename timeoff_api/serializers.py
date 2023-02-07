from rest_framework import serializers
from timeoff_api.models import PolicyModel, LeaveModel


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyModel
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveModel
        fields = '__all__'

        