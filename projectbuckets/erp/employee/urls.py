from django.urls import path
from employee.views import index, create, detail, update, delete, sync, download
from employee.views import create, detail, update, delete

app_name = 'employee'
urlpatterns = [
    path('create/', create, name='create'),
    path('index/', index, name='index'),
    path('detail/<int:id>', detail, name='detail'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),
    path('download', download, name='download'),
    path('sync', sync, name='sync')
]
