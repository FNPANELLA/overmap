
from apps.workflow.views import dashboard_view
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/accounts/', include('apps.accounts.urls')), 
    path('api/', include('apps.workflow.urls')), 

    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name=("dashboard")),
]