from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coffee.urls')),
    path('basket/', include('basket.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'coffee.views.error_404'
handler400 = 'coffee.views.error_400'
handler403 = 'coffee.views.error_403'
handler500 = 'coffee.views.error_500'

