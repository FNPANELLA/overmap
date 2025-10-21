
from rest_framework import generics
from .models import Workflow, Result
from .serializers import WorkflowSerializer, ResultSerializer
from rest_framework import permissions
from .tasks import export_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class WorkflowListCreate(generics.ListCreateAPIView):

    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Workflow.objects.all().order_by('-created_at')

class WorkflowDetail(generics.RetrieveAPIView):

    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Workflow.objects.all() 

class ResultDetail(generics.RetrieveAPIView):

    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Result.objects.all()

class ExportDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk, format=None):
        try:
            workflow = Workflow.objects.get(pk=pk, user=request.user)
        except Workflow.DoesNotExist:
            return Response({"error": "Workflow no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        #   exportación
        export_data.delay(workflow.id) 
        return Response({"message": "Exportación a CSV iniciada.", "workflow_id": pk}, status=status.HTTP_202_ACCEPTED)