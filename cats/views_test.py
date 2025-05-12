from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.models import User
import json

from .models import (
    Usuario, Gato, Foto, Voto, Comentario,
    Tag, FotoTag, Badge, GatoBadge,
    Chat, Mensaje, Notificacion
)
from .serializers import (
    GatoSerializer, FotoSerializer,
    VotoSerializer, ComentarioSerializer, TagSerializer,
    FotoTagSerializer, BadgeSerializer, GatoBadgeSerializer,
)

# Test Template Views
class TestTemplateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    
    def get(self, request):
        cats = Gato.objects.all()
        serializer = GatoSerializer(cats, many=True)
        context = {
            'message': 'This is a test page for the Cat API',
            'cats': cats,
            'api_data_json': json.dumps(serializer.data, indent=2)
        }
        return Response(context, template_name='cats/test.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([AllowAny])
def test_dual_view(request, format=None):
    """Test endpoint that can render both HTML and JSON"""
    cats = Gato.objects.all()
    serializer = GatoSerializer(cats, many=True)
    
    # If HTML format is requested
    if request.accepted_renderer.format == 'html':
        context = {
            'message': 'This is a test page with dual rendering',
            'cats': cats,
            'api_data_json': json.dumps(serializer.data, indent=2)
        }
        return Response(context, template_name='cats/test.html')
    
    # Default JSON response
    return Response(serializer.data)

# Simple plain text response
@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    return HttpResponse("Hello, Cat API World! This is a simple test endpoint.")

# Statistics view
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([AllowAny])
def stats_view(request, format=None):
    """Statistics view that shows counts and aggregates from the database"""
    # Get counts
    total_cats = Gato.objects.count()
    total_photos = Foto.objects.count()
    total_users = User.objects.count()
    total_votes = Voto.objects.count()
    
    # Get top breeds
    top_breeds = Gato.objects.values('raza').annotate(
        count=Count('raza')
    ).order_by('-count')[:5]
    
    # Get recent activity
    recent_photos = Foto.objects.order_by('-fecha_subida')[:5]
    recent_votes = Voto.objects.order_by('-fecha_voto')[:5]
    recent_comments = Comentario.objects.order_by('-fecha_comentario')[:5]
    
    # Combine and sort recent activity
    recent_activity = []
    for photo in recent_photos:
        recent_activity.append({
            'activity_type': f'New photo of {photo.id_gato.nombre}',
            'date': photo.fecha_subida
        })
    
    for vote in recent_votes:
        recent_activity.append({
            'activity_type': f'{vote.tipo.capitalize()} vote by {vote.id_usuario.username}',
            'date': vote.fecha_voto
        })
    
    for comment in recent_comments:
        recent_activity.append({
            'activity_type': f'Comment by {comment.id_usuario.username}',
            'date': comment.fecha_comentario
        })
    
    # Sort by date
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_activity[:10]
    
    context = {
        'total_cats': total_cats,
        'total_photos': total_photos,
        'total_users': total_users,
        'total_votes': total_votes,
        'top_breeds': top_breeds,
        'recent_activity': recent_activity
    }
    
    # If HTML format is requested
    if request.accepted_renderer.format == 'html':
        return Response(context, template_name='cats/stats.html')
    
    # Default JSON response
    return Response(context)

# Form test view
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([AllowAny])
def form_test_view(request):
    """View to test form submission with templates"""
    return Response({}, template_name='cats/form_test.html')

# Login view
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([AllowAny])
def login_view(request):
    """Login page"""
    return Response({}, template_name='cats/login.html')

# Cat Feed view (Tinder-like experience)
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([AllowAny])
def feed_view(request):
    """Tinder-like feed for cat photos"""
    return Response({}, template_name='cats/feed.html') 