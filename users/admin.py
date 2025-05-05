from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Personnalisation de l'affichage des utilisateurs dans Django Admin"""
    
    list_display = ('id', 'username', 'email', 'is_seller', 'is_staff', 'is_superuser', 'created_at')  # Colonnes visibles
    search_fields = ('username', 'email')  # Ajoute une barre de recherche
    list_filter = ('is_seller', 'is_staff', 'is_superuser')  # Filtres pour faciliter la navigation
    ordering = ('username',)  # Trie par username

    # Champs affichés lorsqu'on édite un utilisateur dans l'admin
    fieldsets = (
        ("Informations personnelles", {'fields': ('username', 'email', 'password', 'profile_picture')}),
        ("Permissions", {'fields': ('is_seller', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Dates importantes", {'fields': ('last_login', 'created_at')}),
    )

    # Champs requis pour créer un nouvel utilisateur dans l'admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_seller', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)  # Enregistre CustomUser dans l'admin Django