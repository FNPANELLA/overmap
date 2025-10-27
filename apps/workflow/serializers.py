from rest_framework import serializers
from .models import Workflow, Result
# p/ create
class WorkflowSerializer(serializers.ModelSerializer):
#   serializer
    result_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='results')
    error_message = serializers.CharField(read_only=True)
    class Meta:
        model = Workflow
        fields = ['id', 'name', 'query_nl', 'status', 'created_at', 'completed_at', 'result_ids', 'export_file_path', 'error_message']
        read_only_fields = ['status', 'created_at', 'completed_at', 'export_file_path', 'error_message']
        
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