from django.db import models
from student_dashboard_app.models import  Asignatura
from accounts.models.user import User

class Folder(models.Model):
    usuario_folder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_folder")
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="asignatura")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ['usuario_folder', 'asignatura', 'parent', 'name']
    
    def __str__(self):
        return self.name
    
    def get_parents(self):
        parents = []
        if self.parent:
            parents.append(self.parent)
            parents.extend(self.parent.get_parents())
        return parents

class File(models.Model):
    usuario_file = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_file")
    asignatura_file = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="asignatura_file")
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="folder", null=True, blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['usuario_file', 'asignatura_file', 'folder', 'name']

    def __str__(self):
        return self.name
 