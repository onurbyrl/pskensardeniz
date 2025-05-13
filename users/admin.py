from django.contrib import admin
from .models import CustomUser, UserProfile, Appointment


admin.site.register(CustomUser)
admin.site.register(UserProfile)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ('notes',)
    fields = ('client', 'date', 'time', 'notes', 'is_paid', 'my_notes')  # Sıra bu şekilde olacak