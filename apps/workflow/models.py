
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
    

    class Meta:
        verbose_name = "Flujo de Trabajo"
        verbose_name_plural = "Flujos de Trabajo"
        ordering = ['-created_at']
    def __str__(self):
        return f"[{self.status}] {self.name} por {self.user.username}"
class WorkflowStep(models.Model):
    ACTION_CHOICES = (
        ('NLP_EXTRACT', 'Extracción NLP'),
        ('OVERPASS_QUERY', 'Consulta Overpass'),
        ('SELENIUM_PROCESS', 'Procesamiento Selenium'),
        ('EXPORT_CSV', 'Exportar CSV/BI'),
    )


    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='steps')
    
    step_number = models.PositiveSmallIntegerField(verbose_name="Número de Paso")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    parameters = models.JSONField(default=dict, help_text="Parámetros para la acción (e.g., el query QL generado).")

    class Meta:
        verbose_name = "Paso de Flujo"
        verbose_name_plural = "Pasos de Flujo"
        ordering = ['step_number']

    def __str__(self):
        return f"Paso {self.step_number}: {self.action} en {self.workflow.name}"


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