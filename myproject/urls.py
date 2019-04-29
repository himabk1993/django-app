from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace = 'accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
]
