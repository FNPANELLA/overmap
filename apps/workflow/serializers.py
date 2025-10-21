from rest_framework import serializers
from .models import Workflow, WorkflowStep, Result
# p/ create
class WorkflowSerializer(serializers.ModelSerializer):
#   serializer
    result_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='results')

    class Meta:
        model = Workflow
        fields = ['id', 'name', 'query_nl', 'status', 'created_at', 'completed_at', 'result_ids']
        read_only_fields = ['status', 'created_at', 'completed_at']
        
    def create(self, validated_data):
        from .tasks import execute_overpass
        validated_data['user'] = self.context['request'].user
        workflow = super().create(validated_data)
        # async
        execute_overpass.delay(workflow.id) 
        return workflow

class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'