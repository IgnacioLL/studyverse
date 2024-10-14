from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Folder, File
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateFolderForm
from student_dashboard_app.models import Asignatura
from accounts.models.user import User
import os, subprocess

from django.contrib import messages

from django.db import IntegrityError
import shutil
import boto3

#############################################################################################################
# Auxiliares
#############################################################################################################

def handle_uploaded_file(request, asignatura_id, folder_id=None):
    documents = request.FILES.getlist('documents[]')
    s3 = boto3.client('s3')
    
    for document in documents:
        asignatura = get_object_or_404(Asignatura, usuario=request.user, id=asignatura_id)
        folder = get_object_or_404(Folder, usuario_folder=request.user, id=folder_id) if folder_id else None
        carpeta = os.path.join(str(request.user), str(asignatura_id), str(folder_id) if folder_id else '')
        file_path = os.path.join(carpeta, document.name)
        file = File.objects.create(usuario_file=request.user, name=document.name, asignatura_file=asignatura, folder=folder)
        
        s3.upload_fileobj(
            document,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            Config=boto3.s3.transfer.TransferConfig(multipart_threshold=8 * 1024 * 1024)
        )
def delete_folders(folders_to_delete, request, asignatura_id, parent=None):
    ids = list(Folder.objects.filter(usuario_folder=request.user, asignatura=asignatura_id, parent=parent, name__in=folders_to_delete).values_list('id',flat=True))
    s3 = boto3.client('s3')
    
    for id in ids:
        carpeta = os.path.join(str(request.user), str(asignatura_id), str(id) if id else '')
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=carpeta)
    
    Folder.objects.filter(usuario_folder=request.user, asignatura=asignatura_id, parent=None, name__in=folders_to_delete).delete()

def delete_files(files_to_delete, request, asignatura_id, folder=None):
    s3 = boto3.client('s3')
    
    for file in files_to_delete:
        file_path = os.path.join(str(request.user), str(asignatura_id), str(folder) if folder else '', str(file))
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path)
    
    File.objects.filter(usuario_file=request.user, asignatura_file=asignatura_id, folder=folder, name__in=files_to_delete).delete()
            



def get_file_icon(file):
    dict_files = {
        '.zip': 'fa-file-archive',
        '.py': 'fa-python',
        '.js': 'fa-js',
        '.pdf': 'fa-file-pdf',
        '.jpg': 'fa-file-image',
        '.png': 'fa-file-image',  
        '.doc': 'fa-file-word',
        '.docx': 'fa-file-word',
    }
    file_extension = "." + str(file.name).split(".")[-1:][0]
    return dict_files.get(file_extension)

#############################################################################################################
# Create
#############################################################################################################
def create_asignatura(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Asignatura.objects.create(usuario=request.user,nombre=name)
        return redirect('filemanager')

    return render(request, 'filemanager/create_asignatura.html')

def create_folder(request, asignatura_id):
    if request.method == 'POST':
        name = request.POST.get('folder_name')


        asignatura = get_object_or_404(Asignatura,usuario = request.user, id=asignatura_id)


        Folder.objects.create(usuario_folder=request.user, asignatura=asignatura, parent=None, name=name )
        return redirect('filemanager_asignatura', asignatura_id)

    return render(request, 'filemanager/create_folder.html')


def create_nested_folder(request, asignatura_id, folder_id):
    if request.method == 'POST':
        name = request.POST.get('folder_name')


        asignatura = get_object_or_404(Asignatura,usuario = request.user, id=asignatura_id)
        folder = get_object_or_404(Folder,usuario_folder = request.user, asignatura=asignatura_id, id=folder_id)
        try:
            # your code to define asignatura, folder and name
            Folder.objects.create(usuario_folder=request.user, asignatura=asignatura, parent=folder, name=name)
        except IntegrityError:
            # when the exception occurs, inform the user
            error_message = "This folder is already created."
            # Display this message is dependant on how you are handling your requests, E.g., Using messages framework, HTTP Response, etc.
            # Here I'm using Django's messages framework
            messages.error(request, error_message)

            return render(request, 'filemanager/create_folder.html')
            
        return redirect('filemanager_folders', asignatura_id, folder_id)

    return render(request, 'filemanager/create_folder.html')

#############################################################################################################
# Vistas
#############################################################################################################

def filemanager_asignaturas(request):
    # Get the asignatura object based on the provided ID
    asignaturas = Asignatura.objects.filter(usuario=request.user)

    return render(request, 'filemanager/filemanager.html', {'asignaturas': asignaturas})



def filemanager_uploads(request, asignatura_id):

    if request.method == 'POST':
        
        if 'folders_to_delete' in request.POST:

            folders_to_delete = request.POST.getlist('folders_to_delete')
            delete_folders(folders_to_delete=folders_to_delete, request=request, asignatura_id=asignatura_id)

        if 'files_to_delete' in request.POST:
            files_to_delete = request.POST.getlist('files_to_delete')
            delete_files(files_to_delete=files_to_delete, request=request,asignatura_id=asignatura_id)
        else:
            handle_uploaded_file(request, asignatura_id)
            return HttpResponseRedirect(request.path)
    files = File.objects.filter(usuario_file=request.user, asignatura_file=asignatura_id, folder=None)
    
    for file in files:
        file.icon = get_file_icon(file)
    folders = Folder.objects.filter(usuario_folder=request.user, asignatura=asignatura_id).exclude(id=None)
    asignatura = get_object_or_404(Asignatura, usuario=request.user, id=asignatura_id)

    
    return render(request, 'filemanager/folders.html', {'asignatura':asignatura, 'files': files, 'folders': folders})


def filemanager_folders(request, asignatura_id, folder_id):
    asignatura = get_object_or_404(Asignatura, usuario=request.user, id=asignatura_id)
    parent = get_object_or_404(Folder, usuario_folder=request.user, asignatura_id=asignatura_id, id=folder_id)
    folders = Folder.objects.filter(usuario_folder=request.user, asignatura_id=asignatura_id, parent_id=folder_id)

    if request.method == 'POST':

        if 'folders_to_delete' in request.POST:
            folders_to_delete = request.POST.getlist('folders_to_delete')
            delete_folders(folders_to_delete=folders_to_delete, request=request, asignatura_id=asignatura_id, parent=folder_id)

        if 'files_to_delete' in request.POST:
            files_to_delete = request.POST.getlist('files_to_delete')
            delete_files(files_to_delete=files_to_delete, request=request, asignatura_id=asignatura_id, folder=folder_id)
        else:
            handle_uploaded_file(request, asignatura_id, folder_id)
        return HttpResponseRedirect(request.path)

    files = File.objects.filter(usuario_file=request.user, asignatura_file=asignatura_id, folder=folder_id)
    for file in files:
        file.icon = get_file_icon(file)


    return render(request, 'filemanager/nested_folders.html', {'asignatura':asignatura, 'files': files, 'folders': folders, 'parent': parent})


def ExecuteView(request, asignatura_id):
    script_path = "/home/ubuntu/one/llm/ingest.py"
    archivos = f"/home/ubuntu/one/app/student_dashboard/media/{str(request.user)}/{asignatura_id}"
    result = subprocess.run(["python3", script_path, archivos], capture_output=True, text=True)
    return HttpResponse('OK')