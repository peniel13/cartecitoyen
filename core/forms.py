from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    email= forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email adress"}))
    username= forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ["email","username","password1","password2"]

from django import forms
from django.contrib.auth import get_user_model

class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter firstname"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter lastname"})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter username"})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter email address"})
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter address"}),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter phone"}),
        required=False
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Enter bio"}),
        required=False
    )
    role = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter role"}),
        required=False
    )

    # --- Nouveaux champs (sans is_active_user) ---
    province = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter province"}),
        required=False
    )
    ville_ou_district = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter ville ou district"}),
        required=False
    )
    commune_ou_contree = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Enter commune ou contrée"}),
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name", "last_name", "username", "email", "address",
            "bio", "phone", "role", "profile_pic",
            "province", "ville_ou_district", "commune_ou_contree"
        ]



from django import forms
from .models import Citoyen, DocumentJustificatif, Temoin,DateExpirationfk

from django import forms
from .models import Citoyen

from django import forms
from .models import Citoyen


class CitoyenForm(forms.ModelForm):
    prenom = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez le prénom"
        })
    )
    postnom = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez le postnom"
        })
    )
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez le nom"
        })
    )
    date_naissance = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )
    lieu_naissance = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez le lieu de naissance"
        })
    )
    nationalite = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez la nationalité"
        })
    )
    sexe = forms.ChoiceField(
        choices=Citoyen.SEXE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # ✅ Nouveaux champs localisation
    province = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez la province"
        })
    )
    federation = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez la fédération"
        })
    )
    cellule = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez la cellule"
        })
    )

    # ✅ Nouveau champ statut d’adhésion
    statut_adhesion = forms.ChoiceField(
        choices=Citoyen.ADHESION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # date_expiration = forms.DateField(
    #     widget=forms.DateInput(attrs={
    #         "class": "form-control",
    #         "type": "date"
    #     })
    # )
    date_expiration_fk = forms.ModelChoiceField(
        queryset=DateExpirationfk.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "placeholder": "Télécharger une photo"
        })
    )
    signature = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "placeholder": "Télécharger une signature"
        })
    )
    statut = forms.ChoiceField(
        choices=Citoyen.STATUT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Citoyen
        fields = [
            "prenom", "postnom", "nom", "date_naissance", "lieu_naissance",
            "nationalite", "sexe", "province", "federation", "cellule",
            "statut_adhesion", "date_expiration_fk", "photo", "signature", "statut"
        ]

# class CitoyenForm(forms.ModelForm):
#     prenom = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Entrez le prénom"
#         })
#     )
#     postnom = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Entrez le postnom"
#         })
#     )
#     nom = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Entrez le nom"
#         })
#     )
#     date_naissance = forms.DateField(
#         widget=forms.DateInput(attrs={
#             "class": "form-control",
#             "type": "date"
#         })
#     )
#     lieu_naissance = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Entrez le lieu de naissance"
#         })
#     )
#     nationalite = forms.CharField(
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Entrez la nationalité"
#         })
#     )
#     sexe = forms.ChoiceField(
#         choices=Citoyen.SEXE_CHOICES,  # ⚡ tu dois avoir SEXE_CHOICES dans ton modèle
#         widget=forms.Select(attrs={"class": "form-control"})
#     )
#     date_expiration = forms.DateField(
#         widget=forms.DateInput(attrs={
#             "class": "form-control",
#             "type": "date"
#         })
#     )
#     photo = forms.ImageField(
#         widget=forms.FileInput(attrs={
#             "class": "form-control",
#             "placeholder": "Télécharger une photo"
#         })
#     )
#     signature = forms.ImageField(
#         widget=forms.FileInput(attrs={
#             "class": "form-control",
#             "placeholder": "Télécharger une signature"
#         })
#     )
#     statut = forms.ChoiceField(
#         choices=Citoyen.STATUT_CHOICES,  # ⚡ idem, définis STATUT_CHOICES dans ton modèle
#         widget=forms.Select(attrs={"class": "form-control"})
#     )

#     class Meta:
#         model = Citoyen
#         fields = [
#             "prenom", "postnom", "nom", "date_naissance", "lieu_naissance",
#             "nationalite", "sexe", "date_expiration",
#             "photo", "signature", "statut"
#         ]

# ============================
# FORMULAIRE CITOYEN
# ============================
# class CitoyenForm(forms.ModelForm):
#     class Meta:
#         model = Citoyen
#         fields = [
#             "prenom", "postnom", "nom", "date_naissance", "lieu_naissance",
#             "nationalite", "sexe", "date_expiration",
#             "photo", "signature", "statut"
#         ]
#         widgets = {
#             "prenom": forms.TextInput(attrs={"class": "form-control"}),
#             "postnom": forms.TextInput(attrs={"class": "form-control"}),  # ✅ Nouveau
#             "nom": forms.TextInput(attrs={"class": "form-control"}),
#             "date_naissance": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
#             "lieu_naissance": forms.TextInput(attrs={"class": "form-control"}),
#             "nationalite": forms.TextInput(attrs={"class": "form-control"}),  # ✅ Nouveau
#             "sexe": forms.Select(attrs={"class": "form-control"}),  # ✅ Nouveau (choices du modèle)
#             "date_expiration": forms.DateInput(attrs={"type": "date", "class": "form-control"}),  # ✅ Nouveau
#             "photo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
#             "signature": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
#             "statut": forms.Select(attrs={"class": "form-control"}),
#         }



# ============================
# FORMULAIRE DOCUMENT
# ============================
class DocumentJustificatifForm(forms.ModelForm):
    class Meta:
        model = DocumentJustificatif
        fields = ["type_document", "fichier"]
        widgets = {
            "type_document": forms.Select(attrs={"class": "form-control"}),
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


# ============================
# FORMULAIRE TEMOIN
# ============================
from django import forms
from .models import Temoin

class TemoinForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez le nom du témoin"
        })
    )
    relation = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Relation avec le citoyen"
        })
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Contact du témoin"
        })
    )
    signature = forms.ImageField(
        widget=forms.FileInput(attrs={
            "class": "form-control",
            "placeholder": "Télécharger la signature"
        })
    )

    class Meta:
        model = Temoin
        fields = ["nom", "relation", "contact", "signature"]

# class TemoinForm(forms.ModelForm):
#     class Meta:
#         model = Temoin
#         fields = ["nom", "relation", "contact", "signature"]
#         widgets = {
#             "nom": forms.TextInput(attrs={"class": "form-control"}),
#             "relation": forms.TextInput(attrs={"class": "form-control"}),
#             "contact": forms.TextInput(attrs={"class": "form-control"}),
#             "signature": forms.ClearableFileInput(attrs={"class": "form-control"}),
#         }
