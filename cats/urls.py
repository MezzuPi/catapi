from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'gatos', views.GatoViewSet)
router.register(r'fotos', views.FotoViewSet)
router.register(r'votos', views.VotoViewSet)
router.register(r'comentarios', views.ComentarioViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'foto-tags', views.FotoTagViewSet)
router.register(r'badges', views.BadgeViewSet)
router.register(r'gato-badges', views.GatoBadgeViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'mensajes', views.MensajeViewSet)
router.register(r'notificaciones', views.NotificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 