"""
URL configuration for app project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app import settings

urlpatterns = [
                  path('', include('home.urls')),  # Default view for the empty path
                  path('explorer/', include('explorer.urls'), name='explorer'),   
                  
                  path('dashboard/', include('home.urls')),
                  path('admin/', admin.site.urls),
                  path('settings/', include('settings.urls')),
                  path('products/', include('products.urls')),

                  path('clients/', include('clients.urls')),
                  path('invoices/', include('invoices.urls')),
                  path('quotations/', include('quotations.urls')),
                  path('contracts/', include('contracts.urls')),

                  path('talents/', include('talents.urls')),
                  path('accounts/', include('allauth.urls')),
                  path('payments/', include('payments.urls')),

                  path('projects/', include('projects.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
