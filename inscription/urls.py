 
from django.urls import path
from .views import *
from . import views 
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

   
 

urlpatterns = [
    
    path('', accueil),
    path('', views.accueil, name='accueil'),
    path('apropos/', views.apropos, name='apropos'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    
    path('dashapprenant', dashapprenant, name='dashapprenant'),
    path('dashformateur', dashformateur, name='dashformateur'),
    
    path('pageappr', pageappr, name='pageappr'),
    path('pageform', pageform, name='pageform'),
    
    path('navform', navform, name='navform'),
    path('navappr', navappr, name='navappr'),
    
    path('creation_compte', creation_compte, name='creation_compte'),
    path('attente', message_approuve, name='attente'),
    
    # lien pour approuver les comptes
     

    path('comptes_en_attente_apprenants/', liste_comptes_en_attente_appr, name='liste_comptes_en_attente_appr'),

    
    path('comptes_en_attente_formateurs/', liste_comptes_en_attente_form, name='liste_comptes_en_attente_form'),

  
    path('approuver_formateur/<int:user_id>/', approuver_formateur, name='approuver_formateur'),
    path('desapprouver_formateur/<int:user_id>/', desapprouver_formateur, name='desapprouver_formateur'),


    path('approuver_apprenant/<int:user_id>/', approuver_apprenant, name='approuver_apprenant'),
    path('desapprouver_apprenant/<int:user_id>/', desapprouver_apprenant, name='desapprouver_apprenant'),
    path('exporter-apprenants/', views.exporter_apprenants_csv, name='exporter_apprenants_csv'),
    
    
    path('approuve_formateur', liste_comptes_en_attente_form, name='approuve_formateur'),
    path('approuve_formateur', liste_comptes_en_attente_form, name='approuve_formateur'),
    path('modifier_formateur/<int:user_id>/', modifier_formateur, name='modifier_formateur'),
    path('supprimer_formateur/<int:user_id>/', supprimer_formateur, name='supprimer_formateur'),
    path('exporter_formateurs_csv/', exporter_formateurs_csv, name='exporter_formateurs_csv'),
    path('modules/exporter/<str:format_type>/', views.exporter_modules, name='exporter_modules'),
    
    path('register_admin', register_admin, name='register_admin.html'),
    
   
    path('login/', user_login, name='login'),
    path('liste_cours/', liste_cours, name='liste_cours'),
    path('liste_module', module, name='liste_module'),
    path('liste_module_formateur', module_formateur, name='liste_module_formateur'),

    #path liste des compte deja approuver


    path('liste_comptes_approuves_appr/', liste_comptes_approuves_appr, name='liste_comptes_approuves_appr'),
    path('liste_comptes_approuves_appr_formateur/', liste_comptes_approuves_appr_formateur, name='liste_comptes_approuves_appr_formateur'),
    path('liste_comptes_approuves_form/', liste_comptes_approuves_form, name='liste_comptes_approuves_form'),

    #supprimer apprenant
    path('supprimer_apprenant/<int:user_id>/', supprimer_apprenant, name='supprimer_apprenant'),

    #modifier apprenant
    path('modifier_apprenant/<int:user_id>/', modifier_apprenant, name='modifier_apprenant'),

    #ajouter cours
    path('ajouter_cours', ajouter_cours, name='ajouter_cours'),

     #ajouter module
    path('ajouter_module', ajouter_module, name='ajouter_module'),
    path('logout/', views.deconnexion, name='logout'),

    

    ##supprimer et modiier module
    path('modifier_module/<int:module_id>/', modifier_module, name='modifier_module'),
    path('supprimer_module/<int:module_id>/', supprimer_module, name='supprimer_module'), 

    #nombre
    path('dashboard/', dashboard, name='dashboard'),

    ####afficher paiement
    
    



    path('apprenants/', views.liste_comptes_approuves_appr, name='liste_comptes_approuves_appr'),
    path('apprenants/modifier/<int:user_id>/', views.modifier_apprenant, name='modifier_apprenant'),
    path('apprenants/supprimer/<int:user_id>/', views.supprimer_apprenant, name='supprimer_apprenant'),
    # ... autres URLs ...

    path('apprenants/', views.liste_comptes_approuves_appr, name='liste_comptes_approuves_appr'),
    path('apprenants/modifier/<int:user_id>/', views.modifier_apprenant, name='modifier_apprenant'),
    path('apprenants/supprimer/<int:user_id>/', views.supprimer_apprenant, name='supprimer_apprenant'),
    
    
    path('cours/modifier/<int:pk>/', views.modifier_cours, name='modifier_cours'),
    path('cours/supprimer/<int:pk>/', views.supprimer_cours, name='supprimer_cours'),
    
    
     # Inclure les URLs de messagerie avec un namespace
    path('messagerie/', include('inscription.urls_messagerie')),
    
    # inscription
    
    path('inscription_cours/', inscription_cours, name='inscription_cours'),
    
    # path('get-cours-details/<int:cours_id>/', get_cours_details, name='get_cours_details'),
    path('get-cours-by-module/<int:module_id>/', get_cours_by_module, name='get_cours_by_module'),
   
    path('get-cours/', views.get_cours_by_module, name='get_cours_by_module'),

    path('get-cours-details/', views.get_cours_details, name='get_cours_details'),

    path('get-cours/', views.get_cours_by_module, name='get_cours'),
   
    path('paiement/', views.paiement, name='paiement'),
    
    path('deja_inscrit/', views.deja_inscrit, name='deja_inscrit'),
    
    path('liste_cours_apprenant/', liste_cours_apprenant, name='liste_cours_apprenant'),
    path('liste_cours_formateur/', liste_cours_formateur, name='liste_cours_formateur'),
    
    path('confirmation_paiement/<int:pk>/', views.confirmation_paiement, name='confirmation_paiement'),
    
    path('gestion_paiements/',gestion_paiements, name='gestion_paiements'),
    path('gestion_paiements_apprenant/',gestion_paiements_apprenant, name='gestion_paiements_apprenant'),
    path('gestion_paiements_formateur/',gestion_paiements_formateur, name='gestion_paiements_formateur'),
    
    path('facture/<int:paiement_id>/', views.facture_paiement, name='facture_paiement'),
 
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 