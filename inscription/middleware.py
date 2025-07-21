from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs exemptées (login, logout, static, etc.)
        exempt_urls = [
            reverse("login"),  # Nom de votre URL de connexion
            reverse("logout"),
            "/admin/",  # Si vous utilisez l'admin Django
            "/static/",  # Fichiers statiques
            "/media/",   # Fichiers média
        ]

        if not request.user.is_authenticated and not any(
            request.path.startswith(url) for url in exempt_urls
        ):
            return redirect(settings.LOGIN_URL + f"?next={request.path}")

        return self.get_response(request)

