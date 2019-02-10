from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='index'),
    path('update_photos', views.update_photos, name='update_photos'),
    path('update_main_page', views.update_page, name='update_main_page'),
]