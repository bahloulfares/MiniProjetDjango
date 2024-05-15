# urls.py (du projet)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # Ajoutez include ici

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),  # Ajoutez cette ligne pour inclure les URLs d'authentification
    path('', include('studenthelp.urls')),  # Incluez les URLs de votre application studenthelp
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)