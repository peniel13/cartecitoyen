from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'profile_pic', 'is_active',
#                     'is_staff', 'is_superuser', 'last_login',)
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "username", "password1", "password2", "profile_pic"),
#             },
#         ),
#     )
    
# admin.site.register(CustomUser, CustomUserAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'profile_pic', 'is_active_user', 
        'is_active', 'is_staff', 'is_superuser', 'role',
        'province', 'ville_ou_district', 'commune_ou_contree', 
        'phone', 'last_login',
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'profile_pic')}),
        ('Informations personnelles', {'fields': ('role', 'bio', 'phone', 'province', 'ville_ou_district', 'commune_ou_contree')}),
        ('Permissions', {'fields': ('is_active_user', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "profile_pic",
                           "role", "bio", "phone", "province", "ville_ou_district", "commune_ou_contree", "is_active_user"),
            },
        ),
    )

    search_fields = ('email', 'username', 'role', 'province', 'ville_ou_district', 'commune_ou_contree')
    list_filter = ('is_active_user', 'is_staff', 'is_superuser', 'province', 'ville_ou_district')

admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from .models import Citoyen, DocumentJustificatif, Temoin, JournalAction,DateExpirationfk

admin.site.register(DateExpirationfk)
# ============================
# INLINE POUR DOCUMENTS
# ============================
class DocumentInline(admin.TabularInline):
    model = DocumentJustificatif
    extra = 1


# ============================
# INLINE POUR TEMOINS
# ============================
class TemoinInline(admin.TabularInline):
    model = Temoin
    extra = 1


# ============================
# ADMIN CITOYEN
# ============================
@admin.register(Citoyen)
class CitoyenAdmin(admin.ModelAdmin):
    list_display = (
        "prenom", "postnom", "nom", "date_naissance", "numero_identite",
        "nationalite", "sexe", "province", "federation", "cellule",
        "statut_adhesion",
        "statut", "cree_par", "valide_par","date_expiration_fk",
    )
    list_filter = ("statut", "statut_adhesion", "province", "federation", "cellule", "date_creation")
    search_fields = ("prenom", "postnom", "nom", "numero_identite", "province", "federation", "cellule")
    inlines = [DocumentInline, TemoinInline]
    readonly_fields = ("numero_identite", "qr_code", "date_creation")

    fieldsets = (
        ("Informations personnelles", {
            "fields": (
                "prenom", "postnom", "nom",
                "date_naissance", "lieu_naissance",
                "nationalite", "sexe", "province", "federation", "cellule",
                "statut_adhesion", "date_expiration_fk",
                "photo", "signature"
            )
        }),
        ("Statut & Identité", {
            "fields": ("numero_identite", "statut", "qr_code")
        }),
        ("Suivi administratif", {
            "fields": ("cree_par", "valide_par", "date_creation")
        }),
    )

# @admin.register(Citoyen)
# class CitoyenAdmin(admin.ModelAdmin):
#     list_display = (
#         "prenom", "postnom", "nom", "date_naissance", "numero_identite",
#         "nationalite", "sexe", "date_expiration",
#         "statut", "cree_par", "valide_par"
#     )
#     list_filter = ("statut", "date_creation")
#     search_fields = ("prenom", "postnom", "nom", "numero_identite")
#     inlines = [DocumentInline, TemoinInline]
#     readonly_fields = ("numero_identite", "qr_code", "date_creation")

#     fieldsets = (
#         ("Informations personnelles", {
#             "fields": (
#                 "prenom", "postnom", "nom",
#                 "date_naissance", "lieu_naissance",
#                 "nationalite", "sexe", "date_expiration",
#                 "photo", "signature"
#             )
#         }),
#         ("Statut & Identité", {
#             "fields": ("numero_identite", "statut", "qr_code")
#         }),
#         ("Suivi administratif", {
#             "fields": ("cree_par", "valide_par", "date_creation")
#         }),
#     )


# ============================
# ADMIN DOCUMENTS
# ============================
@admin.register(DocumentJustificatif)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("citoyen", "type_document", "date_upload")
    list_filter = ("type_document", "date_upload")
    search_fields = ("citoyen__nom", "citoyen__prenom")


# ============================
# ADMIN TEMOINS
# ============================
@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin):
    list_display = ("nom", "relation", "contact", "citoyen")
    search_fields = ("nom", "relation", "citoyen__nom", "citoyen__prenom")


# ============================
# ADMIN JOURNAL
# ============================
@admin.register(JournalAction)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("action", "utilisateur", "citoyen", "date_action")
    list_filter = ("action", "date_action")
    search_fields = ("citoyen__nom", "citoyen__prenom", "utilisateur__email")
