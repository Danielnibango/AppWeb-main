from django.contrib import admin
from .models import Formateur, Module, Apprenant, Cours, CustomUser

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_active', 'is_staff')
    list_filter = ('role',)

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Module)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'formateur', 'module', 'date_debut', 'date_fin', 'price', 'heure')

@admin.register(Apprenant)
class ApprenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approuver_apprenant']

    def approuver_apprenant(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Les apprenants sélectionnés ont été approuvés.")
    approuver_apprenant.short_description = "Approuver les apprenants sélectionnés"

@admin.register(Formateur)
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('get_nom', 'user', 'telephone', 'adress', 'module')

    def get_nom(self, obj):
        return obj.user.username

    get_nom.admin_order_field = 'user'  
    get_nom.short_description = 'Nom'
   
from .models import Paiement 
    
@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('apprenant', 'cours', 'formateur', 'mode_paiement', 'prix', 'date_paiement', 'statut')
    list_filter = ('mode_paiement', 'statut', 'date_paiement')
    search_fields = ('apprenant__username', 'cours__titre', 'formateur__nom')



