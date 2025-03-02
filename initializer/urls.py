"""
URL configuration for initializer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from django.urls import path, include  # <-- 추가된 코드
from django.conf.urls.static import static # <-- 추가된 코드
from initializer import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basicapp/', include('basicapp.urls'), name='basicapp'),
    path('basicauth/', include('basicauth.urls'), name='basicauth'),
    path('proj/', include('proj.urls'), name='proj'),
    path('account/', include('account.urls'), name='account'),  # <-- 추가된 코드
    path('account/', include('django.contrib.auth.urls')),  # <-- 추가된 코드
    path('', include('doctris_base.urls'), name='doctris_base'),
    path('', RedirectView.as_view(url='/home', permanent=False))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # <-- 추가된 코드
