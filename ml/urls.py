# ml/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PredictView, test_upload

urlpatterns = [
    path('', PredictView.as_view(), name='predict'),
   path('test-upload/', test_upload, name='test-upload'),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
