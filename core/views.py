from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CitoyenForm, DocumentJustificatifForm, TemoinForm,UpdateProfileForm,RegisterForm

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("signin")
        
    context = {"form":form}
    return render(request, "core/signup.html", context)

def signin (request):
    if request.method == 'POST':
        email = request.POST["email"]
        password= request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context= {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("index")

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from django.db.models import Q

@login_required(login_url="signin")
def profile(request, user_id):
    
    
    user = get_object_or_404(CustomUser, id=user_id)
    query = request.GET.get("q")

    citoyens_qs = Citoyen.objects.filter(cree_par=user).order_by("-date_creation")

    if query:
        query = query.strip()
        terms = query.split()  # exemple : "loly danyo 950" → ["loly", "danyo", "950"]

        q_objects = Q()
        for term in terms:
            q_objects |= (
                Q(prenom__icontains=term) |
                Q(postnom__icontains=term) |
                Q(nom__icontains=term) |
                Q(numero_identite__icontains=term) |
                Q(numero_identite__endswith=term)  # match sur les 3 derniers chiffres
            )

        citoyens_qs = citoyens_qs.filter(q_objects)

    # Pagination: 6 cartes par page
    paginator = Paginator(citoyens_qs, 6)
    page = request.GET.get("page")
    try:
        citoyens = paginator.page(page)
    except PageNotAnInteger:
        citoyens = paginator.page(1)
    except EmptyPage:
        citoyens = paginator.page(paginator.num_pages)

    # Nombre total de cartes créées par ce user
    total_cartes = Citoyen.objects.filter(cree_par=user).count()

    context = {
        "user": user,
        "citoyens": citoyens,
        "query": query,
        "total_cartes": total_cartes,
    }
    return render(request, "core/profile.html", context)






@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile mis à jour")
                return redirect("profile", user_id=user.id)
                
    context = {"form": form}
    return render(request, "core/update_profile.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Citoyen, DocumentJustificatif, Temoin
from .forms import CitoyenForm, DocumentJustificatifForm, TemoinForm


# ============================
# LISTE DES CITOYENS
# ============================
# views.py
from django.shortcuts import render
from .models import Citoyen
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Citoyen
from django.db.models import Q
from django.db.models import Count
from django.db.models import Count

@login_required(login_url="signin")
def citoyens_list(request):
    query = request.GET.get("q")
    citoyens_qs = Citoyen.objects.all().order_by("-date_creation")

    # Filtrage par recherche textuelle
    if query:
        query = query.strip()
        terms = query.split()
        q_objects = Q()
        for term in terms:
            q_objects |= (
                Q(prenom__icontains=term) |
                Q(postnom__icontains=term) |
                Q(nom__icontains=term) |
                Q(numero_identite__icontains=term) |
                Q(numero_identite__endswith=term)
            )
        citoyens_qs = citoyens_qs.filter(q_objects)

    # Compteurs par province, fédération et cellule
    provinces_count = citoyens_qs.values('province').annotate(total=Count('id')).order_by('-total')
    federations_count = citoyens_qs.values('federation').annotate(total=Count('id')).order_by('-total')
    cellules_count = citoyens_qs.values('cellule').annotate(total=Count('id')).order_by('-total')

    # Pagination
    paginator = Paginator(citoyens_qs, 6)
    page = request.GET.get("page")
    try:
        citoyens = paginator.page(page)
    except PageNotAnInteger:
        citoyens = paginator.page(1)
    except EmptyPage:
        citoyens = paginator.page(paginator.num_pages)

    return render(
        request,
        "core/list.html",
        {
            "citoyens": citoyens,
            "query": query,
            "provinces_count": provinces_count,
            "federations_count": federations_count,
            "cellules_count": cellules_count,
        },
    )


from django.shortcuts import render
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Citoyen

from django.shortcuts import render
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from .models import Citoyen

@login_required(login_url="signin")
def citoyens_dashboard_stats(request):
    # Récupérer la valeur du filtre (province, federation, cellule, statut_adhesion)
    filtre = request.GET.get("filtre", "").strip()
    valeur = request.GET.get("valeur", "").strip()

    citoyens_qs = Citoyen.objects.all()

    # Appliquer le filtre si défini
    if filtre and valeur:
        filter_kwargs = {f"{filtre}__icontains": valeur}
        citoyens_qs = citoyens_qs.filter(**filter_kwargs)

    # Comptage global par catégorie
    provinces_count = Citoyen.objects.values('province').annotate(total=Count('id')).order_by('-total')
    federations_count = Citoyen.objects.values('federation').annotate(total=Count('id')).order_by('-total')
    cellules_count = Citoyen.objects.values('cellule').annotate(total=Count('id')).order_by('-total')
    statut_adhesion_count = Citoyen.objects.values('statut_adhesion').annotate(total=Count('id')).order_by('-total')

    context = {
        "citoyens_count": citoyens_qs.count(),
        "provinces_count": provinces_count,
        "federations_count": federations_count,
        "cellules_count": cellules_count,
        "statut_adhesion_count": statut_adhesion_count,
        "filtre": filtre,
        "valeur": valeur,
    }
    return render(request, "core/citoyens_stats.html", context)


# @login_required(login_url="signin")
# def citoyens_list(request):
#     query = request.GET.get("q")  # récupération de la recherche
#     citoyens_qs = Citoyen.objects.all().order_by("-date_creation")

#     if query:
#         query = query.strip()
#         terms = query.split()  # sépare "loly danyo loly" → ["loly", "danyo", "loly"]

#         # Construire un filtre combiné
#         q_objects = Q()
#         for term in terms:
#             q_objects |= (
#                 Q(prenom__icontains=term) |
#                 Q(postnom__icontains=term) |
#                 Q(nom__icontains=term) |
#                 Q(numero_identite__icontains=term) |
#                 Q(numero_identite__endswith=term)  # si on tape 950
#             )

#         citoyens_qs = citoyens_qs.filter(q_objects)

#     # ✅ Pagination : 6 cartes par page
#     paginator = Paginator(citoyens_qs, 6)
#     page = request.GET.get("page")

#     try:
#         citoyens = paginator.page(page)
#     except PageNotAnInteger:
#         citoyens = paginator.page(1)
#     except EmptyPage:
#         citoyens = paginator.page(paginator.num_pages)

#     return render(
#         request,
#         "core/list.html",
#         {
#             "citoyens": citoyens,
#             "query": query,
#         },
#     )

# @login_required
# def citoyens_list(request):
#     query = request.GET.get("q")  # récupération de la recherche
#     if query:
#         citoyens_qs = Citoyen.objects.filter(numero_identite__icontains=query).order_by("-date_creation")
#     else:
#         citoyens_qs = Citoyen.objects.all().order_by("-date_creation")
    
#     # ✅ Pagination : 6 cartes par page
#     paginator = Paginator(citoyens_qs, 6)
#     page = request.GET.get('page')
#     try:
#         citoyens = paginator.page(page)
#     except PageNotAnInteger:
#         citoyens = paginator.page(1)
#     except EmptyPage:
#         citoyens = paginator.page(paginator.num_pages)
    
#     return render(request, "core/list.html", {
#         "citoyens": citoyens,
#         "query": query,
#     })




# ============================
# CREER UN CITOYEN
# ============================
# @login_required
# def citoyen_create(request):
#     if request.method == "POST":
#         form = CitoyenForm(request.POST, request.FILES)
#         if form.is_valid():
#             citoyen = form.save(commit=False)
#             citoyen.cree_par = request.user
#             citoyen.save()
#             messages.success(request, "Citoyen enregistré avec succès !")
#             return redirect("ajouter_document")
#     else:
#         form = CitoyenForm()

#     return render(request, "core/create.html", {"form": form})
# @login_required
# def citoyen_create(request):
#     if request.method == "POST":
#         form = CitoyenForm(request.POST, request.FILES)
#         if form.is_valid():
#             citoyen = form.save(commit=False)
#             citoyen.cree_par = request.user
#             citoyen.save()
#             messages.success(request, "Citoyen enregistré avec succès !")
#             # Redirection vers ajouter_document avec l'ID du citoyen
#             return redirect("ajouter_document", citoyen_id=citoyen.id)
#     else:
#         form = CitoyenForm()

#     return render(request, "core/create.html", {"form": form})
@login_required(login_url="signin")
def citoyen_create(request):
    if request.method == "POST":
        form = CitoyenForm(request.POST, request.FILES)
        if form.is_valid():
            citoyen = form.save(commit=False)
            citoyen.cree_par = request.user
            citoyen.save()

            # Journal
            JournalAction.objects.create(
                action="Création du citoyen",
                utilisateur=request.user,
                citoyen=citoyen
            )

            messages.success(request, "Citoyen enregistré avec succès !")
            return redirect("ajouter_document", citoyen_id=citoyen.id)
        else:
            # ⚠️ Si formulaire invalide, afficher un message global
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = CitoyenForm()

    return render(request, "core/create.html", {"form": form})

# @login_required(login_url="signin")
# def citoyen_create(request):
#     if request.method == "POST":
#         form = CitoyenForm(request.POST, request.FILES)
#         if form.is_valid():
#             citoyen = form.save(commit=False)
#             citoyen.cree_par = request.user
#             citoyen.save()

#             # Ajouter au journal
#             JournalAction.objects.create(
#                 action="Création du citoyen",
#                 utilisateur=request.user,
#                 citoyen=citoyen
#             )

#             messages.success(request, "Citoyen enregistré avec succès !")
#             return redirect("ajouter_document", citoyen_id=citoyen.id)
#     else:
#         form = CitoyenForm()

#     return render(request, "core/create.html", {"form": form})

# ============================
# DETAIL D’UN CITOYEN
# ============================
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Citoyen, DocumentJustificatif, Temoin
from django.http import HttpResponse
import qrcode
from io import BytesIO
from django.core.files import File

@login_required(login_url="signin")
def citoyen_detail(request, pk):
    citoyen = get_object_or_404(Citoyen, pk=pk)
    documents = DocumentJustificatif.objects.filter(citoyen=citoyen)
    temoins = Temoin.objects.filter(citoyen=citoyen)

    # Générer QR code si pas déjà créé
    if not citoyen.qr_code:
        qr_img = qrcode.make(f"https://tonsite.com/verifier/{citoyen.numero_identite}")
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        citoyen.qr_code.save(f"qr_{citoyen.id}.png", File(buffer))
        citoyen.save()

    return render(request, "core/detail.html", {
        "citoyen": citoyen,
        "documents": documents,
        "temoins": temoins,
    })



# ============================
# AJOUTER UN DOCUMENT
# ============================
# @login_required
# def ajouter_document(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

#     if request.method == "POST":
#         form = DocumentJustificatifForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save(commit=False)
#             document.citoyen = citoyen
#             document.save()
#             messages.success(request, "Document ajouté avec succès !")
#             # Correction ici
#             return redirect("ajouter_temoin", citoyen_id=citoyen.id)
#     else:
#         form = DocumentJustificatifForm()

#     return render(request, "core/ajouter_document.html", {"form": form, "citoyen": citoyen})
@login_required(login_url="signin")
def ajouter_document(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

    if request.method == "POST":
        form = DocumentJustificatifForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.citoyen = citoyen
            document.save()

            # Ajouter au journal
            JournalAction.objects.create(
                action="Ajout d’un document justificatif",
                utilisateur=request.user,
                citoyen=citoyen
            )

            messages.success(request, "Document ajouté avec succès !")
            return redirect("ajouter_temoin", citoyen_id=citoyen.id)
    else:
        form = DocumentJustificatifForm()

    return render(request, "core/ajouter_document.html", {"form": form, "citoyen": citoyen})



# ============================
# AJOUTER UN TEMOIN
# ============================
# @login_required
# def ajouter_temoin(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

#     if request.method == "POST":
#         form = TemoinForm(request.POST, request.FILES)
#         if form.is_valid():
#             temoin = form.save(commit=False)
#             temoin.citoyen = citoyen
#             temoin.save()
#             messages.success(request, "Témoin ajouté avec succès !")
#             return redirect("citoyen_detail", pk=citoyen.id)  # <=== ici
#     else:
#         form = TemoinForm()

#     return render(request, "core/ajouter_temoin.html", {"form": form, "citoyen": citoyen})
@login_required(login_url="signin")
def ajouter_temoin(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

    if request.method == "POST":
        form = TemoinForm(request.POST, request.FILES)
        if form.is_valid():
            temoin = form.save(commit=False)
            temoin.citoyen = citoyen
            temoin.save()

            # Ajouter au journal
            JournalAction.objects.create(
                action="Ajout d’un témoin",
                utilisateur=request.user,
                citoyen=citoyen
            )

            messages.success(request, "Témoin ajouté avec succès !")
            return redirect("citoyen_detail", pk=citoyen.id)
    else:
        form = TemoinForm()

    return render(request, "core/ajouter_temoin.html", {"form": form, "citoyen": citoyen})
# ============================
# PAGE PUBLIQUE DE VERIFICATION
# ============================
def verifier_citoyen(request, numero_identite):
    citoyen = get_object_or_404(Citoyen, numero_identite=numero_identite)
    return render(request, "core/verifier.html", {"citoyen": citoyen})


from django.db.models import Q
from .models import JournalAction
from django.core.paginator import Paginator


# @login_required
# def journal_list(request):
#     query = request.GET.get("q")
#     journaux = JournalAction.objects.select_related("citoyen", "utilisateur").order_by("-date_action")

#     if query:
#         journaux = journaux.filter(
#             Q(action__icontains=query) |
#             Q(citoyen__nom__icontains=query) |
#             Q(citoyen__prenom__icontains=query) |
#             Q(utilisateur__email__icontains=query)
#         )

#     paginator = Paginator(journaux, 20)  # pagination par 20
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(request, "core/journal_list.html", {"page_obj": page_obj, "query": query})
from django.db.models import Q, Count

from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required(login_url="signin")
def journal_list(request):
    query = request.GET.get("q")

    # Si on a recherché un utilisateur précis
    if query and '@' in query:
        # Vue détail utilisateur
        journaux_user = JournalAction.objects.filter(utilisateur__email=query).select_related("citoyen", "utilisateur")

        # Stats globales de l’utilisateur
        stats_qs = journaux_user.values('action').annotate(total=Count('id'))
        stats_utilisateur = {item['action']: item['total'] for item in stats_qs}

        # Pagination des journaux
        paginator = Paginator(journaux_user.order_by("-date_action"), 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "core/journal_detail_user.html", {
            "query": query,
            "page_obj": page_obj,
            "stats_utilisateur": stats_utilisateur
        })

    else:
        # Vue globale : liste des utilisateurs + nombre total d’actions
        users_stats = (
            JournalAction.objects
            .values("utilisateur__email")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return render(request, "core/journal_users.html", {
            "query": query,
            "users_stats": users_stats
        })



# @login_required
# def journal_list(request):
#     query = request.GET.get("q")
#     journaux = JournalAction.objects.select_related("citoyen", "utilisateur").order_by("-date_action")

#     # Filtrage par recherche
#     if query:
#         journaux = journaux.filter(
#             Q(action__icontains=query) |
#             Q(citoyen__nom__icontains=query) |
#             Q(citoyen__prenom__icontains=query) |
#             Q(utilisateur__email__icontains=query)
#         )

#     # Nombre d’actions par type si recherche par email
#     stats_utilisateur = {}
#     if query and "@" in query:  # recherche par email
#         journaux_user = journaux.filter(utilisateur__email=query)
#         stats_utilisateur = journaux_user.values('action').annotate(count=Count('id'))
        
#     paginator = Paginator(journaux, 20)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(request, "core/journal_list.html", {
#         "page_obj": page_obj,
#         "query": query,
#         "stats_utilisateur": stats_utilisateur,
#     })


from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Citoyen
from reportlab.lib.utils import ImageReader

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Citoyen


from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

@login_required(login_url="signin")
def telecharger_carte(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

    # Ici on met le chemin complet "core/carte_pdf.html"
    html_string = render_to_string("core/carte_pdf.html", {"citoyen": citoyen})

    # Conversion HTML → PDF
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    # Réponse HTTP
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.pdf'
    return response


import imgkit
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Citoyen
import tempfile
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML
from pdf2image import convert_from_bytes
from io import BytesIO
from django.contrib.auth.decorators import login_required
import zipfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from pdf2image import convert_from_bytes
from io import BytesIO
import zipfile
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from pdf2image import convert_from_bytes
from io import BytesIO
import zipfile
from django.templatetags.static import static
from django.conf import settings

from .models import Citoyen

@login_required(login_url="signin")
def telecharger_carte_image(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

    # Préparer toutes les URLs absolues pour les images statiques
    static_base = request.build_absolute_uri('/')[:-1]  # base absolue
    context = {
        "citoyen": citoyen,
        "fondudps": static_base + static("img/fondudps.jpg"),
        "logo_udps": static_base + static("img/logo_udps.jpg"),
        "udps_logo": static_base + static("img/udps_logo.jpg"),
        "coter": static_base + static("img/coter.jpg"),
        
        "MEDIA_URL": request.build_absolute_uri(settings.MEDIA_URL),
    }

    # Générer le HTML
    html_string = render_to_string("core/carte_pdf.html", context)

    # Créer le PDF depuis le HTML
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_bytes = html.write_pdf()

    # Convertir le PDF en images (recto + verso)
    images = convert_from_bytes(pdf_bytes)

    # Créer un fichier ZIP contenant les images PNG
    zip_io = BytesIO()
    with zipfile.ZipFile(zip_io, mode="w") as zip_file:
        for i, image in enumerate(images, start=1):
            img_bytes_io = BytesIO()
            image.save(img_bytes_io, format='PNG')
            img_bytes_io.seek(0)
            zip_file.writestr(f"Carte_{citoyen.numero_identite}_page{i}.png", img_bytes_io.read())

    zip_io.seek(0)
    response = HttpResponse(zip_io, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.zip'
    return response

# @login_required(login_url="signin")
# def telecharger_carte_image(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

#     # Générer le HTML avec les bons chemins d’images
#     html_string = render_to_string("core/carte_pdf.html", {
#         "citoyen": citoyen,
#         "STATIC_URL": request.build_absolute_uri(static("")),
#         "MEDIA_URL": request.build_absolute_uri(settings.MEDIA_URL),
#     })

#     # Créer le PDF depuis le HTML
#     html = HTML(string=html_string, base_url=request.build_absolute_uri())
#     pdf_bytes = html.write_pdf()

#     # Convertir le PDF en images (recto + verso)
#     images = convert_from_bytes(pdf_bytes)

#     # Créer un fichier ZIP contenant les deux images PNG
#     zip_io = BytesIO()
#     with zipfile.ZipFile(zip_io, mode="w") as zip_file:
#         for i, image in enumerate(images, start=1):
#             img_bytes_io = BytesIO()
#             image.save(img_bytes_io, format='PNG')
#             img_bytes_io.seek(0)
#             zip_file.writestr(f"Carte_{citoyen.numero_identite}_page{i}.png", img_bytes_io.read())

#     zip_io.seek(0)
#     response = HttpResponse(zip_io, content_type="application/zip")
#     response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.zip'
#     return response

# @login_required(login_url="signin")
# def telecharger_carte_image(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

#     # Générer le HTML
#     html_string = render_to_string("core/carte_pdf.html", {"citoyen": citoyen})
#     html = HTML(string=html_string, base_url=request.build_absolute_uri())

#     # Générer le PDF en mémoire
#     pdf_bytes = html.write_pdf()

#     # Convertir le PDF en images PNG (une image par page)
#     images = convert_from_bytes(pdf_bytes)

#     # Créer un ZIP contenant les deux images
#     zip_io = BytesIO()
#     with zipfile.ZipFile(zip_io, mode="w") as zip_file:
#         for i, image in enumerate(images, start=1):
#             img_bytes_io = BytesIO()
#             image.save(img_bytes_io, format='PNG')
#             img_bytes_io.seek(0)
#             zip_file.writestr(f"Carte_{citoyen.numero_identite}_page{i}.png", img_bytes_io.read())

#     zip_io.seek(0)
#     response = HttpResponse(zip_io, content_type="application/zip")
#     response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.zip'
#     return response



# @login_required(login_url="signin")
# def telecharger_carte_image(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)
#     html_string = render_to_string("core/carte_pdf.html", {"citoyen": citoyen})

#     # Créer un fichier temporaire
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
#         tmp_file.write(html_string.encode("utf-8"))
#         tmp_file_path = tmp_file.name

#     options = {
#         'format': 'png',
#         'encoding': "UTF-8",
#         'width': 800,
#         'disable-smart-width': '',
#     }

#     # Génération PNG depuis fichier temporaire
#     png_bytes = imgkit.from_file(tmp_file_path, False, options=options)

#     # Supprimer le fichier temporaire
#     os.remove(tmp_file_path)

#     response = HttpResponse(png_bytes, content_type="image/png")
#     response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.png'
#     return response





# @login_required
# def telecharger_carte(request, citoyen_id):
#     citoyen = get_object_or_404(Citoyen, pk=citoyen_id)

#     # Taille carte ID en points
#     width = 85 * 2.83465  # 85 mm
#     height = 54 * 2.83465  # 54 mm

#     from io import BytesIO
#     from reportlab.pdfgen import canvas
#     from reportlab.lib.utils import ImageReader
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=(width, height))

#     # Cadre
#     c.setStrokeColorRGB(0, 0, 0)
#     c.rect(0, 0, width, height, stroke=1, fill=0)

#     # Texte
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(5, height - 15, f"{citoyen.prenom} {citoyen.nom}")
#     c.setFont("Helvetica", 8)
#     c.drawString(5, height - 27, f"N° ID: {citoyen.numero_identite}")
#     c.drawString(5, height - 38, f"Né le: {citoyen.date_naissance.strftime('%d/%m/%Y')}")
#     c.drawString(5, height - 49, f"Lieu: {citoyen.lieu_naissance}")

#     # Photo
#     if citoyen.photo:
#         img = ImageReader(citoyen.photo.path)
#         c.drawImage(img, width - 35, height - 40, width=30, height=35)

#     # QR Code
#     if citoyen.qr_code:
#         qr_img = ImageReader(citoyen.qr_code.path)
#         c.drawImage(qr_img, width - 35, 5, width=30, height=30)

#     c.showPage()
#     c.save()

#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=Carte_{citoyen.numero_identite}.pdf'
#     return response


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Citoyen

@login_required(login_url="signin")
def verifier_qr(request):
    # On récupère le contenu du QR code scanné ou entré par l'utilisateur
    numero = request.GET.get("numero")

    citoyen = None
    statut = "inexistante"

    if numero:
        try:
            citoyen = Citoyen.objects.get(numero_identite=numero)
            if citoyen.statut == "valid":
                statut = "valide"
            else:
                statut = "non_valide"
        except Citoyen.DoesNotExist:
            statut = "inexistante"

    return render(request, "core/verifier_qr.html", {"citoyen": citoyen, "statut": statut})


# core/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Citoyen

from django.http import JsonResponse

@login_required(login_url="signin")
def verifier_qr_ajax(request):
    """
    Vérification QR pour scan en temps réel via JS
    """
    numero = request.GET.get("numero")
    if not numero:
        return JsonResponse({"statut": "inexistante"})

    try:
        citoyen = Citoyen.objects.get(numero_identite=numero)
        statut = "valide" if citoyen.statut == "valid" else "non_valide"
        return JsonResponse({
            "statut": statut,
            "prenom": citoyen.prenom,
            "nom": citoyen.nom,
            "numero_identite": citoyen.numero_identite
        })
    except Citoyen.DoesNotExist:
        return JsonResponse({"statut": "inexistante"})



@login_required(login_url="signin")
def verifier_qr_scanner(request):
    return render(request, "core/verifier_qr_scanner.html")


# ============================
# MODIFIER / SUPPRIMER DOCUMENT
# ============================
@login_required(login_url="signin")
def modifier_document(request, pk):
    document = get_object_or_404(DocumentJustificatif, pk=pk)

    # Vérification : seul le créateur du citoyen peut modifier
    if document.citoyen.cree_par != request.user:
        messages.error(request, "Vous n’avez pas l’autorisation de modifier ce document.")
        return redirect("citoyen_detail", pk=document.citoyen.id)

    if request.method == "POST":
        form = DocumentJustificatifForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            JournalAction.objects.create(
                action="Modification d’un document justificatif",
                utilisateur=request.user,
                citoyen=document.citoyen
            )
            messages.success(request, "Document modifié avec succès !")
            return redirect("citoyen_detail", pk=document.citoyen.id)
    else:
        form = DocumentJustificatifForm(instance=document)

    return render(request, "core/modifier_document.html", {"form": form, "document": document})


@login_required(login_url="signin")
def supprimer_document(request, pk):
    document = get_object_or_404(DocumentJustificatif, pk=pk)

    if document.citoyen.cree_par != request.user:
        messages.error(request, "Vous n’avez pas l’autorisation de supprimer ce document.")
        return redirect("citoyen_detail", pk=document.citoyen.id)

    if request.method == "POST":
        JournalAction.objects.create(
            action="Suppression d’un document justificatif",
            utilisateur=request.user,
            citoyen=document.citoyen
        )
        document.delete()
        messages.success(request, "Document supprimé avec succès !")
        return redirect("citoyen_detail", pk=document.citoyen.id)

    return render(request, "core/confirmer_suppression.html", {"objet": document, "type": "document"})


# ============================
# MODIFIER / SUPPRIMER TEMOIN
# ============================
@login_required(login_url="signin")
def modifier_temoin(request, pk):
    temoin = get_object_or_404(Temoin, pk=pk)

    if temoin.citoyen.cree_par != request.user:
        messages.error(request, "Vous n’avez pas l’autorisation de modifier ce témoin.")
        return redirect("citoyen_detail", pk=temoin.citoyen.id)

    if request.method == "POST":
        form = TemoinForm(request.POST, request.FILES, instance=temoin)
        if form.is_valid():
            form.save()
            JournalAction.objects.create(
                action="Modification d’un témoin",
                utilisateur=request.user,
                citoyen=temoin.citoyen
            )
            messages.success(request, "Témoin modifié avec succès !")
            return redirect("citoyen_detail", pk=temoin.citoyen.id)
    else:
        form = TemoinForm(instance=temoin)

    return render(request, "core/modifier_temoin.html", {"form": form, "temoin": temoin})


@login_required(login_url="signin")
def supprimer_temoin(request, pk):
    temoin = get_object_or_404(Temoin, pk=pk)

    if temoin.citoyen.cree_par != request.user:
        messages.error(request, "Vous n’avez pas l’autorisation de supprimer ce témoin.")
        return redirect("citoyen_detail", pk=temoin.citoyen.id)

    if request.method == "POST":
        JournalAction.objects.create(
            action="Suppression d’un témoin",
            utilisateur=request.user,
            citoyen=temoin.citoyen
        )
        temoin.delete()
        messages.success(request, "Témoin supprimé avec succès !")
        return redirect("citoyen_detail", pk=temoin.citoyen.id)

    return render(request, "core/confirmer_suppression.html", {"objet": temoin, "type": "témoin"})

@login_required(login_url="signin")
def modifier_carte(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, id=citoyen_id)

    # Vérifier que l'utilisateur connecté est le créateur
    if request.user != citoyen.cree_par:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette carte.")
        return redirect("profile")

    if request.method == "POST":
        form = CitoyenForm(request.POST, request.FILES, instance=citoyen)
        if form.is_valid():
            form.save()
            messages.success(request, "Carte citoyenne modifiée avec succès ✅")
            # Corrigé ici : utiliser request.user.id
            return redirect("profile", user_id=request.user.id)
        
    else:
        form = CitoyenForm(instance=citoyen)

    return render(request, "core/modifier_carte.html", {
        "form": form,
        "citoyen": citoyen
    })


@login_required(login_url="signin")
def supprimer_carte(request, citoyen_id):
    citoyen = get_object_or_404(Citoyen, id=citoyen_id)

    # Vérifier que l'utilisateur connecté est le créateur
    if request.user != citoyen.cree_par:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette carte.")
        return redirect("profile")

    if request.method == "POST":
        citoyen.delete()
        messages.success(request, "Carte citoyenne supprimée avec succès ✅")
        return redirect("profile")

    # GET : afficher confirmation
    return render(request, "core/confirmer_suppression_carte.html", {
        "citoyen": citoyen
    })


from django.db.models import Count, Q
from django.shortcuts import render
from .models import CustomUser, Citoyen
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render
from .models import CustomUser, Citoyen

def liste_createurs(request):
    query = request.GET.get("q", "").strip()

    # Base : utilisateurs qui ont créé au moins une carte
    users_qs = CustomUser.objects.annotate(nb_cartes=Count("citoyens_crees")).filter(nb_cartes__gt=0)

    # Stats globales
    total_users = users_qs.count()
    total_cartes = Citoyen.objects.count()

    # Filtrage par localisation
    filtre_active = None
    if query:
        users_qs = users_qs.filter(
            Q(province__icontains=query) |
            Q(ville_ou_district__icontains=query) |
            Q(commune_ou_contree__icontains=query)
        )
        filtre_active = query

    # ✅ Pagination : 6 créateurs par page
    paginator = Paginator(users_qs, 6)
    page = request.GET.get("page")
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # Stats filtrées
    total_users_filtre = users_qs.count()
    total_cartes_filtre = sum(u.nb_cartes for u in users_qs)

    context = {
        "users": users,
        "total_users": total_users,
        "total_cartes": total_cartes,
        "query": query,
        "filtre_active": filtre_active,
        "total_users_filtre": total_users_filtre,
        "total_cartes_filtre": total_cartes_filtre,
    }
    return render(request, "core/liste_createurs.html", context)
