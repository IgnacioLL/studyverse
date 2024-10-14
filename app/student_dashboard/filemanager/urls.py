
from django.urls import path
from .views import filemanager
urlpatterns = [
    path('asignaturas/', filemanager, name='asignatura_list'),
    path('asignaturas/create_asignatura', filemanager, name='create_asignatura'),
    # Other URL patterns
]