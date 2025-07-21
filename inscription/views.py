from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from .models import Apprenant
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Formateur, Apprenant
from django.contrib.auth.decorators import login_required
 
from django.contrib.auth.models import User 
from .models import Apprenant, Formateur

from .models import Cours, Module
from .forms import CoursForm 
from .forms import ModuleForm 
from .models import Cours

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Apprenant, Cours
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid
from datetime import timedelta
from django.utils import timezone
import json
from django.http import Http404

# Create your views here.

def accueil(request):
    return render(request, 'accueil.html')
def apropos(request):
    return render(request, 'apropos.html')

def team(request):
    return render(request, 'team.html')
def contact(request):
    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Envoi d'email (configuration requise dans settings.py)
        send_mail(
            f"Contact JOSNET: {subject}",
            f"De: {name} ({email})\n\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        messages.success(request, 'Votre message a été envoyé avec succès !')
        return redirect('contact')

    return render(request, 'contact.html')


#cette fonction retourne la page par defaut
def accueil(request): 
    
    return render(request, "accueil.html")
#cette fonction retourne la page d'accuel vers le dashboard
@login_required(login_url='login')
def dash(request):

    return render(request, 'dashboard.html', {'page_title': 'Dashboard',})


from django.db.models import Sum, Prefetch
from .models import Cours, Paiement, Inscription, Conversation, Message, StatutMessage
@login_required(login_url='login')
def dashapprenant(request):
    user = request.user

    # Récupérer uniquement les paiements valides de l'utilisateur
    paiements_list = Paiement.objects.filter(apprenant=user, paiement_effectue=True).order_by('-date_paiement')

    # Total des paiements
    total_paiement = paiements_list.aggregate(Sum('prix'))['prix__sum'] or 0

    # Cours associés (via paiements)
    if paiements_list.exists():
        cours = Cours.objects.filter(paiement__in=paiements_list).distinct()
        total_heures = cours.aggregate(Sum('heure'))['heure__sum'] or 0
    else:
        cours = []
        total_heures = 0

    # Toutes les inscriptions (à filtrer si besoin)
    inscriptions = Inscription.objects.all()

    # Conversations avec derniers messages + statut lu/non-lu
    conversations = Conversation.objects.filter(participants=user).prefetch_related(
        Prefetch(
            'messages',
            queryset=Message.objects.order_by('-date_envoi'),
            to_attr='all_messages'
        )
    )

    data = []
    for conv in conversations:
        dernier_message = conv.all_messages[0] if conv.all_messages else None
        if dernier_message:
            non_lu = StatutMessage.objects.filter(
                message=dernier_message,
                utilisateur=user,
                est_lu=False
            ).exists()

            data.append({
                'conversation': conv,
                'dernier_message': dernier_message,
                'non_lu': non_lu
            })

    return render(request, 'dashapprenant.html', {
        'conversations': data,
        'cours': cours,
        'total_paiement': total_paiement,
        'paiements_list': paiements_list,
        'inscriptions': inscriptions,
        'total_heures': total_heures
    })

from django.contrib.auth import logout
def deconnexion(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='login')
def dashformateur(request):
    appr_approuves = Apprenant.objects.filter(statut=True).count()
    module_total = Module.objects.all().count()

    formateur = request.user.formateur
    cours = Cours.objects.filter(formateur=formateur)

    total_heures = cours.aggregate(Sum('heure'))['heure__sum'] or 0

    apprenants_approuves = Apprenant.objects.filter(statut=True)

    formateur = request.user.formateur
    cours = Cours.objects.filter(formateur=formateur)

# ✅ Obtenir uniquement les modules liés aux cours du formateur
    modules_enseignes = Module.objects.filter(cours__in=cours).distinct()
    module_total = modules_enseignes.count()

    user = request.user
    conversations = Conversation.objects.filter(participants=user).prefetch_related(
        Prefetch(
            'messages',
            queryset=Message.objects.order_by('-date_envoi'),
            to_attr='all_messages'
        )
    )

    data = []
    for conv in conversations:
        dernier_message = conv.all_messages[0] if conv.all_messages else None
        if dernier_message:
            non_lu = StatutMessage.objects.filter(
                message=dernier_message,
                utilisateur=user,
                est_lu=False
            ).exists()
            data.append({
                'conversation': conv,
                'dernier_message': dernier_message,
                'non_lu': non_lu
            })

    return render(request, 'dashformateur.html', {
        'conversations': data,
        'appr_approuves': appr_approuves,
        'module_total': module_total,
        'cours': cours,
        'apprenants_approuves': apprenants_approuves,
        'total_heures': total_heures  # ✅ sans espace
    })

@login_required(login_url='login')
def pageappr(request):
    return render(request, 'pageappr.html')
@login_required(login_url='login')
def pageform(request):
    return render(request, 'pageform.html')
@login_required(login_url='login')
def navform(request):
    return render(request, 'navform.html')
@login_required(login_url='login')
def navappr(request):
    return render(request, 'navappr.html')
@login_required(login_url='login')
def deja_inscrit(request):
    return render(request, 'deja_inscrit.html')
@login_required(login_url='login')
def confirmation_paiement(request):
    return render(request, 'confirmation_paiement.html')
@login_required(login_url='login')
def liste_cours_apprenant(request):
    cours = Cours.objects.all()
    return render(request, 'liste_cours_apprenant.html', {'cours': cours})


@login_required(login_url='login')
def liste_cours_formateur(request):
    cours = Cours.objects.all()
    return render(request, 'liste_cours_formateur.html', {'cours': cours})

 
@login_required(login_url='login')
def pageappr(request):
    apprenants = Apprenant.objects.all()  # Récupère tous les apprenants
    return render(request, 'pageappr.html', {'apprenants': apprenants})
@login_required
def liste_cours(request):
    cours = Cours.objects.all()
    return render(request, 'liste_cours.html', {'cours': cours})

#fonction pour ajouter cours
@login_required(login_url='login')
def ajouter_cours(request):
    formateurs = Formateur.objects.all()
    modules = Module.objects.all()
    
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer le nouveau cours dans la base de données
            return redirect('liste_cours')  # Rediriger vers la liste des cours

    else:
        form = CoursForm()

    return render(request, 'ajouter_cours.html', {
        'form': form,
        'formateurs': formateurs,
        'modules': modules
    })

#fonction pour ajouter module

@login_required(login_url='login')
def ajouter_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_module')  # Assure-toi que cette URL est définie
    else:
        form = ModuleForm()

    return render(request, 'ajouter_module.html', {'form': form})

###supprimer module
@login_required(login_url='login')
def modifier_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)  # Récupère le module ou affiche une erreur 404
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('liste_module')  # Redirection après modification
    else:
        form = ModuleForm(instance=module)  # Pré-remplit le formulaire avec les données du module

    return render(request, 'modifier_module.html', {'form': form, 'module': module})


#supprimer module
@login_required(login_url='login')
def supprimer_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':  # Vérifie si l'utilisateur a confirmé la suppression
        module.delete()
        return redirect('liste_module')

    return render(request, 'supprimer_module.html', {'module': module})

###fonction pour le module
def module(request):
    modules = Module.objects.all()
       
    return render(request, 'liste_module.html', {'modules': modules})
@login_required(login_url='login')
def module_formateur(request):
    modules = Module.objects.all()
       
    return render(request, 'liste_module_formateur.html', {'modules': modules})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Apprenant

@login_required
def message_approuve(request):
    user = request.user
    message = ""

    try:
        apprenant = Apprenant.objects.get(user=user)

        if apprenant.statut is False:
            message = "❌ Votre compte a été refusé. Veuillez contacter le support pour plus d'informations."
        elif apprenant.statut is None:
            message = "⌛ Votre compte est en attente d'approbation. Merci de patienter pendant la vérification."
        else:
            # Cas rare : il est approuvé mais redirigé ici ?
            message = "✅ Votre compte est déjà approuvé."
    except Apprenant.DoesNotExist:
        message = "❗ Aucune information d'inscription trouvée pour ce compte."

    return render(request, 'attente.html', {'message_statut': message})

#Creation du compte admin
def register_admin(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # ✅ Rendre l'utilisateur admin
            user.is_superuser = True  # ✅ Accès complet
            user.save()
            login(request, user)  # ✅ Connecter directement l'admin
            return redirect('login')  # 🚀 Redirection après connexion

    else:
        form = UserCreationForm()

    return render(request, 'register_admin.html', {'form': form})


#Autentification  admin

 
 

def user_login(request):
    user = None  # ✅ Définit user au début pour éviter l'erreur

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
            return redirect('login')
        
        if user.is_superuser:
            login(request, user)
            return redirect('dashboard') 

        # Vérifier si l'utilisateur est approuvé
        is_approved = False
        redirect_url = 'login'  # Par défaut, rediriger vers la page de connexion

        if hasattr(user, 'apprenant'):
            is_approved = user.apprenant.statut
            redirect_url = 'dashapprenant'  # Redirection pour apprenant

        elif hasattr(user, 'formateur'):
            is_approved = user.formateur.statut
            redirect_url = 'dashformateur'  # Redirection pour formateur

        if not is_approved:
            return render(request, 'attente.html', {'user': user})  

        # Connecter l'utilisateur si son compte est approuvé
        login(request, user)
        return redirect(redirect_url)  # ✅ Redirige selon le rôle

    return render(request, "login.html", {'user': user})


#fonction pour la Creation du compte user

def creation_compte(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get('email')
        telephone = request.POST.get('telephone', '')
        adress = request.POST.get('adress', '')  
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get("role", "")

        # Vérification des champs obligatoires
        required_fields = {
            "username": username,
            "email": email,
            "adress": adress,  
            "password": password,
            "password_confirm": password_confirm,
            "role": role
        }
        
        for field, value in required_fields.items():
            if not value:
                messages.error(request, f"Le champ {field} est obligatoire.")
                return redirect('creation_compte')

        # Vérification du mot de passe
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne sont pas identiques. Veuillez réessayer.")
            return redirect('creation_compte')

        # Validation du mot de passe
        if len(password) < 6 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#%&(),.?!$":{}|<>]', password):
            messages.error(request, "Le mot de passe doit contenir au moins 6 caractères, incluant des lettres, des chiffres et des caractères spéciaux.")
            return redirect('creation_compte')
        
        # Vérification du format email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "L'adresse e-mail est invalide. Veuillez réessayer")
            return redirect('creation_compte')
        
        # Vérification de l'existence de l'utilisateur et adresse e-mail
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà. Réessayez")
            return redirect('creation_compte')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée. Veuillez en choisir une autre.")
            return redirect('creation_compte')
        
        # Création de l'utilisateur de base
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password
        )
        user.is_active = True
        user.save()

        # Création du profil selon le rôle avec les informations supplémentaires
        if role == "formateur":
            formateur = Formateur.objects.create(
                user=user, 
                statut=False,
                telephone=telephone,
                adress=adress  # Correction ici
            )
   
        elif role == "apprenant":
            apprenant = Apprenant.objects.create(
                user=user, 
                statut=False,
                telephone=telephone,
                adress=adress  # Correction ici
            )
        else:
            messages.error(request, "Rôle invalide sélectionné")
            user.delete()  # Supprime l'utilisateur si le rôle est invalide
            return redirect('creation_compte')

        messages.success(request, "Compte créé avec succès. Connectez-vous maintenant.")
        return redirect('login')
    
    return render(request, 'creation_compte.html')


#en attente

def connexion(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Formateur approuvé
            if Formateur.objects.filter(user=user, statut=True).exists():
                login(request, user)
                return redirect("dashformateur")
            
            # Apprenant approuvé
            elif Apprenant.objects.filter(user=user, statut=True).exists():
                login(request, user)
                return redirect("dashapprenant")
            
            # Apprenant refusé
            elif Apprenant.objects.filter(user=user, statut=False).exists():
                messages.error(request, "Votre compte a été refusé. Veuillez contacter le support.")
                return redirect("login")

            # Compte en attente
            else:
                messages.warning(request, "Votre compte est en attente d'approbation.")
                return redirect("attente")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect("login")

    return render(request, "login.html")


#### approuver les comptes.

# Afficher les formateurs non approuvés
@login_required(login_url='login')
def liste_comptes_en_attente_form(request):
    formateurs = Formateur.objects.filter(statut=False)
    print(f"Formateurs non approuvés : {formateurs}")  # Pour déboguer
    return render(request, "approuve_formateur.html", {"formateurs": formateurs})

# Afficher les apprenants non approuvés
@login_required(login_url='login')
def liste_comptes_en_attente_appr(request):
    apprenants = Apprenant.objects.filter(statut=False)
    return render(request, "approuver_apprenant.html", {"apprenants": apprenants})  # Assure-toi que tu passes la bonne variable

 

@staff_member_required
@login_required(login_url='login')
def approuver_apprenant(request, user_id):
    print(f"Recherche d'un apprenant avec user_id={user_id}")  # Debugging
    apprenant = Apprenant.objects.filter(user_id=user_id).first()
    
    if apprenant is None:
        print("Aucun apprenant trouvé avec cet ID")
        messages.error(request, "Aucun apprenant trouvé avec cet ID.")
        return redirect("liste_comptes_en_attente_appr")  # Rediriger vers la liste au lieu d'afficher une erreur 404
    
    apprenant.statut = True
    apprenant.save()
    messages.success(request, f"Le compte de {apprenant.user.username} a été approuvé.")
    return redirect("liste_comptes_en_attente_appr")

@staff_member_required
@login_required(login_url='login')
def desapprouver_apprenant(request, user_id):
    apprenant = get_object_or_404(Apprenant, user_id=user_id)
    apprenant.statut = False  # Désapprouver l'apprenant
    apprenant.save()

    # Optionnel: Supprimer l'apprenant de la liste d'attente après la désapprobation
    apprenant.delete()  # Cela va le supprimer de la base de données

    messages.success(request, f"Le compte de {apprenant.user.username} a été désapprouvé et supprimé de la liste d'attente.")
    return redirect("approuver_apprenant")



@staff_member_required
@login_required(login_url='login')
def approuver_formateur(request, user_id):
    formateur = get_object_or_404(Formateur, user_id=user_id)
    formateur.statut = True
    formateur.save()
    messages.success(request, f"Le compte de {formateur.user.username} a été approuvé.")
    return redirect("liste_comptes_en_attente_form")

@staff_member_required
@login_required(login_url='login')
def desapprouver_formateur(request, user_id):
    formateur = get_object_or_404(Formateur, user_id=user_id)
    formateur.statut = False  # Désapprouver le formateur
    formateur.save()
    formateur.delete()
    messages.success(request, f"Le compte de {formateur.user.username} a été désapprouvé.")
    return redirect("liste_comptes_en_attente_form")

#fonction de liste des utilisateurs approuver

@staff_member_required
@login_required(login_url='login')
def liste_comptes_approuves_appr(request):
    # Récupérer tous les apprenants dont le statut est 'True' (approuvé)
    apprenants_approuves = Apprenant.objects.filter(statut=True)
    return render(request, "liste_comptes_approuves_appr.html", {"apprenants_approuves": apprenants_approuves})


 
def liste_comptes_approuves_appr_formateur(request):
    
    apprenants_approuves = Apprenant.objects.filter(statut=True)
    return render(request, "liste_comptes_approuves_appr_formateur.html", {"apprenants_approuves": apprenants_approuves})

@staff_member_required
def liste_comptes_approuves_form(request):
    # Récupérer tous les formateurs dont le statut est 'True' (approuvé)
    formateurs_approuves = Formateur.objects.filter(statut=True)
    return render(request, "liste_comptes_approuves_form.html", {"formateurs_approuves": formateurs_approuves})

#suprimer apprenant
@staff_member_required
def supprimer_apprenant(request, user_id):
    apprenant = get_object_or_404(Apprenant, user_id=user_id)
    apprenant.delete()
    messages.success(request, "L'apprenant a été supprimé avec succès.")
    return redirect('liste_comptes_approuves_appr')  # Rediriger vers la liste des apprenants approuvés

# modifier apprenant

# Dans views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Apprenant

def modifier_apprenant(request, user_id):
    apprenant = get_object_or_404(Apprenant, user_id=user_id)
    
    if request.method == 'POST':
        # Mise à jour des champs
        apprenant.adress = request.POST.get('adress', apprenant.adress)
        apprenant.telephone = request.POST.get('telephone', apprenant.telephone)
        apprenant.save()
        
        messages.success(request, "L'apprenant a été modifié avec succès.")
        return redirect('liste_comptes_approuves_appr')  # Redirection vers la liste
    
    return render(request, 'modifier_apprenant.html', {'apprenant': apprenant})

from django.db.models import Count
from .models import Formateur, Apprenant, Cours, Module

def dashboard(request):
    # Récupération des statistiques
    context = {
        # Formateurs
        'formateurs_approuves': Formateur.objects.filter(statut=True).count(),
        'formateurs_en_attente': Formateur.objects.filter(statut=False).count(),
        
        # Apprenants
        'apprenants_approuves': Apprenant.objects.filter(statut=True).count(),
        'apprenants_en_attente': Apprenant.objects.filter(statut=False).count(),
        
        # Cours et modules
        'total_cours': Cours.objects.count(),
        'total_modules': Module.objects.count(),
        
        # Autres statistiques (exemples)
        'cours_actifs': Cours.objects.filter(est_actif=True).count(),
        'cours_inactifs': Cours.objects.filter(est_actif=False).count(),
    }
    return render(request, 'dashboard.html', context)
 


    
    
    
  
  
from django.views.decorators.http import require_POST

@require_POST
def supprimer_formateur(request, user_id):
    formateur = get_object_or_404(Formateur, user_id=user_id)
    formateur.delete()
    messages.success(request, "Le formateur a été supprimé avec succès.")
    return redirect('liste_comptes_approuves_form')    
    
def modifier_formateur(request, user_id):
    formateur = get_object_or_404(Formateur, user_id=user_id)
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adress = request.POST.get('adress')

        # Mise à jour de l'utilisateur
        user = formateur.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Mise à jour du formateur
        formateur.telephone = telephone
        formateur.adress = adress
        formateur.save()

        messages.success(request, "Les modifications ont été enregistrées avec succès.")
        return redirect('liste_comptes_approuves_form')

    return render(request, 'modifier_formateur.html', {'formateur': formateur})


from django.http import HttpResponse
import csv

def exporter_formateurs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="formateurs.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nom', 'Email', 'Téléphone', 'Statut'])
    
    formateurs = Formateur.objects.filter(statut=True).select_related('user')
    for formateur in formateurs:
        writer.writerow([
            f"FOR-{formateur.user.id:04d}",
            formateur.user.get_full_name(),
            formateur.user.email,
            formateur.telephone,
            "Actif" if formateur.statut else "Inactif"
        ])
    
    return response

from django.http import HttpResponse
import csv
from django.db.models import Q

def exporter_apprenants_csv(request):
    # Récupérer les paramètres de filtre
    status_filter = request.GET.get('status', '')
    search_term = request.GET.get('search', '')

    # Filtrer les apprenants selon les paramètres
    apprenants = Apprenant.objects.filter(statut=True).select_related('user')
    
    if status_filter == 'active':
        apprenants = apprenants.filter(statut=True)
    elif status_filter == 'inactive':
        apprenants = apprenants.filter(statut=False)
    
    if search_term:
        apprenants = apprenants.filter(
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term) |
            Q(user__email__icontains=search_term) |
            Q(telephone__icontains=search_term) |
            Q(adress__icontains=search_term)
        )

    # Créer la réponse HTTP avec le type CSV
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="apprenants_export.csv"'},
    )
    
    # Créer le writer CSV
    writer = csv.writer(response)
    
    # Écrire l'en-tête
    writer.writerow([
        'ID Apprenant', 
        'Nom Complet', 
        'Email', 
        'Adresse', 
        'Téléphone',
        'Statut',
        'Date Inscription'
    ])

    # Écrire les données
    for apprenant in apprenants:
        writer.writerow([
            f"APP-{apprenant.user.id:04d}",
            apprenant.user.get_full_name(),
            apprenant.user.email,
            apprenant.adress,
            apprenant.telephone,
            "Actif" if apprenant.statut else "Inactif",
            apprenant.user.date_joined.strftime("%Y-%m-%d")
        ])

    return response




from django.http import HttpResponse
import csv
from openpyxl import Workbook
from django.db.models import Q
from .models import Module

def exporter_modules(request, format_type):
    # Récupérer le terme de recherche
    search_term = request.GET.get('search', '')
    
    # Filtrer les modules
    modules = Module.objects.all().prefetch_related('cours_set')
    
    if search_term:
        modules = modules.filter(
            Q(nom__icontains=search_term) |
            Q(description__icontains=search_term)
        )

    if format_type == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="modules_export.csv"'},
        )
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom du Module', 'Description', 'Nombre de Cours'])
        
        for module in modules:
            writer.writerow([
                f"MOD-{module.id:04d}",
                module.nom,
                module.description,
                module.cours_set.count()
            ])
        
        return response
    
    elif format_type == 'excel':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="modules_export.xlsx"'},
        )
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Modules"
        
        # En-têtes
        ws.append(['ID', 'Nom du Module', 'Description', 'Nombre de Cours'])
        
        # Données
        for module in modules:
            ws.append([
                f"MOD-{module.id:04d}",
                module.nom,
                module.description,
                module.cours_set.count()
            ])
        
        wb.save(response)
        return response
    
    return HttpResponse("Format non supporté", status=400)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cours
from .forms import CoursForm

def modifier_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, "Le cours a été modifié avec succès.")
            return redirect('liste_cours')  # Remplacez par le nom de votre vue de liste
    else:
        form = CoursForm(instance=cours)
    return render(request, 'modifier_cours.html', {'form': form, 'cours': cours})
def supprimer_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, "Le cours a été supprimé avec succès.")
        return redirect('liste_cours')
    # Pour les requêtes GET, afficher une page de confirmation
    return render(request, 'confirmation_suppression.html', {'cours': cours})
from django.shortcuts import render, get_object_or_404
from .models import Cours

@login_required(login_url='login')
def liste_cours(request):
    cours = Cours.objects.all().select_related('formateur', 'module')  # Ajoutez les relations nécessaires
    return render(request, 'liste_cours.html', {'cours': cours})




# NOTIFICATION

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Conversation, Message, StatutMessage
from .forms import FormulaireMessage, FormulaireNouvelleConversation
from django.http import JsonResponse
from django.contrib.auth.models import User
from inscription.models import Formateur, Apprenant

@login_required
def boite_reception(request):
    # Récupère uniquement les conversations où l'utilisateur est participant
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related(
        'messages',
        'participants'
    ).order_by('-date_creation')
    
    conversations_data = []
    for conv in conversations:
        dernier_msg = conv.messages.last()
        if dernier_msg:
            statut = StatutMessage.objects.filter(
                message=dernier_msg,
                utilisateur=request.user
            ).first()
            conversations_data.append({
                'conversation': conv,
                'dernier_message': dernier_msg,
                'non_lu': not statut.est_lu if statut else False
            })
    
    return render(request, 'messagerie/boite_reception.html', {
        'conversations': conversations_data
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Conversation, Message, StatutMessage
from .forms import FormulaireMessage
from django.contrib import messages
from django.http import JsonResponse

@login_required
def voir_conversation(request, conversation_id):
    # Optimisation des requêtes avec Prefetch
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related(
            Prefetch('messages', 
                   queryset=Message.objects.select_related('expediteur').order_by('date_envoi')),
            Prefetch('messages__statutmessage_set', 
                   queryset=StatutMessage.objects.filter(utilisateur=request.user),
                   to_attr='user_status')
        ),
        id=conversation_id,
        participants=request.user
    )
    
    # Marquer les messages comme lus
    for msg in conversation.messages.all():
        if msg.expediteur != request.user:
            statut, created = StatutMessage.objects.get_or_create(
                message=msg,
                utilisateur=request.user,
                defaults={'est_lu': True}
            )
            if not created and not statut.est_lu:
                statut.est_lu = True
                statut.save()
    
    if request.method == 'POST':
        form = FormulaireMessage(request.POST, request.FILES)
        if form.is_valid():
            nouveau_message = form.save(commit=False)
            nouveau_message.conversation = conversation
            nouveau_message.expediteur = request.user
            nouveau_message.save()
            
            # Créer des statuts pour les autres participants
            participants = conversation.participants.exclude(id=request.user.id)
            StatutMessage.objects.bulk_create([
                StatutMessage(
                    utilisateur=participant,
                    message=nouveau_message,
                    est_lu=False
                ) for participant in participants
            ])
            
            messages.success(request, "Message envoyé avec succès!")
            return redirect('messagerie:voir_conversation', conversation_id=conversation.id)
    else:
        form = FormulaireMessage()

        if request.user.is_staff:
            template = 'messagerie/conversation_admin.html'
        elif hasattr(request.user, 'is_formateur') and request.user.is_formateur:
            template = 'messagerie/conversation_formateur.html'
        else:
            template = 'messagerie/conversation_apprenant.html'
            
    return render(request, 'messagerie/conversation.html', {
        'conversation': conversation,
        'form': form
    })






@login_required
def conv_apprenant(request, conversation_pk):
     # Optimisation des requêtes avec Prefetch
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related(
            Prefetch('messages', 
                   queryset=Message.objects.select_related('expediteur').order_by('date_envoi')),
            Prefetch('messages__statutmessage_set', 
                   queryset=StatutMessage.objects.filter(utilisateur=request.user),
                   to_attr='user_status')
        ),
        id=conversation_pk,
   
        participants=request.user
    )
    
    # Marquer les messages comme lus
    for msg in conversation.messages.all():
        if msg.expediteur != request.user:
            statut, created = StatutMessage.objects.get_or_create(
                message=msg,
                utilisateur=request.user,
                defaults={'est_lu': True}
            )
            if not created and not statut.est_lu:
                statut.est_lu = True
                statut.save()
    
    if request.method == 'POST':
        form = FormulaireMessage(request.POST, request.FILES)
        if form.is_valid():
            nouveau_message = form.save(commit=False)
            nouveau_message.conversation = conversation
            nouveau_message.expediteur = request.user
            nouveau_message.save()
            
            # Créer des statuts pour les autres participants
            participants = conversation.participants.exclude(id=request.user.id)
            StatutMessage.objects.bulk_create([
                StatutMessage(
                    utilisateur=participant,
                    message=nouveau_message,
                    est_lu=False
                ) for participant in participants
            ])
            
            messages.success(request, "Message envoyé avec succès!")
            return redirect('messagerie:conv_apprenant', conversation_pk=conversation.pk)
    else:
        form = FormulaireMessage()
    return render(request, 'messagerie/conv_apprenant.html',{
        'conversation': conversation,
        'form': form
    } )


@login_required
def conv_formateur(request, conversation_pk):
     # Optimisation des requêtes avec Prefetch
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related(
            Prefetch('messages', 
                   queryset=Message.objects.select_related('expediteur').order_by('date_envoi')),
            Prefetch('messages__statutmessage_set', 
                   queryset=StatutMessage.objects.filter(utilisateur=request.user),
                   to_attr='user_status')
        ),
        id=conversation_pk,
   
        participants=request.user
    )
    
    # Marquer les messages comme lus
    for msg in conversation.messages.all():
        if msg.expediteur != request.user:
            statut, created = StatutMessage.objects.get_or_create(
                message=msg,
                utilisateur=request.user,
                defaults={'est_lu': True}
            )
            if not created and not statut.est_lu:
                statut.est_lu = True
                statut.save()
    
    if request.method == 'POST':
        form = FormulaireMessage(request.POST, request.FILES)
        if form.is_valid():
            nouveau_message = form.save(commit=False)
            nouveau_message.conversation = conversation
            nouveau_message.expediteur = request.user
            nouveau_message.save()
            
            # Créer des statuts pour les autres participants
            participants = conversation.participants.exclude(id=request.user.id)
            StatutMessage.objects.bulk_create([
                StatutMessage(
                    utilisateur=participant,
                    message=nouveau_message,
                    est_lu=False
                ) for participant in participants
            ])
            
            messages.success(request, "Message envoyé avec succès!")
            return redirect('messagerie:conv_formateur', conversation_pk=conversation.pk)
    else:
        form = FormulaireMessage()
    return render(request, 'messagerie/conv_formateur.html',{
        'conversation': conversation,
        'form': form
    } )


 
def voir_conversation_formateur(request):
     
    
    return render(request, 'messagerie/conversation_formateur.html')

def voir_conversation_apprenant(request):
   
    
    return render(request, 'messagerie/conversation_apprenant.html')



@login_required
def nouvelle_conversation(request, reply_to=None):
    # Récupère uniquement les utilisateurs approuvés
    formateurs = User.objects.filter(
        formateur__statut=True
    ).exclude(id=request.user.id)
    
    apprenants = User.objects.filter(
        apprenant__statut=True
    ).exclude(id=request.user.id)
    
    destinataires = formateurs.union(apprenants)
    
    if request.method == 'POST':
        form = FormulaireNouvelleConversation(request.POST)
        if form.is_valid():
            with transaction.atomic():
                conversation = form.save(commit=False)
                conversation.save()
                
                # Ajouter les participants
                conversation.participants.add(request.user)
                for destinataire in form.cleaned_data['destinataires']:
                    conversation.participants.add(destinataire)
                
                # Créer le premier message
                contenu = request.POST.get('contenu', '')
                if contenu:
                    nouveau_message = Message.objects.create(
                        conversation=conversation,
                        expediteur=request.user,
                        contenu=contenu
                    )
                    
                    # Créer des statuts pour les destinataires
                    for destinataire in form.cleaned_data['destinataires']:
                        StatutMessage.objects.create(
                            utilisateur=destinataire,
                            message=nouveau_message,
                            est_lu=False
                        )
                
                messages.success(request, "Conversation créée avec succès!")
                return redirect('messagerie:voir_conversation', conversation_id=conversation.id)
    else:
        form = FormulaireNouvelleConversation()
        form.fields['destinataires'].queryset = destinataires
    
    return render(request, 'messagerie/nouvelle_conversation.html', {
        'form': form,
        'reply_to': reply_to
    })



@login_required
def nouvelle_conversation_formateur(request, reply_to=None):
    # Récupère uniquement les utilisateurs approuvés
    formateurs = User.objects.filter(
        formateur__statut=True
    ).exclude(id=request.user.id)
    
    apprenants = User.objects.filter(
        apprenant__statut=True
    ).exclude(id=request.user.id)
    
    destinataires = formateurs.union(apprenants)
    
    if request.method == 'POST':
        form = FormulaireNouvelleConversation(request.POST)
        if form.is_valid():
            with transaction.atomic():
                conversation = form.save(commit=False)
                conversation.save()
                
                # Ajouter les participants
                conversation.participants.add(request.user)
                for destinataire in form.cleaned_data['destinataires']:
                    conversation.participants.add(destinataire)
                
                # Créer le premier message
                contenu = request.POST.get('contenu', '')
                if contenu:
                    nouveau_message = Message.objects.create(
                        conversation=conversation,
                        expediteur=request.user,
                        contenu=contenu
                    )
                    
                    # Créer des statuts pour les destinataires
                    for destinataire in form.cleaned_data['destinataires']:
                        StatutMessage.objects.create(
                            utilisateur=destinataire,
                            message=nouveau_message,
                            est_lu=False
                        )
                
                messages.success(request, "Conversation créée avec succès!")
                return redirect('messagerie:voir_conversation_formateur', conversation_id=conversation.id)
    else:
        form = FormulaireNouvelleConversation()
        form.fields['destinataires'].queryset = destinataires
    
    return render(request, 'messagerie/nouvelle_conversation_formateur.html', {
        'form': form,
        'reply_to': reply_to
    })

@login_required
def nouvelle_conversation_apprenant(request, reply_to=None):
    # Récupère uniquement les utilisateurs approuvés
    formateurs = User.objects.filter(
        formateur__statut=True
    ).exclude(id=request.user.id)
    
    apprenants = User.objects.filter(
        apprenant__statut=True
    ).exclude(id=request.user.id)
    
    destinataires = formateurs.union(apprenants)
    
    if request.method == 'POST':
        form = FormulaireNouvelleConversation(request.POST)
        if form.is_valid():
            with transaction.atomic():
                conversation = form.save(commit=False)
                conversation.save()
                
                # Ajouter les participants
                conversation.participants.add(request.user)
                for destinataire in form.cleaned_data['destinataires']:
                    conversation.participants.add(destinataire)
                
                # Créer le premier message
                contenu = request.POST.get('contenu', '')
                if contenu:
                    nouveau_message = Message.objects.create(
                        conversation=conversation,
                        expediteur=request.user,
                        contenu=contenu
                    )
                    
                    # Créer des statuts pour les destinataires
                    for destinataire in form.cleaned_data['destinataires']:
                        StatutMessage.objects.create(
                            utilisateur=destinataire,
                            message=nouveau_message,
                            est_lu=False
                        )
                
                messages.success(request, "Conversation créée avec succès!")
                return redirect('messagerie:voir_conversation_apprenant', conversation_id=conversation.id)
    else:
        form = FormulaireNouvelleConversation()
        form.fields['destinataires'].queryset = destinataires
    
    return render(request, 'messagerie/nouvelle_conversation_apprenant.html', {
        'form': form,
        'reply_to': reply_to
    })


@login_required
def supprimer_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    conversation_id = message.conversation.id
    
    if request.user == message.expediteur:
        message.delete()
        messages.success(request, "Message supprimé avec succès.")
    else:
        # Pour les non-expéditeurs, marquer comme supprimé
        StatutMessage.objects.update_or_create(
            message=message,
            utilisateur=request.user,
            defaults={'est_supprime': True}
        )
        messages.success(request, "Message supprimé de votre vue.")
    
    return redirect('messagerie:voir_conversation', conversation_id=conversation_id)

@login_required
def supprimer_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    if request.method == 'POST':
        if request.user.is_staff:  # Admin peut supprimer définitivement
            conversation.delete()
            messages.success(request, "Conversation supprimée définitivement.")
        else:
            # Marquer tous les messages comme supprimés pour cet utilisateur
            for msg in conversation.messages.all():
                StatutMessage.objects.update_or_create(
                    message=msg,
                    utilisateur=request.user,
                    defaults={'est_supprime': True}
                )
            messages.success(request, "Conversation supprimée de votre vue.")
        
        return redirect('messagerie:boite_reception')
    
    return render(request, 'messagerie/confirmation_suppression.html', {
        'conversation': conversation
    })

@login_required
def check_new_messages(request):
    unread_count = StatutMessage.objects.filter(
        utilisateur=request.user,
        est_lu=False,
        est_supprime=False
    ).count()
    return JsonResponse({'unread_count': unread_count})


# EMAIL

def contact_view(request):
    if request.method == 'POST':
        try:
            # Récupération des données
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message_content = request.POST.get('message')

            # Construction de l'email
            email_subject = f"Nouveau message de contact : {subject}"
            email_body = f"""
            De : {name} <{email}>
            Sujet : {subject}
            
            Message :
            {message_content}
            """

            # Envoi de l'email
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Utilisation du paramètre CONTACT_EMAIL
                fail_silently=False,
            )

            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {str(e)}")
            return redirect('contact')

    return render(request, 'contact.html')



# paiement 

from django.views.decorators.csrf import csrf_exempt  # Temporaire pour tests
from .models import Inscription
def inscription_cours(request):
    profile = None
    try:
        profile = request.user.profile
    except AttributeError:
        pass

    if request.method == 'POST':
        cours_id = request.POST.get('cours')
        if not cours_id:
            messages.error(request, "Veuillez sélectionner un cours.")
            return render(request, 'inscription_cours.html', {
                'user': request.user,
                'profile': profile,
                'modules': Module.objects.all()
            })

        try:
            cours = Cours.objects.get(id=cours_id)
        except Cours.DoesNotExist:
            messages.error(request, "Le cours sélectionné n'existe pas.")
            return render(request, 'inscription_cours.html', {
                'user': request.user,
                'profile': profile,
                'modules': Module.objects.all()
            })

        if Inscription.objects.filter(apprenant=request.user, cours=cours).exists():
            messages.warning(request, "Vous êtes déjà inscrit à ce cours")
            return redirect('deja_inscrit')

        Inscription.objects.create(
            apprenant=request.user,
            cours=cours,
            statut='en_attente'
        )

        messages.success(request, "Inscription enregistrée avec succès !")
        return redirect('paiement')

    return render(request, 'inscription_cours.html', {
        'user': request.user,
        'profile': profile,
       
        'modules': Module.objects.all()
    })
    
    
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.utils import timezone
from .models import Inscription, Paiement

def paiement(request):
    try:
        inscription = Inscription.objects.filter(apprenant=request.user, statut='en_attente').latest('date_inscription')
    except Inscription.DoesNotExist:
        messages.error(request, "Aucune inscription en attente trouvée.")
        return redirect('dashboard')

    cours = inscription.cours
    module = cours.module
    apprenant = request.user
    formateur = cours.formateur

    if request.method == 'POST':
        # Générer une référence de paiement unique
        timestamp = str(int(timezone.now().timestamp()))
        reference_paiement = f"JOSNET-{timestamp[-6:]}-{apprenant.id}"

        paiement = Paiement.objects.create(
            apprenant=apprenant,
            cours=cours,
            formateur=formateur,
            mode_paiement=request.POST.get('mode_paiement'),
            prix=cours.price,
            operateur=request.POST.get('operateur', ''),
            numero_mobile=request.POST.get('numero_mobile', ''),
            numero_carte=request.POST.get('numero_carte', ''),
            date_expiration=request.POST.get('date_expiration', ''),
            cvv=request.POST.get('cvv', ''),
            reference_paiement=reference_paiement,
            statut='effectue',
            paiement_effectue=True
        )

        # Mettre à jour l'inscription
        inscription.statut = 'paye'
        inscription.save()

        return redirect('confirmation_paiement', pk=paiement.id)

    return render(request, 'paiement.html', {
        'cours': cours,
        'module': module,
        'apprenant': apprenant,
        'profile': getattr(apprenant, 'profile', None),
    })

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import qrcode
import io
import base64
import os
from .models import Paiement

def confirmation_paiement(request, pk):
    # Récupération du paiement et vérification des permissions
    paiement = get_object_or_404(Paiement, pk=pk, apprenant=request.user)
    apprenant = request.user  # L'apprenant est l'utilisateur connecté
    
    if 'download' in request.GET:
        # Génération du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=4,
        )
        # Contenu du QR code avec les infos importantes
        qr_content = f"""
        JOSNET FACTURE
        Référence: {paiement.reference_paiement}
        Apprenant: {apprenant.get_full_name() or apprenant.username}
        Cours: {paiement.cours}
        Montant: {paiement.prix} Fbu
        Date: {paiement.date_paiement.strftime('%d/%m/%Y')}
        """
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#01314c", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode()

        # Préparation du contexte
        context = {
            'paiement': paiement,
            'apprenant': apprenant,
            'cours': paiement.cours,
            'module': paiement.cours.module,
            'qr_code': qr_code,
            # Ajoutez d'autres variables si nécessaire
        }

        # Rendu du template HTML
        html_string = render_to_string('facture_paiement.html', context)
        
        # Création de la réponse PDF
        response = HttpResponse(content_type='application/pdf')
        filename = f"facture_josnet_{paiement.reference_paiement}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Génération du PDF avec WeasyPrint
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(response)
        
        return response
    
    # Affichage normal (non PDF)
    return render(request, 'confirmation_paiement.html', {
        'paiement': paiement,
        'cours': paiement.cours,
        'module': paiement.cours.module,
        'apprenant': apprenant,  # Ajout de l'apprenant au contexte
    })

from django.core.paginator import Paginator

def gestion_paiements(request):
    # Récupérer tous les paiements
    paiements_list = Paiement.objects.all().order_by('-date_paiement')
    
    # Pagination
    paginator = Paginator(paiements_list, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'paiements': page_obj,
        'page_obj': page_obj,  # Pour la pagination
        'is_paginated': True,  # Pour afficher la pagination
    }
    
    return render(request, 'gestion_paiements.html', context)


def gestion_paiements_apprenant(request):
    # Récupérer tous les paiements
    paiements_list = Paiement.objects.all().order_by('-date_paiement')
    
    # Pagination
    paginator = Paginator(paiements_list, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'paiements': page_obj,
        'page_obj': page_obj,  # Pour la pagination
        'is_paginated': True,  # Pour afficher la pagination
    }
    
    return render(request, 'gestion_paiements_apprenant.html', context)

def gestion_paiements_formateur(request):
    # Récupérer tous les paiements
    paiements_list = Paiement.objects.all().order_by('-date_paiement')
    
    # Pagination
    paginator = Paginator(paiements_list, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'paiements': page_obj,
        'page_obj': page_obj,  # Pour la pagination
        'is_paginated': True,  # Pour afficher la pagination
    }
    
    return render(request, 'gestion_paiements_formateur.html', context)



@login_required

def get_cours_by_module(request):
    cours = Cours.objects.filter(module_id=request.GET.get('module_id'))
    try:
        module_id = request.GET.get('module_id')
        if not module_id:
            return JsonResponse({'error': 'Paramètre module_id requis'}, status=400)

        cours = Cours.objects.filter(module_id=module_id, est_actif=True).select_related('formateur__user')

        cours_data = [
            {
                'id': c.id,
                'nom': c.titre,
                'formateur': str(c.formateur),
                'prix': float(c.price),
                'heure': c.heure
            }
            for c in cours
        ]
        return JsonResponse({'cours': cours_data})
    except Exception as e:
        return JsonResponse({'error': 'Erreur interne du serveur'}, status=500)
    
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def get_cours_details(request):
    cours_id = request.GET.get('cours_id')
    try:
        cours = Cours.objects.get(id=cours_id)
        if cours.formateur:
            formateur_name = cours.formateur.user.get_full_name() or cours.formateur.user.username
        else:
            formateur_name = 'N/A'
        
        data = {
            'success': True,
            'module': cours.module.nom,
            'formateur': formateur_name,
            'prix': str(cours.price),
            'heure': cours.heure,
        }
        return JsonResponse(data)
    except Cours.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cours non trouvé.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

def facture_paiement(request, paiement_id):
    paiement = get_object_or_404(Paiement, pk=paiement_id, apprenant=request.user.apprenant)
    return render(request, 'facture_paiement.html', {
        'paiement': paiement,
        'apprenant': request.user.apprenant,
        'cours': paiement.cours,
        'module': paiement.cours.module
    })   