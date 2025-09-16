from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core.models import Citoyen, DocumentJustificatif, Temoin
from core.forms import CitoyenForm, DocumentJustificatifForm, TemoinForm

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    query = request.GET.get("q", "").strip()
    citoyens = None

    if query:
        mots = query.split()
        q_objects = Q()

        for mot in mots:
            if mot.isdigit() and len(mot) <= 4:  
                # Recherche par les derniers chiffres de la carte
                q_objects |= Q(numero_identite__endswith=mot)
            else:
                # Recherche par prénom, nom ou postnom
                q_objects |= (
                    Q(prenom__icontains=mot) |
                    Q(nom__icontains=mot) |
                    Q(postnom__icontains=mot)
                )

        citoyens_qs = Citoyen.objects.filter(q_objects).order_by("-date_creation")

        # Pagination
        paginator = Paginator(citoyens_qs, 6)
        page = request.GET.get("page")
        try:
            citoyens = paginator.page(page)
        except PageNotAnInteger:
            citoyens = paginator.page(1)
        except EmptyPage:
            citoyens = paginator.page(paginator.num_pages)

    return render(request, "base/index.html", {
        "query": query,
        "citoyens": citoyens,
    })
