from django.urls import path

from askapp import views


app_name = "ask"


urlpatterns = [
    path('', views.home, name='ask_home'),
    path('<int:asignatura_id>/', views.home_asignatura, name='ask_asignatura'),
    path('<int:asignatura_id>/<int:folder_id>', views.home_folder, name='ask_folder'),
    path('response', views.response, name='response'),
    path('response_asignatura/<int:asignatura_id>', views.response_asignatura, name='response_asignatura'),
    path('response_asignatura/<int:asignatura_id>/<int:folder_id>', views.response_folder, name='response_folders')
]

