from .models import Intervention

def interventions_context(request):
    return {
        'intervention': Intervention.objects.all(),
        'redirect_to': request.path
    }