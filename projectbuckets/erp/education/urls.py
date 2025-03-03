from django.urls import path
from education.views import index, create, detail, update, delete, sync
from education.views import create, detail, update, delete
app_name = 'education'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'), 
	path('update/<int:id>', update, name='update'), 
	path('delete/<int:id>', delete, name='delete'),
	path('sync', sync, name='sync')
	]