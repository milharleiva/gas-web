from django.urls import path
from gasmenu import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login_view),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view),
    path('change/', views.change),
    path('change/<username>/', views.change),
    path('ingresar_solicitud/', views.ingresar_solicitud, name='ingresar_solicitud'),
    path('buscar_solicitud/', views.buscar_solicitud, name='buscar_solicitud'),
    path('detalle_solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('listar_solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('detalle_solicitud/<int:solicitud_id>/', views.detalle_solicitud, name='detalle_solicitud'),
    path('editar_solicitud/<int:solicitud_id>/', views.editar_solicitud, name='editar_solicitud'),
    path('cambiar_estado/<int:solicitud_id>/', views.cambiar_estado, name='cambiar_estado'),
    path('confirmar_eliminacion/<int:solicitud_id>/', views.confirmar_eliminacion, name='confirmar_eliminacion'),
    path('crear_usuario/', views.crear_usuarios, name='crear_usuario'),
    path('confirmar_eliminacion_usuario/<str:username>/', views.confirmar_eliminacion_usuario, name='confirmar_eliminacion_usuario'),
    path('usuario/<str:username>/', views.detalles_usuario, name='detalles_usuario'),
    path('usuario/editar/<str:username>/', views.editar_usuario, name='editar_usuario'),


]