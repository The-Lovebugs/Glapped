from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from register.views import register
from django.conf import settings
from  django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', include('Glapped_main.urls')),
    path('', include('django.contrib.auth.urls')),  # Authentication URLs (login, logout, etc.)
    path('terms_and_conditions/', TemplateView.as_view(template_name='terms_and_conditions.html'), name='terms_and_conditions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 404 handler
handler404 = 'Glapped_main.views.custom_404'
