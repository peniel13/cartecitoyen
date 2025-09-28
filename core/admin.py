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




from django.contrib import admin
from .models import News, Comment, ReplyComment,Contribution

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'media_type', 'created_at', 'allow_comments', 'is_active', 'total_likes', 'total_comments')
    list_filter = ('media_type', 'allow_comments', 'is_active', 'created_at')
    search_fields = ('title', 'content', 'author__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('total_likes', 'total_comments', 'share_count')
    list_editable = ('allow_comments', 'is_active')

    fieldsets = (
        ('Informations générales', {
            'fields': ('author', 'title', 'content', 'media_type', 'media_file')
        }),
        ('Interactions & Options', {
            'fields': ('allow_comments', 'is_active', 'likes', 'share_count', 'total_likes', 'total_comments')
        }),
    )

    filter_horizontal = ('likes',)  # pour choisir les likes directement dans l’admin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'short_content', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author__email', 'news__title')
    list_editable = ('is_active',)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Contenu"


@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'short_content', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author__email', 'comment__content')
    list_editable = ('is_active',)

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Contenu"



from django.contrib import admin
from .models import Contribution
@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = (
        'nom_contributeur', 'montant', 'devise', 'phone_number', 'id_transaction',
        'date_contribution', 'user', 'is_active'
    )
    list_filter = ('is_active', 'date_contribution', 'devise')
    search_fields = ('nom_contributeur', 'id_transaction', 'phone_number')
    readonly_fields = ('date_contribution',)

    # ✅ Actions disponibles dans le menu déroulant "Action"
    actions = ["activer_contributions", "desactiver_contributions"]

    @admin.action(description="✅ Activer les contributions sélectionnées")
    def activer_contributions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} contribution(s) ont été activées avec succès ✅")

    @admin.action(description="🚫 Désactiver les contributions sélectionnées")
    def desactiver_contributions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} contribution(s) ont été désactivées 🚫")
