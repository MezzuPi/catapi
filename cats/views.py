from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from .models import (
    Usuario, Gato, Foto, Voto, Comentario,
    Tag, FotoTag, Badge, GatoBadge,
    Chat, Mensaje, Notificacion
)
from .serializers import (
    UsuarioSerializer, GatoSerializer, FotoSerializer, VotoSerializer,
    ComentarioSerializer, TagSerializer, FotoTagSerializer,
    BadgeSerializer, GatoBadgeSerializer, ChatSerializer,
    MensajeSerializer, NotificacionSerializer
)

# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def perfil(self, request, pk=None):
        usuario = self.get_object()
        gatos = Gato.objects.filter(id_usuario=usuario)
        badges = GatoBadge.objects.filter(id_gato__id_usuario=usuario)
        return Response({
            'usuario': UsuarioSerializer(usuario).data,
            'gatos': GatoSerializer(gatos, many=True).data,
            'badges': GatoBadgeSerializer(badges, many=True).data
        })

class GatoViewSet(viewsets.ModelViewSet):
    queryset = Gato.objects.all()
    serializer_class = GatoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'raza']

    def get_queryset(self):
        if self.action == 'list':
            return Gato.objects.filter(id_usuario=self.request.user)
        return super().get_queryset()

class FotoViewSet(viewsets.ModelViewSet):
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """
        Returns random photos for the feed.
        """
        # Get 10 random photos
        fotos = Foto.objects.order_by('?')[:10]
        serializer = self.get_serializer(fotos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def toggle_miniblog(self, request, pk=None):
        foto = self.get_object()
        if foto.id_gato.id_usuario != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        foto.en_miniblog = not foto.en_miniblog
        foto.save()
        return Response(FotoSerializer(foto).data)

class VotoViewSet(viewsets.ModelViewSet):
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['id_usuario'] = request.user.id
        request.data['fecha_voto'] = timezone.now()
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def rankings(self, request):
        periodo = request.query_params.get('periodo', 'all')
        
        # Filter votes based on period
        votos = Voto.objects.all()
        if periodo == 'week':
            votos = votos.filter(fecha_voto__gte=timezone.now() - timezone.timedelta(days=7))
        elif periodo == 'month':
            votos = votos.filter(fecha_voto__gte=timezone.now() - timezone.timedelta(days=30))

        # Get top good and evil cats
        good_cats = votos.filter(tipo='good').values('id_foto__id_gato').annotate(
            total=Count('id')).order_by('-total')[:10]
        evil_cats = votos.filter(tipo='evil').values('id_foto__id_gato').annotate(
            total=Count('id')).order_by('-total')[:10]

        return Response({
            'good_kitties': good_cats,
            'evil_kitties': evil_cats
        })

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['id_usuario'] = request.user.id
        request.data['fecha_comentario'] = timezone.now()
        return super().create(request, *args, **kwargs)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class FotoTagViewSet(viewsets.ModelViewSet):
    queryset = FotoTag.objects.all()
    serializer_class = FotoTagSerializer
    permission_classes = [IsAuthenticated]

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]

class GatoBadgeViewSet(viewsets.ModelViewSet):
    queryset = GatoBadge.objects.all()
    serializer_class = GatoBadgeSerializer
    permission_classes = [IsAuthenticated]

class ChatViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(
            Q(id_usuario_1=self.request.user) | 
            Q(id_usuario_2=self.request.user)
        )

    def create(self, request, *args, **kwargs):
        request.data['fecha_inicio'] = timezone.now()
        return super().create(request, *args, **kwargs)

class MensajeViewSet(viewsets.ModelViewSet):
    serializer_class = MensajeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat_id', None)
        if chat_id:
            return Mensaje.objects.filter(id_chat=chat_id)
        return Mensaje.objects.filter(
            id_chat__in=Chat.objects.filter(
                Q(id_usuario_1=self.request.user) | 
                Q(id_usuario_2=self.request.user)
            )
        )

    def create(self, request, *args, **kwargs):
        request.data['id_remitente'] = request.user.id
        request.data['fecha_envio'] = timezone.now()
        return super().create(request, *args, **kwargs)

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(id_usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response(NotificacionSerializer(notificacion).data)
