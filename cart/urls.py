from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('cart/',CartView.as_view(),name='cart'),
    path('orders/', OrderAPIView.as_view(), name='orders'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
