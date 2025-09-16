from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('signout',views.signout, name='signout'),
    path('profile',views.profile, name='profile'),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path('update_profile',views.update_profile, name='update_profile'),
    path("citoyens/", views.citoyens_list, name="citoyens_list"),
    path("citoyens/create/", views.citoyen_create, name="citoyen_create"),
    path("citoyens/<int:pk>/", views.citoyen_detail, name="citoyen_detail"),
    path("citoyens/<int:citoyen_id>/document/add/", views.ajouter_document, name="ajouter_document"),
    
    path("citoyens/<int:citoyen_id>/temoin/add/", views.ajouter_temoin, name="ajouter_temoin"),
    path("verifier/<str:numero_identite>/", views.verifier_citoyen, name="verifier_citoyen"),
    path("journal/", views.journal_list, name="journal_list"),
    path('citoyens/<int:citoyen_id>/carte/download/', views.telecharger_carte, name='telecharger_carte'),
    path('citoyens/<int:citoyen_id>/carte/download/image/', views.telecharger_carte_image, name='telecharger_carte_image'),
    path('citoyens/', views.citoyens_list, name='citoyens_list'),
    path("createurs/", views.liste_createurs, name="liste_createurs"),
    path("verifier_qr/", views.verifier_qr, name="verifier_qr"),
    path("verifier_qr_ajax/", views.verifier_qr_ajax, name="verifier_qr_ajax"),
    path("verifier_qr_scanner/", views.verifier_qr_scanner, name="verifier_qr_scanner"),
    # urls.py
    path("document/<int:pk>/modifier/", views.modifier_document, name="modifier_document"),
    path("document/<int:pk>/supprimer/", views.supprimer_document, name="supprimer_document"),

    path("temoin/<int:pk>/modifier/", views.modifier_temoin, name="modifier_temoin"),
    path("temoin/<int:pk>/supprimer/", views.supprimer_temoin, name="supprimer_temoin"),
    path('user/carte/<int:citoyen_id>/modifier/', views.modifier_carte, name='modifier_carte'),
    path('user/carte/<int:citoyen_id>/supprimer/', views.supprimer_carte, name='supprimer_carte'),
    path('citoyens_dash/', views.citoyens_dashboard_stats, name='citoyens_dashboard_stats'),


]