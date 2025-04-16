from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals


# class AppointmentsConfig(AppConfig):
#     name = 'appointments'

#     def ready(self):
#         import users.signals