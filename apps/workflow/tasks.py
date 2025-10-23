from celery import shared_task
from django.utils import timezone
from apps.workflow.models import Workflow, Result
from .nlp_processor import QueryTranslator
from .overpass_handler import QueryExec
from .export_handler import DataExporter

@shared_task(name='apps.workflow.tasks.execute_overpass')
def execute_overpass(workflow_id: int):
    try:
        workflow = Workflow.objects.get(id=workflow_id)
        # marcar como running si esta pending
        if workflow.status == 'PENDING':
            workflow.status = 'RUNNING'
            workflow.save()
        translator = QueryTranslator()

        overpass_ql_code = translator.generate_overpass_ql(workflow.query_nl)

        executor = QueryExec()

        results_data = executor.execute_query(overpass_ql_code) 
        created_results = []
        for item in results_data:

            new_result = Result.objects.create(
                workflow=workflow, 
                osm_id=item.get('osm_id'), 
                data=item
            )
            created_results.append(new_result)
        workflow.status = 'COMPLETED'
        workflow.completed_at = timezone.now()
        workflow.save()

        for result in created_results:
            run_selenium_job.delay(result.id)
        
        return f"Workflow {workflow_id} completado. Resultados: {len(results_data)}"
    except Workflow.DoesNotExist:
        return "Error: Workflow no encontrado."
    except Exception as e:
        Workflow.objects.filter(id=workflow_id).update(status='FAILED')
        raise e
@shared_task(name='apps.workflow.tasks.run_selenium_job')
def run_selenium_job(result_id: int):
    #tarea celery de procesado a un resultado especifico mediante selenium
    try: 
        from .selenium_handler import SeleniumProcessor
        result = Result.objects.get(id=result_id)

        processor = SeleniumProcessor()
        url_to_process = result.data.get('website') or result.data.get('url') 
        # run_validation obtiene la información adicional
        updated_data = processor.run_validation(url_to_process, result.data) 
        # 2. registro en la base de datos
        result.data = updated_data
        result.save()

        return f"Resultado {result_id} procesado mediante selenium. Estado: {updated_data.get('selenium_status', 'OK')}"
    except Result.DoesNotExist:
        return "error: result does not exist."
    except Exception as e:
        # En caso de error, registrarlo en el resultado
        Result.objects.filter(id=result_id).update(data={'selenium_status': f'FATAL_ERROR: {str(e)}'})
        raise e

@shared_task(name='apps.workflow.tasks.export_data')
def export_data(workflow_id: int):
    try:
        # Busca el workflow primero
        workflow = Workflow.objects.get(id=workflow_id)
        exporter = DataExporter()
        file_path = exporter.export_to_csv(workflow_id)
        
        workflow.status = 'EXPORTED'
        workflow.completed_at = timezone.now()
        workflow.export_file_path = file_path  
        workflow.save()
        
        return f"Datos exportados a: {file_path}"
    except Workflow.DoesNotExist:
        return "Error: Workflow no encontrado."
    except Exception as e:
        raise e
    