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
from .views_test import (
    TestTemplateView, test_dual_view, hello_world,
    stats_view, form_test_view, login_view, feed_view
)

# Create a router for API endpoints
router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'usuarios', UsuarioViewSet)
router.register(r'gatos', GatoViewSet)
router.register(r'fotos', FotoViewSet)
router.register(r'votos', VotoViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'tags', TagViewSet)
router.register(r'foto-tags', FotoTagViewSet)
router.register(r'badges', BadgeViewSet)
router.register(r'gato-badges', GatoBadgeViewSet)
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'mensajes', MensajeViewSet, basename='mensaje')
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Test template views
    path('test-template/', TestTemplateView.as_view(), name='test_template'),
    path('test-dual/', test_dual_view, name='test_dual'),
    path('test-dual/<str:format>/', test_dual_view, name='test_dual_format'),
    path('hello/', hello_world, name='hello_world'),
    path('stats/', stats_view, name='stats'),
    path('stats/<str:format>/', stats_view, name='stats_format'),
    path('form-test/', form_test_view, name='form_test'),
    path('feed/', feed_view, name='feed'),
    path('login/', login_view, name='login'),
    path('', login_view, name='home'),  # Make login the default view
] 