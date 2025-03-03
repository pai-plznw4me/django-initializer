from django.urls import path
from project.views import index, create, detail, update, delete
from project.views import create, detail, update, delete
app_name = 'project'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'), 
	path('update/<int:id>', update, name='update'), 
	path('delete/<int:id>', delete, name='delete')
	]