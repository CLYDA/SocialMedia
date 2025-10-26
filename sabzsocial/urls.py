from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social.urls', namespace='social')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('__debug__/', include("debug_toolbar.urls")),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)