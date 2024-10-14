from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student_dashboard_app.models import Asignatura
from accounts.models.user import User


@login_required(login_url="signin")
def index(request):
    # Add your view logic here

    asignaturas = Asignatura.objects.values('nombre').distinct()

    for asignatura in asignaturas:
        nombre = asignatura['nombre']
        nombre = nombre.capitalize()
        asignatura['nombre'] = nombre

    usuario = request.user

    return render(request, 'index.html', {'asignaturas': asignaturas, 'usuario':usuario})


def calendar(request):
    # Logic to fetch data or perform other operations for the dashboard
    # ...
    
    return render(request, 'calendar/calendarapp/dashboard.html')

