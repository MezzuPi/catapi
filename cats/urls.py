from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/usuarios', views.UsuarioViewSet)
router.register(r'api/gatos', views.GatoViewSet)
router.register(r'api/fotos', views.FotoViewSet)
router.register(r'api/votos', views.VotoViewSet)
router.register(r'api/comentarios', views.ComentarioViewSet)
router.register(r'api/tags', views.TagViewSet)
router.register(r'api/foto-tags', views.FotoTagViewSet)
router.register(r'api/badges', views.BadgeViewSet)
router.register(r'api/gato-badges', views.GatoBadgeViewSet)
router.register(r'api/chats', views.ChatViewSet, basename='chat')
router.register(r'api/mensajes', views.MensajeViewSet, basename='mensaje')
router.register(r'api/notificaciones', views.NotificacionViewSet, basename='notificacion')

urlpatterns = [
    path('', include(router.urls)),
] 