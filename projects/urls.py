# projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('update/<int:project_id>/', views.update_project, name='update_project'),
    path('list/', views.project_list, name='project_list'),
    path('talent/create/<int:project_id>/', views.create_talent, name='create_talent'),
    path('talent/list/<int:project_id>/', views.talent_list, name='talent_list'),

    # path('<int:project_id>/create_talent/', views.create_talent, name='create_talent'),
    # path('<int:project_id>/talent_list/', views.talent_list, name='talent_list'),
    path('update_talent/<int:talent_id>/', views.update_talent, name='update_talent'),
    path('delete_talent/<int:talent_id>/', views.delete_talent, name='delete_talent'),

]
