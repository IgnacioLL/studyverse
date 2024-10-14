from django.db import models
from accounts.models.user import  User
from filemanager.models import Folder
from student_dashboard_app.models import Asignatura
from django.utils import timezone

class AskLog(models.Model):
    ask_usuario = models.ForeignKey(User, related_name='ask_usuario', on_delete=models.CASCADE)
    ask_asignatura = models.ForeignKey(Asignatura, related_name='ask_asignatura', on_delete=models.CASCADE, blank=True, null=True)
    ask_folder = models.ForeignKey(Folder, related_name='ask_folder', on_delete=models.CASCADE, blank=True, null=True)
    last_consulta = models.DateTimeField(auto_now_add=True)

def save_or_update_ask_log(user, asignatura=None, folder=None):
    now = timezone.now()
    existing_record = AskLog.objects.filter(
        ask_usuario=user,
        ask_asignatura=asignatura,
        ask_folder=folder
    ).first()

    if existing_record:
        existing_record.last_consulta = now
        existing_record.save()
    else:
        new_ask_log = AskLog(
            ask_usuario=user,
            ask_asignatura=asignatura,
            ask_folder=folder,
            last_consulta=now
        )
        new_ask_log.save()