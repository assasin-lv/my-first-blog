from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('info/<str:android_id>/', views.info, name='info'),
    path('log/', views.log, name='log'),
    path('hoy/', views.hoy, name='hoy'),
    path('inventario/', views.inventario, name='inventario'),
    path('logout/', views.logout_view, name='logout'),
    path('terminal/', views.TerminalView.as_view()),
    path('evento/', views.EventoView.as_view()),
    path('api-token-auth/', obtain_auth_token,name='api_token_auth'),
    path('reportes/', views.reportes, name = 'reportes'),
    path('productividad/', views.productividad, name='productividad'),
    path('disponibilidad/', views.disponibilidad, name='disponibilidad'),

]
