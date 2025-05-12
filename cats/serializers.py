from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Usuario, Gato, Foto, Voto, Comentario, 
    Tag, FotoTag, Badge, GatoBadge, 
    Chat, Mensaje, Notificacion
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

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
    id_usuario_details = serializers.SerializerMethodField()
    username = serializers.CharField(source='id_usuario.username', read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'id_usuario', 'id_foto', 'contenido', 'fecha_comentario', 
                'username', 'avatar_url', 'id_usuario_details']
        read_only_fields = ['fecha_comentario']
    
    def get_avatar_url(self, obj):
        try:
            usuario = Usuario.objects.get(user=obj.id_usuario)
            return usuario.avatar_url
        except Usuario.DoesNotExist:
            return None
    
    def get_id_usuario_details(self, obj):
        return {
            'id': obj.id_usuario.id,
            'username': obj.id_usuario.username
        }

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