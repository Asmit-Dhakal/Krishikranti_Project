from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    path('product/',ProductView.as_view()),
  #  path('demo',DemoView.as_view()),

]
