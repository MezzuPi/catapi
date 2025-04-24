from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Gato(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gatos')
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    descripcion = models.TextField()
    raza = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - Owner: {self.id_usuario.username}"

class Foto(models.Model):
    id_gato = models.ForeignKey(Gato, on_delete=models.CASCADE)
    imagen = CloudinaryField('image', folder='cat_photos', null=True, blank=True)
    descripcion = models.TextField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    en_miniblog = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_subida']

    def __str__(self):
        return f"Photo of {self.id_gato.nombre}"

class Voto(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=4, choices=[('good', 'Good'), ('evil', 'Evil')])
    fecha_voto = models.DateTimeField(auto_now_add=True)

class Comentario(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=[('raza', 'Raza'), ('edad', 'Edad')])

    def __str__(self):
        return self.nombre

class FotoTag(models.Model):
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    id_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Badge(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class GatoBadge(models.Model):
    id_gato = models.ForeignKey(Gato, on_delete=models.CASCADE)
    id_badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    fecha_otorgado = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    id_usuario_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_usuario_1')
    id_usuario_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_usuario_2')
    fecha_inicio = models.DateTimeField(auto_now_add=True)

class Mensaje(models.Model):
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    id_remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)