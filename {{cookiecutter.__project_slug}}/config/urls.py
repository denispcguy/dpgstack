from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.my_app.urls')),
    path('', include('django_prometheus.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Include builder dev tool for building html
    import debug_toolbar
    from django.shortcuts import render

    def builder(request):
        return render(request, 'builder.html')

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('builder/', builder),
    ]
