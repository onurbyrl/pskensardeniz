from django.contrib import admin
from .models import Intervention, Message, Article

from django.contrib import admin
from django.contrib.auth.models import Group



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Message._meta.fields]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.unregister(Group)

admin.site.site_header = "Administration"
admin.site.site_title = "Psk Ensar Deniz Administration"
admin.site.index_title = "Welcome to Administration portal"

class ApplicationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Intervention)

admin.site.register(Article)