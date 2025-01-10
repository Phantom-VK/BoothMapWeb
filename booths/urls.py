from django.urls import path
from . import views

urlpatterns = [
    path('', views.city_selection, name='city_selection'),
    path('api/talukas/<str:city>/', views.get_talukas, name='get_talukas'),
    path('api/booths/<str:city>/<str:taluka>/', views.get_booths_by_taluka, name='get_booths_by_taluka'),
    path('map/', views.map_view, name='map_view'),
]