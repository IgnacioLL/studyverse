"""
URL configuration for student_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from accounts.views import SignUpView, SignInView, signout
from filemanager.views import filemanager_asignaturas, filemanager_uploads, filemanager_folders, create_folder, ExecuteView, create_asignatura, create_nested_folder
from django.conf import settings
from django.conf.urls.static import static

from filemanager import views as filemanager_views
from chatapp import views as chat
from askapp import views as ask


urlpatterns = [
    path('', views.index, name='index'),
    path("calendar", include("calendarapp.urls")),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('ask/', include('askapp.urls')),


    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("signout/", signout, name="signout"),
    path('archive/', filemanager_asignaturas, name='filemanager'),
    path('archive/asignatura/create_folder/<int:asignatura_id>', create_folder, name='create_folder'),
    path('archive/asignatura/create_nested_folder/<int:asignatura_id>/<int:folder_id>/', create_nested_folder, name='create_nested_folder'),
    path('archive/asignatura/create_asignatura', create_asignatura, name='create_asignatura'),
    path('archive/asignatura/<int:asignatura_id>/', filemanager_uploads, name='filemanager_asignatura'),
    path('archive/asignatura/<int:asignatura_id>/<int:folder_id>/', filemanager_folders, name='filemanager_folders'),
    path('execute/<int:asignatura_id>', ExecuteView, name='execute'),
    path('chats/', chat.chat_list, name='chat_list'),
    path('chats/chat_create/', chat.chat_create, name='chat_create'),
    path('chats/<int:chat_id>/', chat.chat_detail, name='chat_detail'),


    # ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
