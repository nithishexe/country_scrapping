from django.urls import path

from . import views

urlpatterns = [
    path('<country_name>/', views.country_data, name='country_data'),
]