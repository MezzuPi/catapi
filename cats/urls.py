from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, UsuarioViewSet, GatoViewSet, FotoViewSet,
    VotoViewSet, ComentarioViewSet, TagViewSet, FotoTagViewSet,
    BadgeViewSet, GatoBadgeViewSet, ChatViewSet, MensajeViewSet,
    NotificacionViewSet
)

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'api/usuarios', UsuarioViewSet)
router.register(r'api/gatos', GatoViewSet)
router.register(r'api/fotos', FotoViewSet)
router.register(r'api/votos', VotoViewSet)
router.register(r'api/comentarios', ComentarioViewSet)
router.register(r'api/tags', TagViewSet)
router.register(r'api/foto-tags', FotoTagViewSet)
router.register(r'api/badges', BadgeViewSet)
router.register(r'api/gato-badges', GatoBadgeViewSet)
router.register(r'api/chats', ChatViewSet, basename='chat')
router.register(r'api/mensajes', MensajeViewSet, basename='mensaje')
router.register(r'api/notificaciones', NotificacionViewSet, basename='notificacion')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 