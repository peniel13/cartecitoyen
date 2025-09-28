from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify # type: ignore
from decimal import Decimal

# Create your models here.


class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # Nouveaux champs
    is_active_user = models.BooleanField(default=False)  # utilisateur désactivé par défaut
    province = models.CharField(max_length=100, blank=True, null=True)
    ville_ou_district = models.CharField(max_length=100, blank=True, null=True)
    commune_ou_contree = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    def __str__(self):
        return self.email


from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# ============================
# 1. CITOYEN
# ============================
# class Citoyen(models.Model):
#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("valid", "Valide"),
#         ("invalid", "Invalide"),
#     )

#     prenom = models.CharField(max_length=100)
#     nom = models.CharField(max_length=100)
#     date_naissance = models.DateField()
#     lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
#     photo = models.ImageField(upload_to="citoyens/photos/", blank=True, null=True)
#     signature = models.ImageField(upload_to="citoyens/signatures/", blank=True, null=True)

#     numero_identite = models.CharField(max_length=20, unique=True, blank=True)
#     statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="pending")
#     qr_code = models.ImageField(upload_to="citoyens/qrcodes/", blank=True, null=True)

#     date_creation = models.DateTimeField(auto_now_add=True)
#     cree_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="citoyens_crees"
#     )
#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="citoyens_valides"
#     )

#     def save(self, *args, **kwargs):
#         # Génération automatique d’un numéro unique si non défini
#         if not self.numero_identite:
#             self.numero_identite = str(uuid.uuid4().int)[:12]  # 12 chiffres uniques

#         # Génération du QR code lié à l’URL de vérification
#         if not self.qr_code:
#             qr_img = qrcode.make(f"https://monsite.com/verifier/{self.numero_identite}")
#             buffer = BytesIO()
#             qr_img.save(buffer, format="PNG")
#             filename = f"qr_{self.numero_identite}.png"
#             self.qr_code.save(filename, File(buffer), save=False)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.prenom} {self.nom} ({self.numero_identite})"

class DateExpirationfk(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime("%d/%m/%Y")

import uuid
from io import BytesIO
import qrcode
from django.core.files import File
from django.db import models
from django.conf import settings
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings


class Citoyen(models.Model):
    STATUT_CHOICES = (
        ("pending", "En attente"),
        ("valid", "Valide"),
        ("invalid", "Invalide"),
    )

    SEXE_CHOICES = (
        ("M", "Masculin"),
        ("F", "Féminin"),
    )

    ADHESION_CHOICES = (
        ("membre_honneur", "Membre d'honneur"),
        ("president_federation", "Président Fédération"),
        ("president_cellule", "Président Cellule"),
    )

    prenom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
    nationalite = models.CharField(max_length=100, default="Congolaise")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default="M")

    # Localisation organisationnelle
    province = models.CharField(max_length=150, blank=True, null=True)
    federation = models.CharField(max_length=150, blank=True, null=True)
    cellule = models.CharField(max_length=150, blank=True, null=True)

    # Statut d'adhésion
    statut_adhesion = models.CharField(
        max_length=30,
        choices=ADHESION_CHOICES,
        default="membre_honneur"
    )

    photo = models.ImageField(upload_to="citoyens/photos/", blank=True, null=True)
    signature = models.ImageField(upload_to="citoyens/signatures/", blank=True, null=True)

    numero_identite = models.CharField(max_length=20, unique=True, blank=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="pending")
    qr_code = models.ImageField(upload_to="citoyens/qrcodes/", blank=True, null=True)

    
    date_expiration_fk = models.ForeignKey(
        "DateExpirationfk",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="citoyens"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="citoyens_crees"
    )
    valide_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="citoyens_valides"
    )

    def save(self, *args, **kwargs):
        # Numéro unique si absent
        if not self.numero_identite:
            self.numero_identite = str(uuid.uuid4().int)[:12]
        
        # Génération du QR code si absent
        if not self.qr_code:
            # qr_img = qrcode.make(f"https://monsite.com/verifier_qr/?numero={self.numero_identite}")
            qr_img = qrcode.make(f"http://13.244.101.138/user/verifier_qr/?numero={self.numero_identite}")
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            filename = f"qr_{self.numero_identite}.png"
            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.postnom or ''} {self.nom} ({self.numero_identite})"

# class Citoyen(models.Model):
#     STATUT_CHOICES = (
#         ("pending", "En attente"),
#         ("valid", "Valide"),
#         ("invalid", "Invalide"),
#     )

#     SEXE_CHOICES = (
#         ("M", "Masculin"),
#         ("F", "Féminin"),
#     )

#     prenom = models.CharField(max_length=100)
#     postnom = models.CharField(max_length=100, blank=True, null=True)  # ✅ Nouveau
#     nom = models.CharField(max_length=100)
#     date_naissance = models.DateField()
#     lieu_naissance = models.CharField(max_length=150, blank=True, null=True)
#     nationalite = models.CharField(max_length=100, default="Congolaise")  # ✅ Nouveau
#     sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default="M")  # ✅ Nouveau
#     photo = models.ImageField(upload_to="citoyens/photos/", blank=True, null=True)
#     signature = models.ImageField(upload_to="citoyens/signatures/", blank=True, null=True)

#     numero_identite = models.CharField(max_length=20, unique=True, blank=True)
#     statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default="pending")
#     qr_code = models.ImageField(upload_to="citoyens/qrcodes/", blank=True, null=True)

#     date_expiration = models.DateField(blank=True, null=True)  # ✅ Nouveau

#     date_creation = models.DateTimeField(auto_now_add=True)
#     cree_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="citoyens_crees"
#     )
#     valide_par = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="citoyens_valides"
#     )

#     def save(self, *args, **kwargs):
#         # Numéro unique si absent
#         if not self.numero_identite:
#             self.numero_identite = str(uuid.uuid4().int)[:12]

#         # Génération du QR code si absent
#         if not self.qr_code:
#             qr_img = qrcode.make(f"https://monsite.com/verifier_qr/?numero={self.numero_identite}")
#             buffer = BytesIO()
#             qr_img.save(buffer, format="PNG")
#             filename = f"qr_{self.numero_identite}.png"
#             self.qr_code.save(filename, File(buffer), save=False)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.prenom} {self.postnom or ''} {self.nom} ({self.numero_identite})"

# ============================
# 2. DOCUMENTS JUSTIFICATIFS
# ============================
class DocumentJustificatif(models.Model):
    TYPE_CHOICES = (
        ("birth_certificate", "Certificat de naissance"),
        ("old_id", "Ancienne carte"),
        ("passport", "Passeport"),
        ("other", "Autre"),
    )

    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name="documents")
    type_document = models.CharField(max_length=50, choices=TYPE_CHOICES)
    fichier = models.FileField(upload_to="citoyens/documents/")
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_document_display()} - {self.citoyen}"


# ============================
# 3. TEMOINS
# ============================
class Temoin(models.Model):
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name="temoins")
    nom = models.CharField(max_length=100)
    relation = models.CharField(max_length=100, help_text="Relation avec le citoyen (ami, parent, voisin, ...)")
    contact = models.CharField(max_length=20)
    signature = models.ImageField(upload_to="citoyens/temoins/signatures/")

    def __str__(self):
        return f"Témoin {self.nom} pour {self.citoyen}"


# ============================
# 4. JOURNAL DES ACTIONS
# ============================
class JournalAction(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name="journaux")
    action = models.CharField(max_length=200)  # Exemple : "Validation", "Blocage", "Création"
    date_action = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} par {self.utilisateur} sur {self.citoyen}"




from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class News(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True)
    media_file = models.FileField(upload_to='news_media/', blank=True, null=True)  # photo ou vidéo
    created_at = models.DateTimeField(default=timezone.now)

    # 🔥 interactions
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)
    share_count = models.PositiveIntegerField(default=0)

    # 🔧 options
    allow_comments = models.BooleanField(default=True)  # admin peut désactiver les commentaires
    is_active = models.BooleanField(default=True)  # pour archiver/supprimer sans supprimer physiquement

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # possibilité de masquer un commentaire

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.news.title}"


class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Réponse de {self.author} à un commentaire sur {self.comment.news.title}"



from django.conf import settings
from django.conf import settings
from django.db import models

class Contribution(models.Model):
    DEVISE_CHOICES = [
        ('USD', 'Dollar américain (USD)'),
        ('FC', 'Franc congolais (FC)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contributions'
    )
    nom_contributeur = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='FC')  # ✅ Nouveau champ
    id_transaction = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    date_contribution = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom_contributeur} - {self.montant} {self.devise}"
