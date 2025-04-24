from django.db import models

# Create your models here.
class Usuario(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField()

class Gato(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    descripcion = models.TextField()
    raza = models.CharField(max_length=50)

class Foto(models.Model):
    id_gato = models.ForeignKey(Gato, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_subida = models.DateTimeField()
    en_miniblog = models.BooleanField()

class Voto(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=4, choices=[('good', 'Good'), ('evil', 'Evil')])
    fecha_voto = models.DateTimeField()

class Comentario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField()

class Tag(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=[('raza', 'Raza'), ('edad', 'Edad')])

class FotoTag(models.Model):
    id_foto = models.ForeignKey(Foto, on_delete=models.CASCADE)
    id_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Badge(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

class GatoBadge(models.Model):
    id_gato = models.ForeignKey(Gato, on_delete=models.CASCADE)
    id_badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    fecha_otorgado = models.DateTimeField()

class Chat(models.Model):
    id_usuario_1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='chat_usuario_1')
    id_usuario_2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='chat_usuario_2')
    fecha_inicio = models.DateTimeField()

class Mensaje(models.Model):
    id_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    id_remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField()

class Notificacion(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # Puedes hacer un ENUM si tienes los valores
    mensaje = models.TextField()
    leida = models.BooleanField()
    fecha_creacion = models.DateTimeField()