from .models import Application

def applications_context(request):
    return {
        'applications': Application.objects.all(),
        'redirect_to': request.path
    }