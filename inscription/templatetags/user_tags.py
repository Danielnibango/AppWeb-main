from django import template
from inscription.models import Formateur, Apprenant

register = template.Library()

@register.simple_tag
def get_user_role(user):
    if user.is_staff:
        return "Administrateur"
    if hasattr(user, 'formateur'):
        return "Formateur"
    if hasattr(user, 'apprenant'):
        return "Apprenant"
    return "Utilisateur"

def exclude_user(queryset, user):
    return queryset.exclude(id=user.id)