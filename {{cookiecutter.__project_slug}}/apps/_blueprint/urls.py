from django.urls import path
from . import views

app_name = '_blueprint'
urlpatterns = [
    path('', views.BlueprintSimpleModelView.as_view(), name='table'),
    path('<int:pk>/', views.BlueprintSimpleModelView.as_view(), name='table_detail'),
]