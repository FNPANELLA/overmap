
import pandas as pd
import os
from django.conf import settings
from .models import Workflow, Result

class DataExporter:
    def __init__(self):
        pass
    def export_to_csv(self, workflow_id: int) -> str:
        #cons db normaliza json y guarda as csv
        workflow = Workflow.objects.get(id=workflow_id)
        results = Result.objects.filter(workflow=workflow)

        if not results.exists():
            return "no data found LOL"
        data_list = [r.data for r in results]
        df = pd.json_normalize(data_list)
        export_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        filename = f'report_{workflow_id}_{workflow.name.replace(" ", "_")}.csv'
        file_path = os.path.join(export_dir, filename)
        df.to_csv(file_path, index=False)
        return file_path