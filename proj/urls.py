from django.urls import path
from proj.views import index, create, detail, update, delete, downloadproject
app_name = 'proj'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'), 
	path('update/<int:id>', update, name='update'), 
	path('delete/<int:id>', delete, name='delete'),
	path('downloadproject/<int:id>', downloadproject, name='downloadproject'),
	]