from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('logistics', views.logistics, name="logistics"),
    path('unit_management', views.unit_management, name="unit_management"),
    path('communication', views.communication, name="communication"),
    path('communicate_airforce', views.communicate_airforce, name="communicate_airforce"),
    path('communicate_naval_forces', views.communicate_naval_forces, name="communicate_naval_forces"),
    path('order_supply', views.order_supply, name="order_supply"),
    path('view_map', views.view_map, name="view_map"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
