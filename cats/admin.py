from django.contrib import admin
from django.contrib.auth.models import User
from .models import Gato, Foto, Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'fecha_registro')
    search_fields = ('user__username', 'user__email')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Gato)
class GatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'raza', 'get_owner')
    list_filter = ('raza', 'edad')
    search_fields = ('nombre', 'raza', 'id_usuario__username')

    def get_owner(self, obj):
        return obj.id_usuario.username
    get_owner.short_description = 'Owner'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_usuario":
            kwargs["queryset"] = User.objects.filter(usuario__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ('id_gato', 'descripcion', 'fecha_subida', 'en_miniblog')
    list_filter = ('en_miniblog', 'fecha_subida')
    search_fields = ('descripcion',)
