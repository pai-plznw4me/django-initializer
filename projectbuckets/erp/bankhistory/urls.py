from django.urls import path
from bankhistory.views import index, create, detail, update, delete, download
app_name = 'bankhistory'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'),
	path('update/<int:id>', update, name='update'),
	path('delete/<int:id>', delete, name='delete'),
	path('download', download, name='download'),
	]