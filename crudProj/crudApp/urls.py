from django.conf.urls import url
from crudApp import views

app_name = 'crudApp'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]
