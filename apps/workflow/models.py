
from django.db import models
from django.conf import settings 
class Workflow(models.Model):
    # opciones del estyado de flujo de trabajo 
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('RUNNING', 'En ejecución'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
        ('EXPORTED', 'Exportado'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Nombre del Flujo")
    query_nl = models.TextField(verbose_name="Consulta en Lenguaje Natural") 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    export_file_path = models.CharField(max_length=512, null=False, blank=True, verbose_name="Ruta del archivo exportado")
    error_message = models.TextField(null=True, blank=True, verbose_name="Mensaje de Error")
    

    class Meta:
        verbose_name = "Flujo de Trabajo"
        verbose_name_plural = "Flujos de Trabajo"
        ordering = ['-created_at']
    def __str__(self):
        return f"[{self.status}] {self.name} por {self.user.username}"

class Result(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='results')
    
    osm_id = models.BigIntegerField(null=True, blank=True, verbose_name="ID de OpenStreetMap")
    
    data = models.JSONField(help_text="Datos JSON obtenidos del POI/Elemento.")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resultado de Query"
        verbose_name_plural = "Resultados de Query"
        ordering = ['-created_at']

    def __str__(self):
        return f"Resultado ({self.osm_id}) para {self.workflow.name}"