from django.urls import path
import apps.my_app.views as v

app_name = 'my_app'

urlpatterns = []

urlpatterns += [path('book/', v.BookView.as_view(), name='book')]
