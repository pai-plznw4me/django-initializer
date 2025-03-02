from django.urls import path
from basicauth.views import index, create, detail, update, delete
from basicauth.views import create, detail, update, delete
app_name = 'basicauth'
urlpatterns = [
	path('create/', create, name='create'), 
	path('index/', index, name='index'), 
	path('detail/<int:id>', detail, name='detail'), 
	path('update/<int:id>', update, name='update'), 
	path('delete/<int:id>', delete, name='delete')
	]