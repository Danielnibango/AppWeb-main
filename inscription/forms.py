from django import forms
from django.contrib.auth.models import User
from .models import Apprenant, Formateur, Cours, Module 
from django.contrib.auth.forms import UserCreationForm

# Formulaire de base pour les utilisateurs
class BaseUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'username': 'Nom d\'utilisateur',
            'password': 'Mot de passe',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}),
            'username': forms.TextInput(attrs={'placeholder': 'Entrez un nom d\'utilisateur'}),
        }

# Formulaire pour l'administrateur
class UserForm(BaseUserForm):
    role = forms.ChoiceField(
        choices=[
            ('admin', 'Administrateur'),
            ('apprenant', 'Apprenant'),
            ('formateur', 'Formateur'),
            
        ],
        required=True,
        label='Rôle'
    )

    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['role']

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['admin', 'apprenant', 'formateur']:
            raise forms.ValidationError("Rôle invalide.")
        return role

# Formulaire pour l'apprenant
class ApprenantUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        pass

class ApprenantForm(forms.ModelForm):
    class Meta:
        model = Apprenant
        fields = ['telephone']
        labels = {
            'telephone': 'Téléphone',
        }
        widgets = {
            'telephone': forms.TextInput(attrs={'placeholder': 'Entrez votre numéro de téléphone'}),
        }

# Formulaire pour le stagiaire
class StagiaireUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        pass

 

# Formulaire pour le formateur
class FormateurUserForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        pass

class FormateurForm(forms.ModelForm):
    class Meta:
        model = Formateur
        fields = ['adress', 'telephone']
        labels = {
            'adress': 'Adresse',
            'telephone': 'Téléphone',
        }
        widgets = {
            'adress': forms.TextInput(attrs={'placeholder': 'Entrez votre adresse'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Entrez votre numéro de téléphone'}),
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")


#modifier apprenant

class ApprenantForm(forms.ModelForm):
    class Meta:
        model = Apprenant
        fields = ['user', 'adress', 'telephone']

#form pour ajoutez cours

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'formateur', 'module' , 'price', 'date_debut', 'date_fin']


#form pour ajouter module

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['nom', 'description']



# notifications

from django import forms
from .models import Message, Conversation
from django.contrib.auth.models import User
from inscription.models import Apprenant, Formateur

class FormulaireNouvelleConversation(forms.ModelForm):
    destinataires = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Sélectionnez les destinataires"
    )
    
    class Meta:
        model = Conversation
        fields = ['sujet']
        labels = {
            'sujet': 'Sujet de la conversation'
        }

class FormulaireMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu', 'fichier', 'image']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Écrivez votre message ici...'
            }),
        }
        labels = {
            'contenu': 'Message',
            'fichier': 'Joindre un fichier',
            'image': 'Joindre une image'
        }