from django.db import models
from django.contrib.auth.models import User
 
from django import forms
from django.contrib.auth.models import AbstractUser

from django.db import models
 
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db.models import Count
from django.core.exceptions import ValidationError

 # Create your models here.
################un champ role au modèle User

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('apprenant', 'Apprenant'),
        ('formateur', 'Formateur'),
        
    ]
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='apprenant')

    # Ajouter related_name pour éviter les conflits
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Nom unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Nom unique
        blank=True
    )


    #update
    def get_revenus(self):
        """Calcule le total des revenus des cours validés"""
        from django.db.models import Sum
        return self.cours_set.aggregate(
            total=Sum('paiements__montant'),
            count=Count('paiements')
        )
    #update
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name 
    
####classe pour module  
 
    
     

class Module(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    

    def __str__(self):
        return self.nom
    
####classe pour formateur
class Formateur(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length= 20)
     
    is_approved = models.BooleanField(default=False)  # Ajout de l'approbation
    statut = models.BooleanField(default=False)
    
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, blank=True)
   


    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
####classe pour apprenant
class Apprenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True, )
    is_approved = models.BooleanField(default=False)  # Ajout de l'approbation
    statut = models.BooleanField(default=False)  # Approuvé ou non

    #update
    def peut_effectuer_paiement(self):
        """Vérifie si l'apprenant peut payer"""
        return self.is_approved and self.statut and self.user.is_active
    
    def get_paiements_complets(self):
        """Retourne les paiements validés"""
        return self.paiements.filter(statut='complete')
    
    #update

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
 


class Cours(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    formateur = models.ForeignKey(Formateur, on_delete=models.SET_NULL, null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    heure = models.FloatField(default=0) 

    # 👉 Ajoute ce champ :
    est_actif = models.BooleanField(default=True)

 
 
 

    def __str__(self):
        formateur = f" - {self.formateur}" if self.formateur else ""
        return f"{self.titre}{formateur}"
    

      
####Modèle inscription
from django.contrib.auth import get_user_model

User = get_user_model()

class Inscription(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente de paiement'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]

    apprenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'profile__role': 'apprenant'},  # Si vous utilisez les rôles dans le profil
        related_name='inscriptions'
    )
    
    cours = models.ForeignKey(
        'Cours',  # Remplacez par votre modèle Cours
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    
    date_inscription = models.DateTimeField(default=timezone.now)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    
    # Informations de paiement
    paiement_effectue = models.BooleanField(default=False)
    date_paiement = models.DateTimeField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=50, blank=True)
    reference_paiement = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together = ('apprenant', 'cours')  # Empêche les inscriptions en double
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.apprenant} - {self.cours} ({self.get_statut_display()})"

    



# notification
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

class Conversation(models.Model):
    sujet = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='conversations')
    date_creation = models.DateTimeField(default=timezone.now)
    est_groupe = models.BooleanField(default=False)
    
    def __str__(self):
        return self.sujet

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.TextField()
    fichier = models.FileField(upload_to='messages/fichiers/', null=True, blank=True)
    image = models.ImageField(upload_to='messages/images/', null=True, blank=True)
    date_envoi = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['date_envoi']
    
    def __str__(self):
        return f"Message de {self.expediteur.username} ({self.date_envoi})"

class StatutMessage(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    est_lu = models.BooleanField(default=False)
    est_supprime = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('utilisateur', 'message')
        verbose_name_plural = "Statuts des messages"
        
        
        

####Modèle Paiement
class Paiement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('carte_bancaire', 'Carte Bancaire'),
    ]

    apprenant = models.ForeignKey(User, on_delete=models.CASCADE)
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
    formateur = models.ForeignKey('Formateur', on_delete=models.SET_NULL, null=True, blank=True)

    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)

    # Informations Mobile Money
    operateur = models.CharField(max_length=50, blank=True, null=True)
    numero_mobile = models.CharField(max_length=20, blank=True, null=True)

    # Informations Carte Bancaire
    nom_carte = models.CharField(max_length=100, blank=True, null=True)
    numero_carte = models.CharField(max_length=16, blank=True, null=True)
    date_expiration = models.CharField(max_length=5, blank=True, null=True)  # ex: "12/25"
    cvv = models.CharField(max_length=4, blank=True, null=True)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True)
    paiement_effectue = models.BooleanField(default=False)

    statut = models.CharField(max_length=20, default='en_attente')  # ou 'effectué', 'échoué'

    def __str__(self):
        return f"{self.apprenant.username} - {self.cours.titre} - {self.mode_paiement}"