
from apps.workflow.views import dashboard_view, logoff
from django.contrib import admin
from django.urls import path, include 
from apps.accounts.views import RegisterView
from apps.workflow.views import dashboard_view, export_workflow_view


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/accounts/', include('apps.accounts.urls')), 
    path('api/', include('apps.workflow.urls')), 

    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('', dashboard_view, name=("dashboard")),
    path('workflow/<int:pk>/export_start/', export_workflow_view, name='export_start'),
    path('logout/', logoff, name="logout")
]