from django.urls import include
from django.conf.urls.static import static
from erp import settings
from django.urls import include
from django.conf.urls.static import static
from erp import settings

"""
URL configuration for erp project.

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
from django.urls import include
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
path('bankhistory/', include('bankhistory.urls'), name='bankhistory'),
path('bankbook/', include('bankbook.urls'), name='bankbook'),
path('card/', include('card.urls'), name='card'),
path('department/', include('department.urls'), name='department'),
path('purchase/', include('purchase.urls'), name='purchase'),
    path('company/', include('company.urls'), name='company'),
    path('project/', include('project.urls'), name='project'),
    path('employee/', include('employee.urls'), name='employee'),
    path('education/', include('education.urls'), name='education'),
    path('history/', include('history.urls'), name='history'),
    path('account/', include('account.urls'), name='account'),
    path('account/', include('django.contrib.auth.urls')),
    path('doctris_base/', include('doctris_base.urls'), name='doctris_base'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
