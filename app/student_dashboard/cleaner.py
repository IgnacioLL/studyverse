
import os
import shutil
import django
from django.conf import settings
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_dashboard.settings")  # Replace "your_project.settings" with the actual settings module
# Configure Django
django.setup()

import os 
from askapp.models import AskLog
from accounts.models.user import User
from django.utils import timezone
from datetime import timedelta

from django.db.models import Min, Value
from django.db.models.functions import Coalesce


def delete_except(path, keep):
    # Convert keep to set for faster lookup
    keep = set(keep)

    for root, dirs, files in os.walk(path, topdown=False):
        # Check files
        for name in files:
            file_path = os.path.join(root, name)
            if file_path not in keep:
                os.remove(file_path)

        # Check directories
        for name in dirs:
            dir_path = os.path.join(root, name)
            if dir_path not in keep and not any(dir_path in k for k in keep):
                shutil.rmtree(dir_path)

# Calculate the timestamp 1 hour ago
one_hour_ago = timezone.now() - timedelta(hours=1)

# Retrieve folders with last_consulta > 1 hour ago
folders_with_recent_consulta = AskLog.objects.filter(last_consulta__gt=one_hour_ago)

result = (
    AskLog
    .objects
    .filter(last_consulta__gt=one_hour_ago)
    .annotate(
        ask_folder_id_new=Coalesce('ask_folder_id', Value(0)),
        ask_asignatura_id_new=Coalesce('ask_asignatura_id', Value(0))
    )
    .values('ask_usuario_id')
    .annotate(
        min_ask_folder_id=Min('ask_folder_id_new'),
        min_ask_asignatura_id=Min('ask_asignatura_id_new')
    )
)




# Print or process the folders as needed
for log in folders_with_recent_consulta:
    print("Folder:", log.ask_usuario_id)
    usuario = User.objects.filter(id=log.ask_usuario_id).get().email

path = "temp_media/"


delete_except(path, f"{path}/{usuario}/1/1")
