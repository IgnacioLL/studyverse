from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Assuming you have a function named reverse_text in a module named utils
from llm_automation.main import main

from askapp.models import save_or_update_ask_log
from student_dashboard_app.models import Asignatura
from filemanager.models import Folder

def home(request):
    return render(request, 'ask/home.html')

def home_asignatura(request, asignatura_id):
    return render(request, 'ask/home_asignaturas.html', {'asignatura_id': asignatura_id})

def home_folder(request, asignatura_id, folder_id):
    return render(request, 'ask/home_folders.html', {'asignatura_id': asignatura_id, 'folder_id':folder_id})




def response(request):
    usuario = request.user
    user_text = request.GET['usertext']
    response, _, _ = main(f"{usuario}", "", "Español", user_text)

    save_or_update_ask_log(request.user)


    return render(request, 'ask/response.html', {'reversedtext': response})

def response_asignatura(request, asignatura_id):
    usuario = request.user
    user_text = request.GET['usertext']
    ruta  = f"{usuario}/{asignatura_id}/"
    response, _, _ = main(ruta, "", "Español", user_text)

    asignatura = get_object_or_404(Asignatura, usuario=request.user, id=asignatura_id)

    save_or_update_ask_log(request.user, asignatura)

    return render(request, 'ask/response_asignatura.html', {'reversedtext': response, 'asignatura_id':asignatura_id})

def response_folder(request, asignatura_id, folder_id):
    usuario = request.user
    user_text = request.GET['usertext']
    ruta  = f"{usuario}/{asignatura_id}/{folder_id}"
    response, _, _ = main(ruta, "", "Español", user_text)

    
    asignatura = get_object_or_404(Asignatura, usuario=request.user, id=asignatura_id)
    folder = get_object_or_404(Folder, usuario_folder=request.user, asignatura_id=asignatura_id, id=folder_id)
    

    save_or_update_ask_log(request.user, asignatura, folder=folder)

    return render(request, 'ask/response_folder.html', {'reversedtext': response, 'asignatura_id':asignatura_id, 'folder_id':folder_id})