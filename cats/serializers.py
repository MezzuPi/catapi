from rest_framework import serializers
from .models import (
    Usuario, Gato, Foto, Voto, Comentario, 
    Tag, FotoTag, Badge, GatoBadge, 
    Chat, Mensaje, Notificacion
)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'avatar_url', 'fecha_registro']
        read_only_fields = ['fecha_registro']

class GatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gato
        fields = ['id', 'id_usuario', 'nombre', 'edad', 'descripcion', 'raza']

class FotoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    nombre_gato = serializers.CharField(source='id_gato.nombre', read_only=True)
    raza_gato = serializers.CharField(source='id_gato.raza', read_only=True)
    
    class Meta:
        model = Foto
        fields = ['id', 'id_gato', 'imagen', 'imagen_url', 'descripcion', 
                 'fecha_subida', 'en_miniblog', 'nombre_gato', 'raza_gato']
        read_only_fields = ['fecha_subida']

    def get_imagen_url(self, obj):
        return obj.imagen.url

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = ['id', 'id_usuario', 'id_foto', 'tipo', 'fecha_voto']
        read_only_fields = ['fecha_voto']

class ComentarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='id_usuario.username', read_only=True)
    avatar_url = serializers.CharField(source='id_usuario.avatar_url', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'id_usuario', 'id_foto', 'contenido', 'fecha_comentario', 
                 'username', 'avatar_url']
        read_only_fields = ['fecha_comentario']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nombre', 'tipo']

class FotoTagSerializer(serializers.ModelSerializer):
    nombre_tag = serializers.CharField(source='id_tag.nombre', read_only=True)
    tipo_tag = serializers.CharField(source='id_tag.tipo', read_only=True)

    class Meta:
        model = FotoTag
        fields = ['id', 'id_foto', 'id_tag', 'nombre_tag', 'tipo_tag']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'nombre', 'descripcion']

class GatoBadgeSerializer(serializers.ModelSerializer):
    nombre_badge = serializers.CharField(source='id_badge.nombre', read_only=True)
    descripcion_badge = serializers.CharField(source='id_badge.descripcion', read_only=True)

    class Meta:
        model = GatoBadge
        fields = ['id', 'id_gato', 'id_badge', 'fecha_otorgado', 
                 'nombre_badge', 'descripcion_badge']
        read_only_fields = ['fecha_otorgado']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'id_usuario_1', 'id_usuario_2', 'fecha_inicio']
        read_only_fields = ['fecha_inicio']

class MensajeSerializer(serializers.ModelSerializer):
    username_remitente = serializers.CharField(source='id_remitente.username', read_only=True)

    class Meta:
        model = Mensaje
        fields = ['id', 'id_chat', 'id_remitente', 'contenido', 
                 'fecha_envio', 'username_remitente']
        read_only_fields = ['fecha_envio']

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'id_usuario', 'tipo', 'mensaje', 'leida', 'fecha_creacion']
        read_only_fields = ['fecha_creacion'] 