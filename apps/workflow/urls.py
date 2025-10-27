
from django.urls import path
from .views import WorkflowListCreate, WorkflowDetail, ResultDetail, ExportDataView, WorkflowDownloadView



urlpatterns = [
    
    path('workflows/', WorkflowListCreate.as_view(), name='workflow-list-create'),
    path('workflows/<int:pk>/', WorkflowDetail.as_view(), name='workflow-detail'),
    path('workflows/<int:pk>/export/', ExportDataView.as_view(), name='workflow-export-start'),
    path('results/<int:pk>/', ResultDetail.as_view(), name='result-detail'),
    path('workflows/<int:pk>/download/', WorkflowDownloadView.as_view(), name='workflow-export-download'),

]