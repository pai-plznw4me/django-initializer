from django.urls import path
from department.views import index, create, detail, update, delete, download, sync

app_name = 'department'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'),
	path('update/<int:id>', update, name='update'),
	path('delete/<int:id>', delete, name='delete'),
	path('download', download, name='download'),
	path('sync', sync, name='sync'),
	]