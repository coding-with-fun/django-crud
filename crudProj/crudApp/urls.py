from django.conf.urls import url
from crudApp import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^projects/$', views.project_list, name='project_list'),
    url(r'^new/$', views.project_create, name='project_new'),

    path('view/<str:slug>', views.project_view, name='project_view'),
    path('edit/<str:slug>', views.project_update, name='project_edit'),
    path('delete/<str:slug>', views.project_delete, name='project_delete'),
]
