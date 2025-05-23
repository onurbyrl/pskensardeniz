from core.models import Intervention

def interventions_context(request):
    return {
        'intervention': Intervention.objects.all(),
        'redirect_to': request.path
    }

def auth_status(request):
    return {
        "is_authenticated": request.user.is_authenticated
    }