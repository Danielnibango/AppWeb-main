from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.boite_reception, name='boite_reception'),
    path('nouveau/', views.nouvelle_conversation, name='nouvelle_conversation'),
    path('nouveau/', views.nouvelle_conversation_formateur, name='nouvelle_conversation_formateur'),
    path('nouveau/', views.nouvelle_conversation_apprenant, name='nouvelle_conversation_apprenant'),
    path('<int:conversation_id>/', views.voir_conversation, name='voir_conversation'),
    path('<int:conversation_id>/', views.voir_conversation_formateur, name='conversation1'),
    path('nouveau/', views.voir_conversation_apprenant, name='conversation_apprenant'),
    
    path('message/<int:message_id>/supprimer/', views.supprimer_message, name='supprimer_message'),
    path('<int:conversation_id>/supprimer/', views.supprimer_conversation, name='supprimer_conversation'),
    
    # Ajoutez cette ligne pour l'API de vérification des messages non lus
    path('api/non-lus/', views.check_new_messages, name='check_new_messages'),
    path('<int:conversation_pk>/', views.conv_apprenant, name='conv_apprenant'),
    path('<int:conversation_pk>/', views.conv_formateur, name='conv_formateur'), 
]