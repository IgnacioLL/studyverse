from django.db import models
from accounts.models.user import  User

class Asignatura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    # Add other fields related to the subject

    def __str__(self):
        return self.nombre


opciones_asignaciones = ['Examen','Trabajo','Parcial']

class Asignacion(models.Model):
    opciones_asignaciones = list(zip(opciones_asignaciones, opciones_asignaciones))

    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    tipo_evaluacion = models.CharField(max_length=100, choices=opciones_asignaciones)
    descripcion = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(tipo_evaluacion__in=opciones_asignaciones), name='constraint_tipo_evaluacion')
        ]
    # Add other fields related to the assignment

    def __str__(self):
        return self.titulo
