from django.urls import path
from company.views import index, create, detail, update, delete, sync, delete_all
from company.views import create, detail, update, delete
app_name = 'company'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'), 
	path('update/<int:id>', update, name='update'), 
	path('delete/<int:id>', delete, name='delete'),
	path('delete_all', delete_all, name='delete_all'),

	path('sync', sync, name='sync')
	]