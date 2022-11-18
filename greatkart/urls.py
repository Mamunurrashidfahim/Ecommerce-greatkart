from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', include('admin_honeypot.urls',namespace='admin_honeypot')),
    path('secure/', admin.site.urls),
    path('cart/',include('cart.urls')), 
    path('category/',include('category.urls')), 
    path('account/',include('accounts.urls')), 
    path('',include('store.urls')), 
    path('orders/',include('orders.urls')), 
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)