import os
from django.http import FileResponse, Http404, HttpRequest
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from django.views.decorators.http import require_POST
from .models import Workflow, Result
from .serializers import WorkflowSerializer, ResultSerializer
from rest_framework import permissions
from .tasks import export_data
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workflow
from .tasks import execute_overpass


class WorkflowListCreate(generics.ListCreateAPIView):

    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]


def get_queryset(self):
    return Workflow.objects.filter(user=self.request.user)

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

class WorkflowDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, pk: int, format=None):
        try:
            workflow = Workflow.objects.get(pk=pk, user=request.user)
        except Workflow.DoesNotExist:
            return Response({"error": "Workflow no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = workflow.export_file_path
        if not file_path:
            return Response({"error": "El archivo de exportación aún no está listo."}, status=status.HTTP_404_NOT_FOUND)
        if not os.path.exists(file_path):
            return Response({"error": "Error: El archivo exportado no se encuentra en el servidor."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return Response({"error": f"No se pudo leer el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required 
def dashboard_view(request):
        #post
        if request.method == 'POST':
            name = request.POST.get('workflow_name')
            query_nl = request.POST.get('query_nl')

            workflow = Workflow.objects.create(
                user=request.user,
                name=name,
                query_nl=query_nl,
                status='PENDING')
            execute_overpass.delay(workflow.id)

            return redirect('dashboard')
        
    #get
        workflows = Workflow.objects.filter(user=request.user)
        context = {
            'workflows': workflows
            }
        return render(request, 'dashboard.html', context)

@require_POST
@login_required
def export_workflow_view(request, pk):
    try:
        workflow = Workflow.objects.get(pk=pk, user=request.user)
    except Workflow.DoesNotExist:
        return redirect('dashboard')
    if workflow.status == 'COMPLETED':
        export_data.delay(workflow.id) 
    return redirect('dashboard')
